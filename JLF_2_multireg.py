import os
import ants
import time
from label_fusion_ants import label_fusion_ants

begin = time.time()

# 创建文件夹
def mkdir(dirs):
    if not os.path.exists(dirs):
        os.system("mkdir "+dirs)


def make_dir_list(path):
    dir_list = []
    file_list = sorted(os.listdir(path))
    for img in file_list:
        dir = os.path.join(path, img)
        print(dir, '  put in to list')
        dir_list.append(dir)
    return dir_list

# target QSM has no need of warped so use masked
# 读入target_image_mask
target_name = 'data/QSM_masked/N037_QSM_mask.nii.gz'
# read mask of target image
target_mask_name = 'data/mask_of_N037_QSM.nii.gz'

# atlas_list 和 label_list
atlas_list = make_dir_list('data/fusion_label_multi/QSM_warped')
label_list = make_dir_list('data/fusion_label_multi/label_warped')
print(atlas_list)
print(label_list)

"""
 核心算法：joint label fusion
	def label_fusion_ants(target_image, atlas_images, atlas_labels, output_label, 
                            rp=2, rs=3, alpha=0.1, beta=2, mask='',verbose = False,parallel = 8):
"""
fusion_result_dirname = "fusion_result"
output_label_name = 'fusion_result.nii.gz'
label_fusion_ants(target_image=target_name, atlas_images=atlas_list,atlas_labels=label_list,output_label=output_label_name, verbose=True)  #,mask=target_mask_name

t = time.time() - begin
print('program complete in {:.0f}m {:.0f}s'.format(t // 60, t % 60)) # 打印出来时间

