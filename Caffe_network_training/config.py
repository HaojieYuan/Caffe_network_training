#
# This is the configuration file for caffe image pre processing
#
# All you need to do is offering :
#   1. caffe master path
#   2. compiled caffe tools path
#   3. generate destination path
#   4. image class number and labels
#   5.*image path of every class
#   6. image numbers you want to add
#   7. resize configurartion
#   8. training configuration
#
# Note that path is stored in a list, keep them in the right order.
#
# Another thing have to be mentioned is caffe use both train and validate data
# at same time, so you need to specify two pathes contain all image classes.

# Sepcify your caffe master path, in order someone changed caffe path architecture,
# also specify some subdirectories below
caffe_master_path = '/home/haojie/code/caffe-master/'

# Specify your caffe tools path, in most cases it is 'Caffe_root_path/build/tools/'
# which should contain binary files named caffe, convert_imageset and compute_image_mean
caffe_tools_path = '/home/haojie/code/caffe-master/build/tools/'


# LMDB file and mean file generate destination
output_path = '/home/haojie/last_train/1000:2000/'
train_DB_name = 'gen_train_lmdb'
val_DB_name = 'gen_val_lmdb'
mean_file_name = 'gen_mean.binaryproto'

# Specify if you need a npy mean file out put
# npy mean file will be useful when deploying a net you trained
# And you will need to specify pycaffe directory
# Usually it's Caffe_root_path/python
# If you don't have one
# Try 'make pycaffe' in caffe_root_path
gen_npy_mean = True
npy_mean_file_name = 'gen_mean.npy'
pycaffe_path = '/home/haojie/code/caffe-master/python/'

# Configure your image class number and labels
# Label list length should have a length same as class_number
class_number = 2
_label = [0, 1]

# Configure your image source pathes
# Note that train path list and validate path list should be in same order
train_path = ['/home/haojie/data/training_data/blot',
         '/home/haojie/data/training_data/other']
validate_path = ['/home/haojie/data/validate_data/blot',
         '/home/haojie/data/validate_data/other']
# In fact only '/ ' will work since we generate absolute pathes
# which has absolute path
data_root_path = '/ '

# Configure image numbers you want to add each class
# Note that don't specify an amount lager than number of images you have
train_amount = [1000, 2000]
val_amount = [100, 100]

# Decide if you need image reshape
resize = True
# Only useful when resize is True
resize_height = 227
resize_width = 227

# Sepcify your solver file, which should contain learning config,
# iteration config...etc. If you don't know how to write it, you can take
# a look at solver sample file.
solver_file = '/home/haojie/last_train/1000:2000/solver.prototxt'

# Usualy training with GPU is much faster,
# but it also means you have to deal with graphic card driver installation,
# caffe-GPU installation, CUDA installation...etc.
# Anyway, good luck.
use_GPU = False
# You can spcify multy GPU here, as long as you installed NCCL for caffe.
# Use comma to to separate different GPU
# e.g. GPU_id = '0,1'
GPU_id = '0'
