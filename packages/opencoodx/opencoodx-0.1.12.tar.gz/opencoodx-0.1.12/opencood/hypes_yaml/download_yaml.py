import os
from opencood.utils.common_utils import download_googledrive_zipmodel_gdown

if __name__ == '__main__':
    yaml_googledrive_url = 'https://drive.google.com/uc?export=download&id=1yVaBbTU16b1oyi1DfCVT6wvMu31Ydnv4' 
    
    print('Getting into download_yaml.py')
    c_path = os.path.abspath(os.path.dirname(__file__)) # string
    print("Current Working Directory:" , os.getcwd())
    print(c_path)
    os.chdir(c_path)
    print("Current Working Directory After Change:" , os.getcwd()) 
    
    filePath = './yamlfiles.zip'
    download_googledrive_zipmodel_gdown(yaml_googledrive_url,filePath,remove_zip=True)