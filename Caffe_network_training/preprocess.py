#!/usr/bin/env python

"""preprocess.py: generate lmdb files and meanfile caffe need for training"""

# I will try to use yaml to load configuration next time

__author__ = "HaojieYuan"
__email__ = "haojie.d.yuan@gmail.com"
__version__ = "0.1"

import create_labellist
import config
import os
import sys
import numpy as np

def load_config():
    # First we need to generate file list, which will be removed at last
    train_config = {}
    val_config = {}
    lmdb_config = {}
    mean_config = {}
    training_config = {}

    train_config['_path'] = config.train_path
    train_config['class_number'] = config.class_number
    train_config['_label'] = config._label
    train_config['file_path'] = config.output_path + 'train.txt'
    train_config['amount'] = config.train_amount

    val_config['_path'] = config.train_path
    val_config['class_number'] = config.class_number
    val_config['_label'] = config._label
    val_config['file_path'] = config.output_path + 'val.txt'
    val_config['amount'] = config.val_amount

    # This is to make sure file list can be used for generating by using absolute path
    train_config['absolute_path'] = 1
    val_config['absolute_path'] = 1

    # Next we load lmdb config
    lmdb_config['output_path'] = config.output_path
    lmdb_config['resize'] = config.resize
    lmdb_config['resize_height'] = config.resize_height
    lmdb_config['resize_width'] = config.resize_width
    lmdb_config['caffe_tools_path'] = config.caffe_tools_path
    lmdb_config['data_root_path'] = config.data_root_path
    lmdb_config['train_DB_name'] = config.train_DB_name
    lmdb_config['val_DB_name'] = config.val_DB_name

    # Here we load mean file config
    mean_config['caffe_tools_path'] = config.caffe_tools_path
    mean_config['output_path'] = config.output_path
    mean_config['train_DB_name'] = config.train_DB_name
    mean_config['mean_file_name'] = config.mean_file_name
    mean_config['gen_npy_mean'] = config.gen_npy_mean
    mean_config['pycaffe_path'] = config.pycaffe_path
    mean_config['npy_mean_file_name'] = config.npy_mean_file_name

    # Also load train config for training, although it's not used in preprocess
    training_config['caffe_tools_path'] = config.caffe_tools_path
    training_config['solver_file'] = config.solver_file
    training_config['use_GPU'] = config.use_GPU
    training_config['GPU_id'] = config.GPU_id

    return train_config, val_config, lmdb_config, mean_config, training_config

def build_list(train_config, val_config):

    # Create train.txt and val.txt
    _file = open(train_config['file_path'], "w+")
    _file.close()
    _file = open(val_config['file_path'], "w+")
    _file.close()

    train_builder = create_labellist.builder(train_config)
    create_labellist.create_labellist(train_builder)

    val_builder = create_labellist.builder(val_config)
    create_labellist.create_labellist(val_builder)

def check_path(_path):

    return os.path.isdir(_path)

def build_lmdb(lmdb_config):

    if check_path(lmdb_config['output_path']) == False:
        sys.exit("Error: output_path does not exist, please check your config file.")

    # As caffe do not have python convert_imageset, compute_image_mean
    # So I have to use os.popen() to run a compiled C++ file
    # If you have a better way to do this, please contact me
    if lmdb_config['resize'] == True:
        resize_height = lmdb_config['resize_height']
        resize_width = lmdb_config['resize_width']
    else:
        resize_height = 0
        resize_width = 0

    print "\nCreating train lmdb..."
    gen_trainDB_command = lmdb_config['caffe_tools_path'] + 'convert_imageset' + \
               ' --resize_height=' + str(resize_height) + \
               ' --resize_width=' + str(resize_width) + \
               ' --shuffle ' + lmdb_config['data_root_path'] + ' ' + \
               lmdb_config['output_path'] + 'train.txt ' + \
               lmdb_config['output_path'] + lmdb_config['train_DB_name']
    os.popen(gen_trainDB_command)
    print "Train lmdb generate complete.\n"

    print "\nCreate validate lmdb..."
    gen_valDB_command = lmdb_config['caffe_tools_path'] + 'convert_imageset' + \
               ' --resize_height=' + str(resize_height) + \
               ' --resize_width=' + str(resize_width) + \
               ' --shuffle ' + lmdb_config['data_root_path'] + ' ' + \
               lmdb_config['output_path'] + 'val.txt ' + \
               lmdb_config['output_path'] + lmdb_config['val_DB_name']
    os.popen(gen_valDB_command)
    print "Validate lmdb generate complete.\n"

def gen_mean(mean_config):

    print "\nGenerating binaryproto mean file from train DB..."
    gen_bin_mean_command = mean_config['caffe_tools_path'] + 'compute_image_mean ' + \
                           mean_config['output_path'] + mean_config['train_DB_name'] + ' ' + \
                           mean_config['output_path'] + mean_config['mean_file_name']
    os.popen(gen_bin_mean_command)
    print "binaryproto mean file generate complete.\n"

    # Caffe module import will take a long time
    # It is not nessary to import it if you don't want a npy mean file
    # So I put import here
    if mean_config['gen_npy_mean'] == True:
        print "\nGenerating npy mean file from train DB..."
        sys.path.append(mean_config['pycaffe_path'])
        import caffe
        blob = caffe.proto.caffe_pb2.BlobProto()
        data = open( mean_config['output_path'] + mean_config['mean_file_name'] , 'rb' ).read()
        blob.ParseFromString(data)
        arr = np.array( caffe.io.blobproto_to_array(blob) )
        out = arr[0]
        np.save( mean_config['output_path'] + mean_config['npy_mean_file_name'] , out )
        print "npy mean file generate complete.\n"

if __name__ == '__main__':

    train_config = {}
    val_config = {}
    lmdb_config = {}
    mean_config = {}
    tmp = {}

    # load configuration from config.py
    train_config, val_config, lmdb_config, mean_config, tmp = load_config()
    # use create_labellist.py generate list we need
    build_list(train_config, val_config)
    build_lmdb(lmdb_config)
    gen_mean(mean_config)

    print "\nDeleting list file..."
    os.unlink(config.output_path + 'train.txt')
    os.unlink(config.output_path + 'val.txt')
    print "Delete complete.\n"

    print "All done."
