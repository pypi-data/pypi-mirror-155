# -*- coding: utf-8 -*-
# Author: Runsheng Xu <rxx3386@ucla.edu>, Hao Xiang <haxiang@g.ucla.edu>,
# License: TDG-Attribution-NonCommercial-NoDistrib


import argparse
import os
import time

import torch
import open3d as o3d
from torch.utils.data import DataLoader
from easydict import EasyDict

import opencood.hypes_yaml.yaml_utils as yaml_utils
from opencood.tools import train_utils, inference_utils
from opencood.data_utils.datasets import build_dataset
from opencood.utils import eval_utils
from opencood.visualization import vis_utils
from opencood.utils import common_utils

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
    
    opt.show_vis = False
    opt.show_sequence = False
    opt.save_vis = False
    opt.save_npy = False        
    return opt

def mymodel(backbone='pointpillar',fusion_method='intermediate',pretrained='af'):
    
    opt = model_map(backbone,fusion_method,pretrained)

    hypes = yaml_utils.load_yaml(None, opt)

    print('Creating Model')
    model = train_utils.create_model(hypes)
    print('Model created')
    
    if torch.cuda.is_available():
        print('activate cuda')
        model.cuda()

    print('Loading Model from checkpoint')
    
    saved_path = opt.model_dir
    _, model = train_utils.load_saved_model(saved_path, model)
    model.eval()   
    print('Model load from checkpoint finished')
    
    return model,opt,hypes

def main_old(backbone,fusion_method,pretrained):
    
    opt = model_map(backbone,fusion_method,pretrained)

    assert opt.fusion_method in ['late', 'early', 'intermediate']
    assert not (opt.show_vis and opt.show_sequence), 'you can only visualize ' \
                                                    'the results in single ' \
                                                    'image mode or video mode'

    hypes = yaml_utils.load_yaml(None, opt)

    print('Dataset Building')
    opencood_dataset = build_dataset(hypes, visualize=True, train=False)
    data_loader = DataLoader(opencood_dataset,
                             batch_size=1,
                             num_workers=4,
                             collate_fn=opencood_dataset.collate_batch_test,
                             shuffle=False,
                             pin_memory=False,
                             drop_last=False)

    print('Creating Model')
    model = train_utils.create_model(hypes)
    # we assume gpu is necessary
    if torch.cuda.is_available():
        model.cuda()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    print('Loading Model from checkpoint')
    saved_path = opt.model_dir
    _, model = train_utils.load_saved_model(saved_path, model)
    model.eval()

    # Create the dictionary for evaluation
    result_stat = {0.3: {'tp': [], 'fp': [], 'gt': 0},
                   0.5: {'tp': [], 'fp': [], 'gt': 0},
                   0.7: {'tp': [], 'fp': [], 'gt': 0}}

    if opt.show_sequence:
        vis = o3d.visualization.Visualizer()
        vis.create_window()

        vis.get_render_option().background_color = [0.05, 0.05, 0.05]
        vis.get_render_option().point_size = 1.0
        vis.get_render_option().show_coordinate_frame = True

        # used to visualize lidar points
        vis_pcd = o3d.geometry.PointCloud()
        # used to visualize object bounding box, maximum 50
        vis_aabbs_gt = []
        vis_aabbs_pred = []
        for _ in range(50):
            vis_aabbs_gt.append(o3d.geometry.LineSet())
            vis_aabbs_pred.append(o3d.geometry.LineSet())

    for i, batch_data in enumerate(data_loader):
        print(i)
        with torch.no_grad():
            batch_data = train_utils.to_device(batch_data, device)
            if opt.fusion_method == 'late':
                pred_box_tensor, pred_score, gt_box_tensor = \
                    inference_utils.inference_late_fusion(batch_data,
                                                          model,
                                                          opencood_dataset)
            elif opt.fusion_method == 'early':
                pred_box_tensor, pred_score, gt_box_tensor = \
                    inference_utils.inference_early_fusion(batch_data,
                                                           model,
                                                           opencood_dataset)
            elif opt.fusion_method == 'intermediate':
                pred_box_tensor, pred_score, gt_box_tensor = \
                    inference_utils.inference_intermediate_fusion(batch_data,
                                                                  model,
                                                                  opencood_dataset)
                print("pred_box_tensor:",pred_box_tensor)
                print("pred_score:", pred_score)
                print("gt_box_tensor:", gt_box_tensor)
            else:
                raise NotImplementedError('Only early, late and intermediate'
                                          'fusion is supported.')

            eval_utils.caluclate_tp_fp(pred_box_tensor,
                                       pred_score,
                                       gt_box_tensor,
                                       result_stat,
                                       0.3)
            eval_utils.caluclate_tp_fp(pred_box_tensor,
                                       pred_score,
                                       gt_box_tensor,
                                       result_stat,
                                       0.5)
            eval_utils.caluclate_tp_fp(pred_box_tensor,
                                       pred_score,
                                       gt_box_tensor,
                                       result_stat,
                                       0.7)
            if opt.save_npy:
                npy_save_path = os.path.join(opt.model_dir, 'npy')
                if not os.path.exists(npy_save_path):
                    os.makedirs(npy_save_path)
                inference_utils.save_prediction_gt(pred_box_tensor,
                                                   gt_box_tensor,
                                                   batch_data['ego'][
                                                       'origin_lidar'][0],
                                                   i,
                                                   npy_save_path)

            if opt.show_vis or opt.save_vis:
                vis_save_path = ''
                if opt.save_vis:
                    vis_save_path = os.path.join(opt.model_dir, 'vis')
                    if not os.path.exists(vis_save_path):
                        os.makedirs(vis_save_path)
                    vis_save_path = os.path.join(vis_save_path, '%05d.png' % i)

                opencood_dataset.visualize_result(pred_box_tensor,
                                                  gt_box_tensor,
                                                  batch_data['ego'][
                                                      'origin_lidar'][0],
                                                  opt.show_vis,
                                                  vis_save_path,
                                                  dataset=opencood_dataset)

            if opt.show_sequence:
                pcd, pred_o3d_box, gt_o3d_box = \
                    vis_utils.visualize_inference_sample_dataloader(
                        pred_box_tensor,
                        gt_box_tensor,
                        batch_data['ego']['origin_lidar'][0],
                        vis_pcd,
                        mode='constant'
                        )
                if i == 0:
                    vis.add_geometry(pcd)
                    vis_utils.linset_assign_list(vis,
                                                 vis_aabbs_pred,
                                                 pred_o3d_box,
                                                 update_mode='add')

                    vis_utils.linset_assign_list(vis,
                                                 vis_aabbs_gt,
                                                 gt_o3d_box,
                                                 update_mode='add')

                vis_utils.linset_assign_list(vis,
                                             vis_aabbs_pred,
                                             pred_o3d_box)
                vis_utils.linset_assign_list(vis,
                                             vis_aabbs_gt,
                                             gt_o3d_box)
                vis.update_geometry(pcd)
                vis.poll_events()
                vis.update_renderer()
                time.sleep(0.001)

    eval_utils.eval_final_results(result_stat,
                                  opt.model_dir)
    if opt.show_sequence:
        vis.destroy_window()


def tensor_to_numpy(det_boxes, det_score, gt_boxes):
    if det_boxes is not None:
        # convert bounding boxes to numpy array
        det_boxes = common_utils.torch_tensor_to_numpy(det_boxes)
        det_score = common_utils.torch_tensor_to_numpy(det_score)
        gt_boxes = common_utils.torch_tensor_to_numpy(gt_boxes)

    else:
        det_boxes = []
        det_score = []
        gt_boxes = []
    return det_boxes, det_score, gt_boxes


def main_new(backbone, fusion_method, pretrained):

    model,opt,hypes = mymodel(backbone, fusion_method, pretrained)

    assert opt.fusion_method in ['late', 'early', 'intermediate']
    assert not (opt.show_vis and opt.show_sequence), 'you can only visualize ' \
                                                     'the results in single ' \
                                                     'image mode or video mode'

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    print('Dataset Building')
    opencood_dataset = build_dataset(hypes, visualize=True, train=False)
    data_loader = DataLoader(opencood_dataset,
                             batch_size=1,
                             num_workers=4,
                             collate_fn=opencood_dataset.collate_batch_test,
                             shuffle=False,
                             pin_memory=False,
                             drop_last=False)

    # Create the dictionary for evaluation
    result_stat = {0.3: {'tp': [], 'fp': [], 'gt': 0},
                   0.5: {'tp': [], 'fp': [], 'gt': 0},
                   0.7: {'tp': [], 'fp': [], 'gt': 0}}

    for i, batch_data in enumerate(data_loader):
        print(i)
        with torch.no_grad():
            batch_data = train_utils.to_device(batch_data, device)
            if opt.fusion_method == 'late':
                pred_box_tensor, pred_score, gt_box_tensor = \
                    inference_utils.inference_late_fusion(batch_data,
                                                          model,
                                                          opencood_dataset)
            elif opt.fusion_method == 'early':
                pred_box_tensor, pred_score, gt_box_tensor = \
                    inference_utils.inference_early_fusion(batch_data,
                                                           model,
                                                           opencood_dataset)
            elif opt.fusion_method == 'intermediate':
                pred_box_tensor, pred_score, gt_box_tensor = \
                    inference_utils.inference_intermediate_fusion(batch_data,
                                                                  model,
                                                                  opencood_dataset)
                """
                print("pred_box_tensor:", pred_box_tensor)
                print("pred_score:", pred_score)
                print("gt_box_tensor:", gt_box_tensor)
                """
            else:
                raise NotImplementedError('Only early, late and intermediate'
                                          'fusion is supported.')

            det_boxes, det_score, gt_boxes = tensor_to_numpy(pred_box_tensor, pred_score, gt_box_tensor)

            print("pred_box:", det_boxes)
            print("pred_score:", det_score)
            print("gt_box_tensor:", gt_boxes)
            """
            
            eval_utils.caluclate_tp_fp(pred_box_tensor,
                                       pred_score,
                                       gt_box_tensor,
                                       result_stat,
                                       0.3)
            eval_utils.caluclate_tp_fp(pred_box_tensor,
                                       pred_score,
                                       gt_box_tensor,
                                       result_stat,
                                       0.5)
            eval_utils.caluclate_tp_fp(pred_box_tensor,
                                       pred_score,
                                       gt_box_tensor,
                                       result_stat,
                                       0.7)
            """
    """
    eval_utils.eval_final_results(result_stat,
                                  opt.model_dir)
    """


def load_dataset(hypes):
    print('Dataset Building')
    opencood_dataset = build_dataset(hypes, visualize=True, train=False)
    data_loader = DataLoader(opencood_dataset,
                             batch_size=1,
                             num_workers=4,
                             collate_fn=opencood_dataset.collate_batch_test,
                             shuffle=False,
                             pin_memory=False,
                             drop_last=False)
    return opencood_dataset,data_loader

def model_pred(opt,model,batch_data,opencood_dataset):

    if opt.fusion_method == 'late':
        pred_box_tensor, pred_score, gt_box_tensor = \
            inference_utils.inference_late_fusion(batch_data,
                                                  model,
                                                  opencood_dataset)
    elif opt.fusion_method == 'early':
        pred_box_tensor, pred_score, gt_box_tensor = \
            inference_utils.inference_early_fusion(batch_data,
                                                   model,
                                                   opencood_dataset)
    elif opt.fusion_method == 'intermediate':
        pred_box_tensor, pred_score, gt_box_tensor = \
            inference_utils.inference_intermediate_fusion(batch_data,
                                                          model,
                                                          opencood_dataset)
        """
        print("pred_box_tensor:", pred_box_tensor)
        print("pred_score:", pred_score)
        print("gt_box_tensor:", gt_box_tensor)
        """
    else:
        raise NotImplementedError('Only early, late and intermediate'
                                  'fusion is supported.')
    return pred_box_tensor, pred_score, gt_box_tensor

def main_new1(backbone, fusion_method, pretrained):
    model, opt, hypes = mymodel(backbone, fusion_method, pretrained)

    assert opt.fusion_method in ['late', 'early', 'intermediate']
    assert not (opt.show_vis and opt.show_sequence), 'you can only visualize ' \
                                                     'the results in single ' \
                                                     'image mode or video mode'

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    opencood_dataset,data_loader = load_dataset(hypes)

    for i, batch_data in enumerate(data_loader):
        print(i)
        with torch.no_grad():
            batch_data = train_utils.to_device(batch_data, device)
            pred_box_tensor, pred_score, gt_box_tensor = model_pred(opt, model, batch_data, opencood_dataset)
            det_boxes, det_score, gt_boxes = tensor_to_numpy(pred_box_tensor, pred_score, gt_box_tensor)
            """
            print("pred_box:", det_boxes)
            print("pred_score:", det_score)
            print("gt_box_tensor:", gt_boxes)
            """

if __name__ == '__main__':
    backbone = 'pointpillar'
    fusion_method = 'intermediate' # 'early' #
    pretrained = 'af' # 'v2v' # require test_culver_city data
    main_new1(backbone,fusion_method,pretrained)
