import ants
import numpy as np
import argparse


def volume(label_image): 
	# 计算标签文件中各个标签的体积

	image = ants.image_read(label_image).numpy()
	max_num = np.int(np.max(image))

	Volume = np.zeros(max_num+1)
	
	for label in range(1, max_num+1):

		Volume[label] = np.sum(image == label)
	
	
	[x,y,z] = ants.get_spacing(ants.from_numpy(image))
	voxel_volume = x*y*z

	return Volume * voxel_volume


def parse_args():

    description = "计算标签文件的体积"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('filename', help="输入标签文件的文件名")

    args = parser.parse_args()
    return args


if __name__ == "__main__":

	args = parse_args()
	filename = args.filename

	Volume = volume(filename)
	str = filename.split("/")

	print("-----------%s 的各个组织的体积(单位 mm³)----------------------------\n\n" % str[-1])

	for i in range(0,len(Volume)):
		print("the volume of label %d is %g" % (i,Volume[i]))
