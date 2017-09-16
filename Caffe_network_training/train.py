#!/usr/bin/env python

import create_labellist
import config
import os
import sys
import numpy as np
from preprocess import *

def training(training_config):
    training_command = training_config['caffe_tools_path'] + 'caffe train ' + '-solver=' + \
                        training_config['solver_file']
    if training_config['use_GPU']:
        training_command = training_command + ' --gpu=' + training_config['GPU_id']
    print training_command
    os.popen(training_command)

if __name__ == '__main__':
    train_config = {}
    val_config = {}
    lmdb_config = {}
    mean_config = {}
    training_config = {}

    # load configuration from config.py
    train_config, val_config, lmdb_config, mean_config, training_config = load_config()

    build_list(train_config, val_config)
    build_lmdb(lmdb_config)
    gen_mean(mean_config)
    training(training_config)

    print "\nDeleting list file..."
    os.unlink(config.output_path + 'train.txt')
    os.unlink(config.output_path + 'val.txt')
    print "Delete complete.\n"

    print "All done."
