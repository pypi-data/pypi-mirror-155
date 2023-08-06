

import argparse
import math
import os
import random
import sys
import time
from copy import deepcopy
from datetime import datetime
from pathlib import Path

import numpy as np
import torch
import torch.distributed as dist
import torch.nn as nn
import yaml
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.optim import SGD, Adam, AdamW, lr_scheduler
from tqdm import tqdm

from FastCNN.nn.experimental import attempt_load
from FastCNN.nn.yolo import Model

from FastCNN.utils.autoanchor import check_anchors
from FastCNN.utils.autobatch import check_train_batch_size
from FastCNN.utils.CallBacks import Callbacks
from FastCNN.utils.dataloaders import create_dataloader
from FastCNN.utils.downloads import attempt_download
from FastCNN.utils.general import (LOGGER, check_amp, check_dataset, check_file, check_git_status, check_img_size,
                           check_requirements, check_suffix, check_version, check_yaml, colorstr, get_latest_run,
                           increment_path, init_seeds, intersect_dicts, labels_to_class_weights,
                           labels_to_image_weights, methods, one_cycle, print_args, print_mutation, strip_optimizer)
from FastCNN.utils.loggers import Loggers
from FastCNN.utils.loggers.wandb.wandb_utils import check_wandb_resume
from FastCNN.utils.loss import ComputeLoss
from FastCNN.utils.metrics import fitness
from FastCNN.utils.plots import plot_evolve, plot_labels
from FastCNN.utils.torch_utils import EarlyStopping, ModelEMA, de_parallel, select_device, torch_distributed_zero_first

LOCAL_RANK = int(os.getenv('LOCAL_RANK', -1))  # https://pytorch.org/docs/stable/elastic/run.html
RANK = int(os.getenv('RANK', -1))
WORLD_SIZE = int(os.getenv('WORLD_SIZE', 1))

from FastCNN.prx.PathProxy import PathProxy3 as PathProxy
from IutyLib.commonutil.config import JConfig

def getConfig(projectid,modelid):
    cfgpath = PathProxy.getConfigPath(projectid,modelid)
    
    jfile = JConfig(cfgpath)
    data = jfile.get()
    return data


def train(projectid,modelid):
    config = getConfig(projectid,modelid)
    net_name = config["Type"]
    
    #modelpath = PathProxy.getModelDir(projectid,modelid)
    #last = os.path.join(modelpath,"TrainSaver","save.pth")
    #best = os.path.join(modelpath,"ValidSaver","save.pth")
    

def val(projectid,modelid):
    pass