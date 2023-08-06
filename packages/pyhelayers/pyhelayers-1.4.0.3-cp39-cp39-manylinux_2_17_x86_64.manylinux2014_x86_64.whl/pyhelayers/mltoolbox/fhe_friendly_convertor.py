'''
MIT License

Copyright (c) 2020 International Business Machines

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import os
import numpy as np
import torch
from torch.optim.lr_scheduler import ReduceLROnPlateau
import pyhelayers.mltoolbox.he_dl_lib.poly_activations as poly_activations
from pyhelayers.mltoolbox.utils.util import get_optimizer
from pyhelayers.mltoolbox.he_dl_lib.my_logger import get_logger
from pyhelayers.mltoolbox.utils.util import load_checkpoint
from types import SimpleNamespace
from pyhelayers.mltoolbox.trainer import Trainer



def starting_point(args):
    """Initializes and returns the Trainer and FheFriendlyConvertor based on user arguments

    Args:
        args (Arguments): the user arguments

    Returns:
        Trainer: the Trainer
        FheFriendlyConvertor: the FheFriendlyConvertor
    """
    # set seed for  reproducibility
    set_seed(args)
    
    if args.from_checkpoint:
        model, optimizer, train_state, loss, metrics, was_completed = load_checkpoint(args)   
        trainer =  Trainer(args, model,optimizer)
        fhe_friendly = FheFriendlyConvertor(args, train_state, was_completed)
        epoch = train_state.epoch
    else:
        trainer =  Trainer(args)
        fhe_friendly = FheFriendlyConvertor(args)
        epoch = 0
    return trainer, fhe_friendly, epoch  



def _calc_relu_ratio(start_epoch: int, epoch: int, change_round: int):
    """Calculates the required ratio of the new activation in the smooth replacement strategy, based on current epoch

    Args:
        start_epoch (int): number of epoch when the replacement started
        epoch (int): current epoch number
        change_round (int): number of epochs for full replacement

    Returns:
        int: change index (relevant only for args.replace_all_at_once=False, when on each change_round a single activation is replaced, for args.replace_all_at_once=True the only possible change_index is 0 )
        float: ratio
        
    """
    change_progress = float(epoch - start_epoch) / change_round
    change_index = int(change_progress)
    change_ratio = change_progress - change_index

    return change_index, change_ratio



def _init_distillation_model(args):
    """Loads the distillation model, if it was specified in user arguments

    Args:
        args (Arguments): user arguments
    """
    if args.distillation_path:
        logger = get_logger()
        logger.info(f"Loading distillation model from {args.distillation_path}")
        
        chk_point = {}
        if args.cuda:
            chk_point = torch.load(os.path.join(args.distillation_path))
        else:
            chk_point = torch.load(os.path.join(args.distillation_path), map_location=torch.device('cpu'))

        args.distillation_model = chk_point['model']
    else:
        args.distillation_model = None



def set_seed(args):
    """Impose reproducibility

    Args:
        args (Arguments): user arguments
    """
    seed = args.seed
    torch.manual_seed(seed)

    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(seed)

    if args.cuda:
        torch.cuda.manual_seed_all(seed)



class FheFriendlyConvertor:
    """This class helps in the FHE conversion of the model; namely the activation replacement. 
    It holds the current model conversion state. The initialization ca be either from scratch, or from some given point - this can be
    usefull when loading a mnodel from a checkpoint.
    """
    def __init__(self, args, train_state=None, was_completed=None):
        self.__init_from_scratch(args)
        if ((was_completed is not None) and (train_state is not None)):
            self.was_completed = was_completed
            self.start_epoch = train_state.start_epoch
            self.wait_before_change = train_state.wait_before_change
            self.logger.debug("init from checkpoint")
        
        
        
    def __init_from_scratch(self, args):
        self.logger = get_logger()
        if args.cuda:
            self.logger.info("Visible gpu devices: " + os.environ["CUDA_VISIBLE_DEVICES"])

        # coefficients scale for trainable poly activation
        assert isinstance(args.coeffs_scale, list)
        self.logger.info(f"loaded coeffs_scale is {args.coeffs_scale}")

        _init_distillation_model(args)

        self.start_epoch = 0
        self.wait_before_change = args.epoch_to_start_change
        self.was_completed = (args.activation_type == 'relu')
        self.best_loss = None
        self.best_epoch = None
        
        
    def get_start_epoch(self):
        return self.start_epoch
    
    def get_wait_before_change(self):
        return self.wait_before_change
    
    def get_was_completed(self):
        return self.was_completed
       
    def set_best_found_loss_and_epoch(self, loss, epoch):
        self.best_loss = loss
        self.best_epoch = epoch
        
        
    def get_best_found_loss(self):
        return self.best_loss
    
    
    def create_train_state(self, epoch: int):
        """Returns a namespace that groups start_epoch, current epoch and wait_before_change together

        Args:
            epoch (int): the current epoch

        Returns:
            SimpleNamespace: a namespace that groupps the passed in arguments together
        """
        return SimpleNamespace(start_epoch=self.start_epoch, epoch=epoch, wait_before_change=self.wait_before_change)


    def replace_activations(self, args, trainer, epoch, scheduler):
        """Handles the entire replacement logic - depending on the arguments values and current epoch

        Args:
            args (object): The user arguments
            trainer (Trainer): trainer instance
            epoch (int): current epoch number
            scheduler (ReduceLROnPlateau): Learning rate reduction schedualer
        """

        # condition to start activation modification
        act_change_needed = (args.activation_type != 'relu')
        is_time_to_change = (epoch > self.start_epoch + self.wait_before_change) and (not self.was_completed)

        if not act_change_needed:
            self.was_completed = True
            return 

        if is_time_to_change:
            model = trainer.get_model()
            optimizer = trainer.get_optimizer()
            activation_gen = poly_activations.get_activation_gen(args.activation_type, args.coeffs_scale)
            # two main cases - smooth and not smooth
            # 1 - smooth
            if args.smooth_transition:
                self.__replace_activations_smooth(model, activation_gen, epoch, optimizer, scheduler, args)
            # 2 - not smooth
            else: 
                scheduler = self.__replace_all_activations(model, activation_gen, args, scheduler)
                self.start_epoch = epoch


    def __replace_all_activations(self, model, activation_gen, args, scheduler):
        """Replaces relu activations in a non-smooth manner, either all at once or one by one. updates the was_completed and wait_before_change states 
            Starts a new scheduler.
        Args:
            model(nn.Module) : Input model
            activation_gen (lambda): A lambda fumction to generate the required activation
            args (Arguments): user arguments

        Raises:
            Exception: There are no ReLU activations to replace - check configuration and the model

        Returns:
            ReduceLROnPlateau: Handles reduction of learning rate when a metric has stopped improving
        """
        new_activations = poly_activations.replace_relu_activations(model, activation_gen, args.replace_all_at_once)
        
        if len(new_activations) == 0: #if no replacement was performed 
            raise Exception("There are no ReLU activations to replace - check configuration and the model")

        if args.cuda:
            model = model.cuda()
        self.logger.info(model)
        self.logger.info(f"restart optimizer and scheduler for activation {new_activations}")
        optimizer = get_optimizer(args, model)
        scheduler = ReduceLROnPlateau(optimizer, factor=0.5, patience=2, min_lr=args.min_lr, verbose=True)
        self.wait_before_change = args.change_round

        self.was_completed = False
        if len(poly_activations.get_relu_activations(model)) == 0:  # there are no more relu activations to replace
            self.logger.info("All changes completed")
            self.was_completed = True

        return scheduler


    def __replace_activations_smooth(self, model, activation_gen, epoch, optimizer, scheduler, args):
        """Replaces relu activations in a smooth manner, updates the was_completed state . Updates the scheduler.

        Args:
            model (nn.Module): the input model
            activation_gen (lambda): A lambda function to generate the required activation
            epoch (int): current epoch
            optimizer (torch.optim): optimizer
            scheduler (ReduceLROnPlateau): scheduler
            args (Arguments): user arguments

        """
        change_index, change_ratio = _calc_relu_ratio(self.start_epoch + self.wait_before_change, epoch, args.change_round)
        new_activations, is_missing = poly_activations.create_or_update_weighted_activations(model, activation_gen,
                                                                                            change_index, change_ratio,
                                                                                            args.replace_all_at_once)
        if len(new_activations) == 0: #if no replacement was performed 
            self.logger.info(f"Transition phase: {change_index}:{change_ratio}" )
        else:
            if args.cuda:
                model = model.cuda()
            for name, activation in new_activations:
                # add new parameters to optimizer and scheduler
                optimizer.add_param_group({'params': activation.parameters(), 'lr': args.lr_new})
                scheduler.min_lrs.append(args.min_lr)
            self.logger.info(model)
            self.logger.debug(optimizer)
            self.logger.info(f"Started changing {change_index} with ratio {change_ratio}")

        self.was_completed = False
        if is_missing:
            self.logger.info("All changes completed")
            self.was_completed = True


