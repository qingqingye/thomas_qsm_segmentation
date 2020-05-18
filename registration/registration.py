import ants
##将 3min向pre配准。1.获取文件路径；2.读取数据，数据格式为 ants.core.ants_image.ANTsImage；3.进行配准，方法为Affine；4.保存配准结果。 
fix_path =  't1atlas.nii.gz'   #'pre.nii.gz'  
move_path1 =  'NC_02_Sub028_restore_brain_flipped.nii.gz'
move_path2 = 'NC_02_Sub035_restore_brain_flipped.nii.gz'   #move
save_path1 = 't1atlas_028.nii.gz'
save_path2 = 't1atlas_035.nii.gz'
fix_img = ants.image_read(fix_path)
move_img1 = ants.image_read(move_path1)
move_img2 = ants.image_read(move_path2)
print("start registration")
outs = ants.registration(fix_img,move_img1,type_of_transforme = 'Affine')  
reg_img = outs['warpedmovout']  
print("start save1")
ants.image_write(reg_img,save_path1)


outs = ants.registration(fix_img,move_img2,type_of_transforme = 'Affine')  
reg_img = outs['warpedmovout']  
print("start save2")
ants.image_write(reg_img,save_path2)