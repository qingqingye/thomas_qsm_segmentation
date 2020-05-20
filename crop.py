import ants
import os
import re
import numpy as np
import nibabel as nb
from lib import *

if __name__ == '__main__':
	# implements class from lib.py
	basicTool = basic()
	cropTool = crop()

	warped_QSM_dir_list = basicTool.make_dir_list('data/fusion_label_multi/QSM_warped')
	warped_label_dir_list = basicTool.make_dir_list('data/fusion_label_multi/label_warped')
	path = 'data/fusion_label_multi/'
	if not os.path.exists('data/fusion_label_multi/QSM_warped/N037_QSM_mask.nii.gz'):
		print('not exist')
		basicTool.cop_target('data/QSM_masked/N037_QSM_mask.nii.gz', 'data/fusion_label_multi/QSM_warped/N037_QSM_mask.nii.gz' )
	if not os.path.exists('data/fusion_label_multi/label_warped/N037_Q_QSM_SyNAggro_moved_ROIs.nii.gz'):
		basicTool.cop_target('data/Label/N037_Q_QSM_SyNAggro_moved_ROIs.nii.gz', 'data/fusion_label_multi/label_warped/N037_Q_QSM_SyNAggro_moved_ROIs.nii.gz' )
	print('succeed copy target QSM and label')
	cropTool.crop(warped_QSM_dir_list,warped_label_dir_list, path,[0,0])