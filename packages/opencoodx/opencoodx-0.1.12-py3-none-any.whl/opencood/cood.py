import os
import argparse
from opencood.version import __version__

def test_parser():
    parser = argparse.ArgumentParser(description="opencood command")
    """
    parser.add_argument('--model_dir', type=str, required=True,
                        help='Continued training path')
    """
    parser.add_argument("-V","--version",action='store_true',
                        help="display version",
                    )
    parser.add_argument('--model', type=str,
                        default='None',
                        help="Your model name or use [all] to download all models at once")
    
    parser.add_argument('--yaml', action='store_true',
                        help='whether to download all yaml files')
    """
    parser.add_argument('--show_sequence', action='store_true',
                        help='whether to show video visualization result.'
                             'it can note be set true with show_vis together ')
    parser.add_argument('--save_vis', action='store_true',
                        help='whether to save visualization result')
    parser.add_argument('--save_npy', action='store_true',
                        help='whether to save prediction and gt result'
                             'in npy file')
    """
    opt = parser.parse_args()
    return opt

def main():
    opt = test_parser()
    
    # sitepath = site.getsitepackages() # a list 
    c_path = os.path.abspath(os.path.dirname(__file__)) # string
    print("Current Working Directory:" , os.getcwd())
    print(c_path)
    os.chdir(c_path)
    print("Current Working Directory After Change:" , os.getcwd()) 
    
    if opt.version:
        print("opencoodx version:",__version__)
        
    if opt.yaml:        
        # cmd = 'python ' + ab_path + '/hypes_yaml/download_yaml.py'
        cmd = 'python ' + c_path + '/hypes_yaml/download_yaml.py'
        os.system(cmd)
        print('Yaml files have been downloaded!')
    else:
        print('Reminder: You need to download yaml files before you run the code!')
    
    if opt.model == 'None':
        print('Reminder: You need to download trained model before you run the code!')
    else:
        cmd = 'python ' + c_path + '/model_dir/download_models.py --model ' + opt.model
        os.system(cmd)
        
if __name__ == '__main__':
    main()
    # path = os. getcwd()
    # c_path = os.path.abspath(os.path.dirname(__file__))
    # print(c_path)
    # os.chdir(c_path)
    # print("Current Working Directory " , os.getcwd()) 
 

    
    

    