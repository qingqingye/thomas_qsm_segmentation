import ants
import time
import numpy as np
import nibabel as nb
from lib import *

if __name__ == '__main__':
	basicTool = basic()
	label_fusion_tool = label_fusion()
	begin = time.time()
	target_name = 'data/fusion_label_multi/QSM_warped/N001_QSM_masked_warped.nii.gz'
	# read mask of target image
	target_mask_name = 'data/mask/mask_of_N001_QSM.nii.gz'

	# atlas_list 和 label_list
	atlas_list = basicTool.make_dir_list('data/fusion_label_multi/QSM_warped')[1:]
	# important! according to specify situation to get image without target qsm and target label
	label_list = basicTool.make_dir_list('data/fusion_label_multi/label_warped')[1:]
	print(atlas_list)
	print(label_list)

	"""
	 核心算法：joint label fusion
		def label_fusion_ants(target_image, atlas_images, atlas_labels, output_label, 
	                            rp=2, rs=3, alpha=0.1, beta=2, mask='',verbose = False,parallel = 8):
	"""
	fusion_result_dirname = "fusion_result"
	output_label_name = 'fusion_result.nii.gz'
	label_fusion_tool.label_fusion_ants(target_image=target_name, atlas_images=atlas_list, atlas_labels=label_list,
					  output_label=output_label_name, verbose=True)  # ,mask=target_mask_name

	t = time.time() - begin
	print('program complete in {:.0f}m {:.0f}s'.format(t // 60, t % 60))  # 打印出来时间


