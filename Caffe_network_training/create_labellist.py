#!/usr/bin/env python

"""create_labellist.py: Create list file of objects with labels"""

__author__ = "HaojieYuan"
__email__ = "haojie.d.yuan@gmail.com"
__version__ = "1.0"

import os
import random
import sys

class builder(object):

    config = {}
    file_list = None

    def open_file_list(self):
        """try to open the file, return 1 if succeded"""
        try:
            self.file_list = open(self.config['file_path'], 'w')
            return 1
        except IOError:
            print "Error while opening file %s" % self.config['file_path']
            return 0

    def close_file_list(self):
        """try to close the file after detect if it's already closed"""
        if self.file_list is None:
            print "The file is already closed."
        else:
            self.file_list.close()
            self.file_list = None

    def writein(self, image_name, image_label):
        """write in the file list with given path and label"""
        writein_line = "%s %s\n" % (image_name, image_label)
        self.file_list.write(writein_line)

    def add_to_file_list(self):
        """add sepcified amount of objects in the dirctory to the list according to amount parameter"""
        count = 0
        for i in range(0, self.config['class_number']):
            object_list = os.listdir(self.config['_path'][i])
            if len(object_list) < self.config['amount'][i]:
                sys.exit("Error: amount larger than image number, program terminated.")
            else:
                object_label = self.config['_label'][i]
                timer = 0

                while True:
                    object_name = random.choice(object_list)
                    if self.config['absolute_path'] == 1:
                        object_name = os.path.abspath(os.path.join(self.config['_path'][i], object_name))
                    self.writein(object_name, object_label)
                    count = count + 1
                    timer = timer + 1
                    if timer == self.config['amount'][i]:
                        break

        return count

    def __init__(self, config):
        """init instance with configuration from parameter"""
        self.config = config

def create_labellist(builder):
    """create a label list with items of specific amount"""
    count = 0

    if builder.open_file_list() == 1:
        count = builder.add_to_file_list()
        builder.close_file_list()
        print "List create success, totally %d objects added to list" % count
    else:
        sys.exit("Error opening file, program terminated.")
