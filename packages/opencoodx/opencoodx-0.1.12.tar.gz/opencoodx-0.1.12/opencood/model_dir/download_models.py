import argparse
import os
from opencood.utils.common_utils import download_googledrive_zipmodel_gdown

def test_parser():
    parser = argparse.ArgumentParser(description="parameters of downloading models")
    parser.add_argument('--model', required=True, type=str,
                        default='None',
                        help="Your model name or use [all] to download all models at once")
    opt = parser.parse_args()
    return opt

def gurl_names():
    gurl1 = 'https://drive.google.com/uc?export=download&id=1p8JbMtd4ClvgOMlsgqDzhE5Xf-JIrDJa'
    mname1 = 'pointpillar_attentive_fusion'
    
    gurl2 = 'https://drive.google.com/uc?export=download&id=1DXmPX61Ij9M-rqCnTN8pGmpvQzawRynS'
    mname2 = 'pointpillar_early_fusion'
    
    gurl3 = 'https://drive.google.com/uc?export=download&id=12XnKie7eeQPDsrJFf-lX5rnOzM2up01h'
    mname3 = 'pointpillar_fcooper'
    
    gurl4 = 'https://drive.google.com/uc?export=download&id=14oKDS8gQZFX1D2YUlyELYUd36mkITBWS'
    mname4 = 'pointpillar_late_fusion'
    
    gurl5 = 'https://drive.google.com/uc?export=download&id=1GUcnFknFAlxF_SAKwKC05u_PeuBHwpHO'
    mname5 = 'v2vnet'
    
    gurl6 = 'https://drive.google.com/uc?export=download&id=1VTXfpXzmdgjrqGx7N427PhZRQikcm-P0'
    mname6 = 'voxelnet_early_fusion'
    
    gurl7 = 'https://drive.google.com/uc?export=download&id=13GaArq37WHv9vqp8oSIPRQx4ckF9WS65'
    mname7 = 'voxelnet_attentive_fusion'
    
    gurl8 = 'https://drive.google.com/uc?export=download&id=13eKXp4i3ecDMyzWdhutp3CsQeLMwlnJz'
    mname8 = 'second_early_fusion'
    
    gurl9 = 'https://drive.google.com/uc?export=download&id=1_kL56M-VzBa0gEWjJpLEjpKtwciPa9X_'
    mname9 = 'second_attentive_fusion'
    
    gurl10 = 'https://drive.google.com/uc?export=download&id=18dddhjShLrZjVm1mQH1vqbkG0-5W_8IV'
    mname10 = 'second_late_fusion'
    
    gurl11 = 'https://drive.google.com/uc?export=download&id=1slhZL21hcnmdyICf1jo_P3ydJRhhVhGd'
    mname11 = 'pixor_early_fusion'
    
    gurls = [gurl1,gurl2,gurl3,gurl4,gurl5,gurl6,gurl7,gurl8,gurl9,gurl10,gurl11]
    mnames = [mname1,mname2,mname3,mname4,mname5,mname6,mname7,mname8,mname9,mname10,mname11]
    
    return gurls,mnames    

def download_all_models(gurls,mnames):
    
    for i in range(len(gurls)):
        gurl = gurls[i]
        mname = mnames[i]
        download_googledrive_zipmodel_gdown(gurl,'./' + mname + '.zip',remove_zip=True)

def download_one_model(target_model_name,gurls,mnames):
    
    if target_model_name in mnames:
        myindex = mnames.index(target_model_name)
        gurl = gurls[myindex]
        mname = mnames[myindex]
        
        download_googledrive_zipmodel_gdown(gurl,'./' + mname + '.zip',remove_zip=True) 
    else:
        raise Warning('Your specified model is not in the model list, please double-check your model name!')
        
if __name__ == '__main__':
    opt = test_parser()
    
    gurls,mnames = gurl_names()
    
    print('Getting into download_models.py')
    c_path = os.path.abspath(os.path.dirname(__file__)) # string
    print("Current Working Directory:" , os.getcwd())
    print(c_path)
    os.chdir(c_path)
    print("Current Working Directory After Change:" , os.getcwd()) 
        
    if opt.model== 'all':
        download_all_models(gurls,mnames)
    elif opt.model== 'None':
        raise Warning("Please specify your model! Using --model arguments")
    else:
        download_one_model(opt.model,gurls,mnames)

