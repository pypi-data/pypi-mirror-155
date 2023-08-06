
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 11:37:22 2022

@author: zhaoliang
"""

import opencood.hypes_yaml.yaml_utils as yaml_utils
from opencood.tools.model import model_map
import numpy as np

if __name__ == '__main__':
    backbone = 'pointpillar'
    fusion_method = 'intermediate' # 'early' #
    pretrained = 'af' # 'v2v' # require test_culver_city data
    
    opt = model_map(backbone,fusion_method,pretrained)

    hypes = yaml_utils.load_yaml(None, opt)
    
    np.save('opencood/hypes_yaml/hypes.npy',hypes)