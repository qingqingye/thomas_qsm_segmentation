import os
def label_fusion_ants(target_image, atlas_images, atlas_labels, output_label,mask='' ,rp=2, rs=3, alpha=0.1, beta=2,verbose = False,parallel = 8):
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