import ants
import numpy as np
import time
import argparse
from lib import *

diceTool = dice()
basicTool = tool()
target_num = 0
label_list = basicTool.make_dir_list('data/Label')
diceTool.cal('fusion_result.nii.gz', label_list[target_num])

