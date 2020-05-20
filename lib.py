import ants
import os
import re
import numpy as np
import nibabel as nb

class dice(object):
    def dice(self,label_image_x_dirname, label_image_y_dirname):
        # 求出标签文件所有标签的dice

        image_x = ants.image_read(label_image_x_dirname).numpy()
        image_y = ants.image_read(label_image_y_dirname).numpy()

        # h = "变量1" if a>b else "变量2"

        max_num = np.max(image_x) if np.max(
            image_x) > np.max(image_y) else np.max(image_y)

        max_num = np.int(max_num)

        # Dice 存放每个标签的dice值
        Dice = np.zeros(max_num + 1)

        # 遍历每个标签

        print(max_num)
        for label in range(1, max_num + 1):

            intersect = 0  # 交集像素个数
            total = 0  # 全部像素

            # 遍历图像
            a = np.sum(image_x == label)
            b = np.sum(image_y == label)

            c = np.sum(((image_x - label) == 0) & ((image_y - label) == 0))

            if a + b != 0:
                Dice[label] = 2 * c / (a + b)

            # """
            # # 写入文件
            # with open(dest_file, 'a+') as f:
            #     f.write('')
            # """

        return Dice

    # def parse_args(self):
    #
    #     description = "计算两个标签文件的dice系数"
    #     parser = argparse.ArgumentParser(description=description)
    #
    #     parser.add_argument('filename', nargs=2, help="输入两个标签文件的文件名")
    #
    #     args = parser.parse_args()
    #     return args

    def dice_cal(self,label_image_x_dirname, label_image_y_dirname):

        print("——————————————开始运行————————————————")
        start = time.time()

        # args = parse_args()
        # [label_image1, label_image2] = args.filename

        DICE = dice(label_image_x_dirname, label_image_y_dirname)
        f = "dice.txt"
        with open(f, "a") as file:  # “a"，代表追加内容
            for i in range(0, len(DICE)):
                file.write("the dice of label %d is %g" % (i, DICE[i]) + "\n")
                print("the dice of label %d is %g" % (i, DICE[i]))
            t = time.time() - start
            file.write('程序结束于 {:.0f}m {:.0f}s'.format(t // 60, t % 60) + "\n")
            print('程序结束于 {:.0f}m {:.0f}s'.format(t // 60, t % 60))

class basic(object):
    # according to path get all file under this path
    def make_dir_list(self,path):
        dir_list = []
        file_list = sorted(os.listdir(path))
        for img in file_list:
            dir = os.path.join(path, img)
            print(dir,'  put in to list')
            dir_list.append(dir)
        return (dir_list)

    def cop_target(self,filename1,filename2):
        os.system("cp %s %s" % (filename1, filename2))
        # if you are using windows use copy

    # 创建文件夹
    def mkdir(self,dirs):
        if not os.path.exists(dirs):
            os.makedirs(dirs)

class mask(object):
    # make all QSM masked
    def masked(self,pic_list):
        for i in pic_list:
            file_name = re.split(r'[/.]', i)[-3]

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
            nb.save(image_masked, "data/QSM_masked/"+file_name+"_masked.nii.gz")
            print(i+' has been masked')
    # save the mask of the target QSM here is the last one of the list
    def save_mask_of_targetpic(self,pic_dir):
        if not os.path.exists("data/mask/"):
            os.makedirs("data/mask/")
        file_name = re.split(r'[/.]', pic_dir)[-3]
        image=ants.image_read(pic_dir)
        mask=image.clone()
        mask[mask!=0]=1
        ants.image_write(mask,"data/mask/mask_of_"+file_name+".nii.gz")

class warp(object):
    def warp(self,masked_dir_list,label_dir_list,target_num):
        basicTool = basic()
        basicTool.mkdir('data/fusion_label_multi/QSM_warped')
        basicTool.mkdir('data/fusion_label_multi/label_warped')
        # target img
        testsubject_img = ants.image_read(masked_dir_list[target_num])
        testsubject_label = ants.image_read(label_dir_list[target_num])

        target_file_name = re.split(r'[/.]', masked_dir_list[target_num])[-3]
        target_label_name = re.split(r'[/.]', label_dir_list[target_num])[-3]
        ants.image_write(testsubject_img,'data/fusion_label_multi/QSM_warped/' + target_file_name + '_warped.nii.gz')
        ants.image_write(testsubject_label,'data/fusion_label_multi/label_warped/' + target_label_name + '_warped.nii.gz')

        # del target img
        del masked_dir_list[target_num]
        del label_dir_list[target_num]
        print(masked_dir_list,label_dir_list)

        # 读取文件, 24个atlas
        for i in range(24):
            move_img = ants.image_read(masked_dir_list[i])  # subject的图像
            # 配准，使用SyN
            outs = ants.registration(testsubject_img, move_img, type_of_transforme='SyN')
            atlas_name = re.split(r'[/.]', masked_dir_list[i])[-3]
            print(atlas_name, ' has been warped')
            # atlas的label_img
            atlas_label_img = ants.image_read(label_dir_list[i])  # atlas的标签图像
            # 模板标签warp到图像,move_img是要配准到的空间即（fix），label_img是要应用变化的图像（move），transformlist是move到fix的转换矩阵，genericLabel用于多标签的插值
            warped_atlas_label_img = ants.apply_transforms(fixed=testsubject_img, moving=atlas_label_img,
                                                           transformlist=outs['fwdtransforms'],
                                                           interpolator='nearestNeighbor')  # 'genericLabel'
            # get file name( without .nii.gz)
            label_name = re.split(r'[/.]', label_dir_list[i])[-3]
            print(label_name, 'has been warped')

            # 保存变换后的图像
            warped_atlas_filename = 'data/fusion_label_multi/QSM_warped/' + atlas_name + '_warped.nii.gz'
            warped_atlas_label_filename = 'data/fusion_label_multi/label_warped/' + label_name + '_warped_label.nii.gz'
            ants.image_write(warped_atlas_label_img, warped_atlas_label_filename)
            ants.image_write(outs['warpedmovout'], warped_atlas_filename)


class crop(object):
    def __init__(self):
        self.x=[]
        self.y=[]
        self.z=[]

    def min_max(self,label_dir,x,y,z):
        label_pix = ants.image_read(label_dir)
        label = label_pix.numpy()
        label_bounding_box_0 = np.where(label > 0)  # label =1 to 10
        label_bounding_box_11 = np.where(label < 11)  # all voxel < 11, where is not label=0
        x_min = np.min(label_bounding_box_0[0])
        y_min = np.min(label_bounding_box_0[1])
        z_min = np.min(label_bounding_box_0[2])
        x_max = np.max(label_bounding_box_0[0])
        y_max = np.max(label_bounding_box_0[1])
        z_max = np.max(label_bounding_box_0[2])
        x.append(x_min)
        x.append(x_max)
        y.append(y_min)
        y.append(y_max)
        z.append(z_min)
        z.append(z_max)

    def crop_onpic(self,img_dir,label_dir,lowerind,upperind,path):
        img_pix = ants.image_read(img_dir)
        label_pix = ants.image_read(label_dir)
        cropped_img = ants.crop_indices(img_pix, lowerind, upperind)
        cropped_label = ants.crop_indices(label_pix, lowerind, upperind)
        img_name = re.split(r'[/.]', img_dir)[-3]
        label_name = re.split(r'[/.]', label_dir)[-3]
        ants.image_write(cropped_img, path + "QSM_masked_cropped/" + img_name + "_cropped.nii.gz")
        ants.image_write(cropped_label, path + "label_cropped/" + label_name + "_cropped.nii.gz")

    def crop_mask(self,mask_dir,lowerind,upperind):
        mask_pix = ants.image_read(mask_dir)
        cropped_mask = ants.crop_indices(mask_pix, lowerind, upperind)
        ants.image_write(cropped_mask, "data/mask/mask_of_N037_QSM_cropped.nii.gz")
        print('mask cropped')

    def crop(self,img_dir,label_dir,path,delta):
        if not os.path.exists(path+"QSM_masked_cropped/"):
            os.makedirs(path+"QSM_masked_cropped/")
        if not os.path.exists(path+"label_cropped/"):
            os.makedirs(path+"label_cropped/")
        x_min,y_min,z_min,x_max,y_max,z_max=self.get_size(img_dir,label_dir)
        x_min -= delta[0]
        y_min -= delta[0]
        z_min -= delta[1]
        x_max += delta[0]
        y_max += delta[0]
        z_max += delta[1]
        print(x_min,y_min,z_min,x_max,y_max,z_max)
        for i in range(25):
            print(i)
            print(img_dir[i],label_dir[i])
            self.crop_onpic(img_dir[i],label_dir[i],(x_min, y_min,z_min),(x_max, y_max , z_max),path)
            self.crop_mask('data/mask/mask_of_N037_QSM.nii.gz',(x_min, y_min,z_min),(x_max, y_max , z_max))

    def get_size(self,img_dir,label_dir):
        for i in label_dir:
            self.min_max(i,self.x,self.y,self.z)
            print(self.x,self.y,self.z,i)
        return np.min(self.x), np.min(self.y), np.min(self.z),np.max(self.x),np.max(self.y),np.max(self.z)


class label_fusion(object):

    def label_fusion_ants(slef,target_image, atlas_images, atlas_labels, output_label,mask='' ,rp=2, rs=3, alpha=0.1, beta=2,verbose = False,parallel = 8):
        """
        输入：atlas_images = ['001.nii.gz','002.nii.gz','003.nii.gz']
             atlas_labels = ['001label.nii.gz','002label.nii.gz','003label.nii.gz']
             targetimage = 'targetimage.nii.gz'

        You can control the number of threads by setting the environment
        variable ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS e.g. to use all or some
        of your CPUs.

        COMMAND:
             antsJointFusion
                  antsJointFusion is an image fusion algorithm developed by Hongzhi Wang and Paul
                  Yushkevich which won segmentation challenges at MICCAI 2012 and MICCAI 2013. The
                  original label fusion framework was extended to accommodate intensities by Brian
                  Avants. This implementation is based on Paul's original ITK-style implementation
                  and Brian's ANTsR implementation. References include 1) H. Wang, J. W. Suh, S.
                  Das, J. Pluta, C. Craige, P. Yushkevich, Multi-atlas segmentation with joint
                  label fusion IEEE Trans. on Pattern Analysis and Machine Intelligence, 35(3),
                  611-623, 2013. and 2) H. Wang and P. A. Yushkevich, Multi-atlas segmentation
                  with joint label fusion and corrective learning--an open source implementation,
                  Front. Neuroinform., 2013.

        OPTIONS:
             -d, --image-dimensionality 2/3/4
                  This option forces the image to be treated as a specified-dimensional image. If
                  not specified, the program tries to infer the dimensionality from the input
                  image.

             -t, --target-image targetImage
                                [targetImageModality0,targetImageModality1,...,targetImageModalityN]
                  The target image (or multimodal target images) assumed to be aligned to a common
                  image domain.

             -g, --atlas-image atlasImage
                               [atlasImageModality0,atlasImageModality1,...,atlasImageModalityN]
                  The atlas image (or multimodal atlas images) assumed to be aligned to a common
                  image domain.

             -l, --atlas-segmentation atlasSegmentation
                  The atlas segmentation images. For performing label fusion the number of
                  specified segmentations should be identical to the number of atlas image sets.

             -a, --alpha 0.1
                  Regularization term added to matrix Mx for calculating the inverse. Default =
                  0.1

             -b, --beta 2.0
                  Exponent for mapping intensity difference to the joint error. Default = 2.0

             -r, --retain-label-posterior-images (0)/1
                  Retain label posterior probability images. Requires atlas segmentations to be
                  specified. Default = false

             -f, --retain-atlas-voting-images (0)/1
                  Retain atlas voting images. Default = false

             -a, --constrain-nonnegative (0)/1
                  Constrain solution to non-negative weights.

             -p, --patch-radius 2
                                2x2x2
                  Patch radius for similarity measures. Default = 2x2x2

             -m, --patch-metric (PC)/MSQ
                  Metric to be used in determining the most similar neighborhood patch. Options
                  include Pearson's correlation (PC) and mean squares (MSQ). Default = PC (Pearson
                  correlation).

             -s, --search-radius 3
                                 3x3x3
                                 searchRadiusMap.nii.gz
                  Search radius for similarity measures. Default = 3x3x3. One can also specify an
                  image where the value at the voxel specifies the isotropic search radius at that
                  voxel.

             -e, --exclusion-image label[exclusionImage]
                  Specify an exclusion region for the given label.

             -x, --mask-image maskImageFilename
                  If a mask image is specified, fusion is only performed in the mask region.

             -o, --output labelFusionImage
                          intensityFusionImageFileNameFormat
                          [labelFusionImage,intensityFusionImageFileNameFormat,<labelPosteriorProbabilityImageFileNameFormat>,<atlasVotingWeightImageFileNameFormat>]
                  The output is the intensity and/or label fusion image. Additional optional
                  outputs include the label posterior probability images and the atlas voting
                  weight images.

             --version
                  Get version information.

             -v, --verbose (0)/1
                  Verbose output.

             -h
                  Print the help menu (short version).

             --help
                  Print the help menu.
        """
        dim = 3
        g = ' '.join(atlas_images)
        tg = target_image
        l = ' '.join(atlas_labels)
        print(mask)
        if mask:
            mask = '-x '+mask
        if verbose:
            verbose = '1'
        else:
            verbose = '0'
        parallel = '%s' % parallel
        cmd1 = 'export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS='+parallel
        cmd2 = 'antsJointFusion -d %s -g %s -t %s -l %s -a %g -b %g -p %d -s %d %s -o %s -v %s' % (dim, g, tg, l, alpha, beta, rp, rs, mask, output_label,verbose)
        os.system(cmd1)
        os.system(cmd2)

        return output_label