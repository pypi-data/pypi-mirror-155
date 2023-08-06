
# -*- coding: utf-8 -*-
"""
@author: zhaoliang
"""
import argparse

def test_parser():
    parser = argparse.ArgumentParser(description="synthetic data generation")
    parser.add_argument('--model_dir', type=str, required=True,
                        help='Continued training path')
    parser.add_argument('--fusion_method', required=True, type=str,
                        default='late',
                        help='late, early or intermediate')
    parser.add_argument('--show_vis', action='store_true',
                        help='whether to show image visualization result')
    parser.add_argument('--show_sequence', action='store_true',
                        help='whether to show video visualization result.'
                             'it can note be set true with show_vis together ')
    parser.add_argument('--save_vis', action='store_true',
                        help='whether to save visualization result')
    parser.add_argument('--save_npy', action='store_true',
                        help='whether to save prediction and gt result'
                             'in npy file')
    opt = parser.parse_args()
    return opt

if __name__ == '__main__':
    opt = test_parser()
    
    print('--model_dir:',opt.model_dir)
    print('--fusion_method:',opt.fusion_method)
    print('--show_vis:',opt.show_vis)
    print('--show_sequence:',opt.show_sequence)
    print('--save_vis:',opt.save_vis)
    print('--save_npy:',opt.save_npy)
    
    """
    python 3_test_parser.py --model_dir opencood/model_dir/model1/ --fusion_method intermediate
    
    --model_dir: opencood/model_dir/model1/
    --fusion_method: intermediate
    --show_vis: False
    --show_sequence: False
    --save_vis: False
    --save_npy: False

    """
    
    

