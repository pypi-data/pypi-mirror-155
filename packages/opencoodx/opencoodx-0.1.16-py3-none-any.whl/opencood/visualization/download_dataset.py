# -*- coding: utf-8 -*-
"""
@author: zhaoliang
"""

import argparse
import os
from opencood.utils.common_utils import download_googledrive_zipmodel_gdown

def test_parser():
    parser = argparse.ArgumentParser(description="download offline data")
    parser.add_argument('--data', type=str,
                        default='None',
                        help="Specify your offline dataset name")
    opt = parser.parse_args()
    return opt

def gurl_dataset():
    
    gurl0 = 'https://drive.google.com/uc?export=download&id=1qB-dDX7jn628ZxxoLs7fDRyGXhOZ2Bze'
    dname0 = 'test_dataset'
    
    gurl1 = 'https://drive.google.com/uc?export=download&id=1vcpou7kpDwOTKMTRNHAwXCwihpcCO8l6'
    dname1 = 'test_culver_city'
    
    gurl2 = 'https://drive.google.com/uc?export=download&id=1fuYK-oNA0FpZtT8rUiEETOCNmtO3FCfS'
    dname2 = 'test'
    
    gurl3 = 'https://drive.google.com/uc?export=download&id=1M4pG-fdPs-EWMLZpc1yl-bqUcJ6yg4zz'
    dname3 = 'validate'
    
    gurl4 = 'https://drive.google.com/uc?export=download&id=1DbBOURvIuV7E9_g4FpKwUGNJiIG_5Eeg'
    dname4 = 'train'
    
    gurls = [gurl0,gurl1,gurl2,gurl3,gurl4]
    dnames = [dname0,dname1,dname2,dname3,dname4]
    
    return gurls,dnames 

def download_one_dataset(dataset_name,gurls,dnames):
    if dataset_name in dnames:
        myindex = dnames.index(dataset_name)
        gurl = gurls[myindex]
        dname = dnames[myindex]
        
        download_googledrive_zipmodel_gdown(gurl,'./opv2v_data_dumping/' + dname + '.zip',remove_zip=True)
    else:
        raise Warning('Your specified dataset is not in the dataset list, please double-check your dataset name!')
    
if __name__ == '__main__':
    opt = test_parser()
    
    gurls,dnames = gurl_dataset()
    
    print('Getting into download_dataset.py')
    
    print('=============================== Warning ===============================')
    print('This process may take a long time.')
    print('Please be patient and do not close the windows before download finish!')
    print('=============================== Warning ===============================')
    
    if not os.path.exists('./opv2v_data_dumping'):
        os.mkdir('./opv2v_data_dumping')
        download_flag = True
        print('Yes mkdir')
    
    path = './opv2v_data_dumping/'+ opt.data
    if not os.path.exists(path):
        print('INFO: No dataset path exist.')
        download_flag = True
    else:
        download_flag = False
    
    if download_flag:
        print('INFO: Download begin')        
        download_one_dataset(opt.data,gurls,dnames)
    else:
        print('Warning: Current specified data is already existed! No need to download')

