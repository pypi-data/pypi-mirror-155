import site
from opencood.utils.common_utils import download_googledrive_zipmodel_gdown

if __name__ == '__main__':
    yaml_googledrive_url = 'https://drive.google.com/uc?export=download&id=1yVaBbTU16b1oyi1DfCVT6wvMu31Ydnv4' 
    sitepath = site.getsitepackages()
    filePath = sitepath[0] + '/opencood/hypes_yaml/yamlfiles.zip'
    download_googledrive_zipmodel_gdown(yaml_googledrive_url,filePath,remove_zip=True)