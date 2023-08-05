import os
import argparse

def test_parser():
    parser = argparse.ArgumentParser(description="opencood command")
    """
    parser.add_argument('--model_dir', type=str, required=True,
                        help='Continued training path')
    """
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
    
    if opt.yaml:
        cmd = 'python opencood/hypes_yaml/download_yaml.py'
        os.system(cmd)
        print('Yaml files have been downloaded!')
    
    if opt.model == 'None':
        print('Warning: You need to download trained model before you run the code!')
    else:
        cmd = 'python opencood/model_dir/download_models.py --model ' + opt.model
        os.system(cmd)
        
if __name__ == '__main__':
    main()

    
    