import ants
import numpy as np
import time
import argparse


def dice(label_image_x_dirname, label_image_y_dirname):
	# 求出标签文件所有标签的dice

	image_x = ants.image_read(label_image_x_dirname).numpy()
	image_y = ants.image_read(label_image_y_dirname).numpy()

	# h = "变量1" if a>b else "变量2"

	max_num = np.max(image_x) if np.max(
	    image_x) > np.max(image_y) else np.max(image_y)

	max_num = np.int(max_num)

	# Dice 存放每个标签的dice值
	Dice = np.zeros(max_num+1)

	# 遍历每个标签
	for label in range(1, max_num+1):

		intersect = 0  # 交集像素个数
		total = 0  # 全部像素

		# 遍历图像
		a = np.sum(image_x==label)
		b = np.sum(image_y==label)

		c = np.sum( ((image_x - label)==0) & ( (image_y - label)==0) )

		if a+b != 0:
			Dice[label] = 2*c/(a+b)

		"""
		# 写入文件
		with open(dest_file, 'a+') as f:
			f.write('')
		"""

	return Dice


def parse_args():

    description = "计算两个标签文件的dice系数"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('filename', nargs=2, help="输入两个标签文件的文件名")

    args = parser.parse_args()
    return args


if __name__ == "__main__":

	print("——————————————开始运行————————————————")
	start = time.time()

	args = parse_args()
	[label_image1,label_image2]=args.filename
	
	DICE = dice(label_image1,label_image2)
	for i in range(0,len(DICE)):
		print("the dice of label %d is %g" % (i,DICE[i]))


	t = time.time() - start
	print('程序结束于 {:.0f}m {:.0f}s'.format(t // 60, t % 60))



