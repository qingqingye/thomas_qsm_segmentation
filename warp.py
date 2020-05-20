import ants
import os
import re
import numpy as np
import nibabel as nb
from lib import *

# implement the class
basicTool = basic()
warpTool = warp()

############################### warp ###################
masked_dir_list_all = basicTool.make_dir_list('data/QSM_masked')
target_num= 0
masked_dir_list = masked_dir_list_all
label_dir_list = basicTool.make_dir_list('data/Label')
#TODO
testdir = masked_dir_list_all[0]
testsubject_img = ants.image_read(testdir)

warpTool.warp(masked_dir_list,label_dir_list,target_num)

