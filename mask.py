import ants
import os
import re
import numpy as np
import nibabel as nb
from lib import *



# implement the class
basicTool = basic()
maskTool=mask()
cropTool = crop()
################################# masked  QSM #########################
atlas_dir_list_all = basicTool.make_dir_list('data/QSM')
print(atlas_dir_list_all)
target_num = 0   # target num from 0 to 24
maskTool.masked(atlas_dir_list_all)
print('multiply mask to all qsm images')
target_img_dir = atlas_dir_list_all[target_num]
maskTool.save_mask_of_targetpic(target_img_dir)
print('the mask of target has been made')




