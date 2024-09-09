from read_write_model import read_model
import open3d as o3d
import numpy as np

cameras_bin = "..kitti_test/mapper/0/cameras.bin"
images_bin = ".kitti_test/mapper/0/images.bin"
points3D_bin = ".kitti_test/mapper/0/cpoints3D.bin"

path = "/home/mrwang/3dgs/kitti_test/exhaustive_matcher/mapper/2/"
path =  "/home/mrwang/3dgs/kitti_test/sequential_matcher/mapper/1"
cameras, images, points3D = read_model(path)

# print("cameras keys: ", cameras.keys())
# for cameras_key in cameras.keys():
#     print(cameras[cameras_key])


# print("images keys: ", images.keys())
# for images_key in images.keys():
#     # print(images[images_key])
#     print(images[images_key].name)

print(len(points3D.keys()))
points = []
rgbs = []
for points3D_key in points3D.keys():
    # print(points3D[points3D_key].xyz)
    # print(points3D[points3D_key].rgb)
    xyz = points3D[points3D_key].xyz
    rgb = points3D[points3D_key].rgb
    points.append(xyz)
    rgbs.append(rgb)
    

    # print(points3D[points3D_key].id)
    # print(points3D[points3D_key].image_ids)

    # if len(rgbs) > 100:
    #     continue
print("--xyz_np--")
xyz_np = np.array(points)
print("--rgbs_np--")
rgbs_np = np.array(rgbs)
print("--shape--")
print(xyz_np.shape, rgbs_np.shape)


fuse_pcds_o3d = o3d.geometry.PointCloud()
fuse_pcds_o3d.points = o3d.utility.Vector3dVector(xyz_np)
fuse_pcds_o3d.colors = o3d.utility.Vector3dVector(rgbs_np/255)
o3d.visualization.draw_geometries([fuse_pcds_o3d])