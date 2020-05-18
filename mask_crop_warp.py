import ants
import os
import re
import numpy as np
import nibabel as nb

class basic(object):
	# according to path get all file under this path
	def make_dir_list(self,path):
		dir_list = []
		file_list = sorted(os.listdir(path))
		for img in file_list:
			dir = os.path.join(path, img)
			print(dir,'  put in to list')
			dir_list.append(dir)
		return dir_list

	# 创建文件夹
	def mkdir(self,dirs):
		if not os.path.exists(dirs):
			os.makedirs(dirs)

class crop(object):
	def crop(self,img_dir,label_dir):
		img_pix = ants.image_read(img_dir)
		img = img_pix.numpy()
		label_pix = ants.image_read(label_dir)
		label = label_pix.numpy()
		# label_nib = nib.load('Label/N001_Q_QSM_SyNAggro_moved_ROIs.nii.gz')
		# np_data = np.array(label_nib.dataobj)
		# # print(np.where(np_data>3))
		label_bounding_box_0 = np.where(label > 0)  # label =1 to 10
		label_bounding_box_11 = np.where(label < 11)
		print(label_bounding_box_11)
		x_min = np.min(label_bounding_box_0[0])
		y_min = np.min(label_bounding_box_0[1])
		z_min = np.min(label_bounding_box_0[2])
		x_max = np.max(label_bounding_box_0[0])
		y_max = np.max(label_bounding_box_0[1])
		z_max = np.max(label_bounding_box_0[2])
		print(x_min, y_min, z_min, x_max, y_max, z_max,img_dir)
		cropped_label = ants.crop_indices(label_pix, (x_min, y_min, z_min), (x_max, y_max, z_max))
		#  cropped = ants.crop_image(img,label,3)
		cropped_img = ants.crop_indices(img_pix, (x_min, y_min, z_min), (x_max, y_max, z_max))
		if not os.path.exists("data/QSM_masked_cropped/"):
			os.makedirs("data/QSM_masked_cropped/")
		if not os.path.exists("data/label_cropped/"):
			os.makedirs("data/label_cropped/")
		img_name = re.split(r'[/.]', img_dir)[2]
		label_name = re.split(r'[/.]', label_dir)[2]
		ants.image_write(cropped_img, "data/QSM_masked_cropped/" +img_name+ "_cropped.nii.gz")
		ants.image_write(cropped_label, "data/label_cropped/" + label_name + "_cropped.nii.gz")

class mask(object):
	# make all QSM masked
	def masked(self,pic_list):
		for i in pic_list:
			file_name = re.split(r'[/.]', i)[2]
			image = nb.load(i)
			# 把仿射矩阵和头文件都存下来
			affine = image.affine.copy()
			hdr = image.header.copy()
            # float data
			image_np = image.get_fdata()
			###########      mask   ####################
			mask = image_np.copy()
			mask[mask != 0] = 1
			###########################################
			max_num = np.max(image_np)
			min_num = np.min(image_np)
			image_np = np.round((image_np - min_num) * 255 / (max_num - min_num))
			image_np.astype(np.uint8)
			image_masked = np.multiply(image_np, mask)

			# 形成新的nii文件
			image_masked = nb.Nifti1Image(image_masked, affine, hdr)
			if not os.path.exists("data/QSM_masked/"):
				os.makedirs("data/QSM_masked/")
			nb.save(image_masked, "data/QSM_masked/"+file_name+"_mask.nii.gz")
			print(i+' has been masked')
	# save the mask of the target QSM here is the last one of the list
	def save_mask_of_targetpic(self,pic_list):
		file_name = re.split(r'[/.]', pic_list[-1])[2]
		image=ants.image_read(pic_list[-1])
		mask=image.clone()
		mask[mask!=0]=1
		ants.image_write(mask,"data/mask_of_"+file_name+".nii.gz")

# implement the class
basicTool = basic()
maskTool=mask()
cropTool = crop()
################################# masked  QSM #########################
atlas_dir_list_all = basicTool.make_dir_list('data/QSM')
maskTool.masked(atlas_dir_list_all)
print('multiply mask to all qsm images')
maskTool.save_mask_of_targetpic(atlas_dir_list_all)
print('the mask of 37 has been made')
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

