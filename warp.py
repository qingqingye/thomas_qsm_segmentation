import ants
import os
import re
import numpy as np
import nibabel as nb
from lib import *

# implement the class
basicTool = basic()
warpTool = warp()

############################### crop label and qsm_maksed by one bouding box###################
masked_dir_list_all = basicTool.make_dir_list('data/QSM_masked')
masked_dir_list = masked_dir_list_all[0:-1]
label_dir_list = basicTool.make_dir_list('data/Label')[0:-1]
#TODO
testdir = masked_dir_list_all[-1]
testsubject_img = ants.image_read(testdir)


# 读取文件, 有24个atlas
for i in range(0,24):
	move_img = ants.image_read(masked_dir_list[i]) # subject的图像
	# 配准，使用SyN
	outs = ants.registration(testsubject_img,move_img,type_of_transforme = 'SyN')
	atlas_name = re.split(r'[/.]', masked_dir_list[i])[2]
	print(atlas_name, ' has been warped')
	# atlas的label_img
	atlas_label_img = ants.image_read(label_dir_list[i]) # atlas的标签图像
	# 模板标签warp到图像,move_img是要配准到的空间即（fix），label_img是要应用变化的图像（move），transformlist是move到fix的转换矩阵，genericLabel用于多标签的插值
	warped_atlas_label_img =  ants.apply_transforms(fixed = testsubject_img ,moving = atlas_label_img ,transformlist = outs['fwdtransforms'],interpolator = 'nearestNeighbor')  #'genericLabel'
	# get file name( without .nii.gz)
	label_name = re.split(r'[/.]', label_dir_list[i])[2]
	print(label_name, 'has been warped')

	# 保存变换后的图像
	basicTool.mkdir('data/fusion_label_multi/QSM_warped')
	basicTool.mkdir('data/fusion_label_multi/label_warped')
	warped_atlas_label_filename = 'data/fusion_label_multi/label_warped/Sub_'+label_name+'warped_label.nii.gz'
	warped_atlas_filename = 'data/fusion_label_multi/QSM_warped/Sub_'+atlas_name + 'warped.nii.gz'

	ants.image_write(warped_atlas_label_img,warped_atlas_label_filename) 
	ants.image_write(outs['warpedmovout'],warped_atlas_filename)

