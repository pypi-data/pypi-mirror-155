
# -*- coding: utf-8 -*-
"""
@author: zhaoliang
"""
import time

import cv2
import numpy as np
import open3d as o3d
import matplotlib
import matplotlib.pyplot as plt

from matplotlib import cm

def visualize_pcd(name):
    pcd = o3d.io.read_point_cloud(name)
    print(pcd)
    print(np.asarray(pcd.points))
    o3d.visualization.draw_geometries([pcd])
if __name__ == '__main__':
    try:
        vis = o3d.visualization.Visualizer()
        vis.create_window()
    
        vis.get_render_option().background_color = [0.05, 0.05, 0.05]
        vis.get_render_option().point_size = 1.0
        vis.get_render_option().show_coordinate_frame = True
    
        # used to visualize lidar points
        vis_pcd = o3d.geometry.PointCloud()
        
        pcd = vis.io.read_point_cloud("/lidar_data/000070.pcd")
        
        vis.add_geometry(pcd)
        vis.update_geometry(pcd)
        vis.poll_events()
        vis.update_renderer()
    except KeyboardInterrupt:
        print('finish')
        

