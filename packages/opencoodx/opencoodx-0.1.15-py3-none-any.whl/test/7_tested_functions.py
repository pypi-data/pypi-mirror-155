
# -*- coding: utf-8 -*-
"""
@author: zhaoliang
"""

from easydict import EasyDict

def model_map(backbone,fusion_method,pretrained=None):
    """
    This function is to map the backbone method and fusion strategy with 
    corresponding model directory

    Parameters
    ----------
    backbone : string
        DESCRIPTION.
    fusion_method : string
        DESCRIPTION.
    pretrained: string
        pretrained model name: 'af' or 'fc' or 'v2v' or NOne
    Returns
    -------
    opt : TYPE
        DESCRIPTION.

    """
    
    opt = EasyDict()
    
    opt.fusion_method = fusion_method
    
    assert opt.fusion_method in ['late', 'early', 'intermediate']
    
    if opt.fusion_method == 'intermediate':
        if backbone == 'pointpillar':
            if pretrained == 'af': # 'attentive fusion'
                opt.model_dir = 'opencood/model_dir/pointpillar_attentive_fusion/'
            elif pretrained == 'fc': #f-cooper
                opt.model_dir = 'opencood/model_dir/pointpillar_fcooper/'
            elif pretrained == 'v2v':
                opt.model_dir = 'opencood/model_dir/v2vnet/'
            else:
                print('Warning: pretrained model is not specified!')
        if backbone == 'voxelnet':
            opt.model_dir = 'opencood/model_dir/voxelnet_attentive_fusion/'
        
    if opt.fusion_method == 'early':
        if backbone == 'pointpillar':
            opt.model_dir = 'opencood/model_dir/pointpillar_early_fusion/'
        if backbone == 'voxelnet':
            opt.model_dir = 'opencood/model_dir/voxelnet_early_fusion/'
            
    return opt
