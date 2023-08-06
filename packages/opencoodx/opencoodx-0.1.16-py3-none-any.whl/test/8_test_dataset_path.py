
# -*- coding: utf-8 -*-
"""
@author: zhaoliang
"""

import os
if __name__ == '__main__':
    if not os.path.exists('./opv2v_data_dumping'):
        os.mkdir('./opv2v_data_dumping')
    else:
        print('yes')
