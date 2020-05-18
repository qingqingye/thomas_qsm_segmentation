
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pylab as plt
#import matplotlib.pyplot as plt
import nibabel as nib
from nibabel import nifti1
from nibabel.viewers import OrthoSlicer3D

example_filename = 'N002_Q_QSM_SyNAggro_moved_ROIs.nii.gz'
img = nib.load(example_filename)
print(img)
print(img.header['db_name'])  # 输出头信息

#shape有四个参数 patient001_4d.nii.gz
#shape有三个参数 patient001_frame01.nii.gz   patient001_frame12.nii.gz
#shape有三个参数  patient001_frame01_gt.nii.gz   patient001_frame12_gt.nii.gz
width, height, queue = img.dataobj.shape
OrthoSlicer3D(img.dataobj).show()

num = 1
for i in range(0, queue, 10):
    img_arr = img.dataobj[:, :, i]
    plt.subplot(5, 4, num)
    plt.imshow(img_arr, cmap='gray')
    num += 1

plt.show()
# img_arr = nib.load('NC_02_Sub028_restore_brain_flipped.nii.gz').get_data()
# plt.imshow(img_arr.numpy()[0, :, :, :].squeeze(), cmap=plt.cm.gray_r)
# plt.pause(3)
