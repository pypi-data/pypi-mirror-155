# -*- coding: utf-8 -*-
# Author: Runsheng Xu <rxx3386@ucla.edu>
# License: TDG-Attribution-NonCommercial-NoDistrib


import os
import argparse
from torch.utils.data import DataLoader

from opencood.hypes_yaml.yaml_utils import load_yaml
from opencood.visualization import vis_utils
from opencood.data_utils.datasets.early_fusion_vis_dataset import \
    EarlyFusionVisDataset


def vis_parser():
    parser = argparse.ArgumentParser(description="data visualization")
    parser.add_argument('--data', type=str, default="test",
                        help='The dataset name that you want to visualize.')
    parser.add_argument('--color_mode', type=str, default="intensity",
                        help='lidar color rendering mode, e.g. intensity,'
                             'z-value or constant.')
    
    opt = parser.parse_args()
    return opt


if __name__ == '__main__':
    opt = vis_parser()
    
    working_path = os.getcwd()
    print("Current Working Directory:" , working_path)
    
    current_path = os.path.dirname(os.path.realpath(__file__))
    """
    print("Current file path:",current_path)
    upper_path = os.path.dirname(current_path)
    root_path = os.path.dirname(upper_path)
    print("root:",root_path)
    """
    params = load_yaml(os.path.join(current_path,
                                    '../hypes_yaml/visualization.yaml'))
    
    params['validate_dir'] = 'opv2v_data_dumping/' + opt.data
    
    params['root_dir'] = os.path.join(working_path,params['root_dir'])
    params['validate_dir'] = os.path.join(working_path,params['validate_dir'])

    print('params_visualize_dir:',params['validate_dir'])
    
    opencda_dataset = EarlyFusionVisDataset(params, visualize=True,
                                            train=False)
    data_loader = DataLoader(opencda_dataset, batch_size=1, num_workers=8,
                             collate_fn=opencda_dataset.collate_batch_train,
                             shuffle=False,
                             pin_memory=False)
    
    
    vis_utils.visualize_sequence_dataloader(data_loader,
                                            params['postprocess']['order'],
                                            color_mode=opt.color_mode)
    