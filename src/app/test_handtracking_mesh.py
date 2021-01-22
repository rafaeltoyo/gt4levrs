import cv2
import app.minimalhand.config as config
import open3d as o3d
import pygame
from app.minimalhand.capture import OpenCVCapture
from app.minimalhand.hand_mesh import HandMesh
from app.minimalhand.kinematics import mpii_to_mano
from transforms3d.axangles import axangle2mat
import numpy as np
from app.minimalhand.mano import plot_hand, plot_hand_3d
from app.minimalhand.utils import *
from app.minimalhand.utils import OneEuroFilter, imresize
from app.minimalhand.wrappers import ModelPipeline

def live_application(capture):
    """
    Launch an application that reads from a webcam and estimates hand pose at
    real-time.

    The captured hand must be the right hand, but will be flipped internally
    and rendered.

    Parameters
    ----------
    capture : object
      An object from `capture.py` to read capture stream from.
    """
    ############ output visualization ############
    view_mat = axangle2mat([1, 0, 0], np.pi)  # align different coordinate systems
    window_size = 1080

    hand_mesh = HandMesh(config.HAND_MESH_MODEL_PATH)
    mesh = o3d.geometry.TriangleMesh()
    mesh.triangles = o3d.utility.Vector3iVector(hand_mesh.faces)
    mesh.vertices = \
        o3d.utility.Vector3dVector(np.matmul(view_mat, hand_mesh.verts.T).T * 1000)
    mesh.compute_vertex_normals()

    viewer = o3d.visualization.Visualizer()
    viewer.create_window(
        width=window_size + 1, height=window_size + 1,
        window_name='Minimal Hand - output'
    )
    viewer.add_geometry(mesh)

    view_control = viewer.get_view_control()
    cam_params = view_control.convert_to_pinhole_camera_parameters()
    extrinsic = cam_params.extrinsic.copy()
    extrinsic[0:3, 3] = 0
    cam_params.extrinsic = extrinsic
    cam_params.intrinsic.set_intrinsics(
        window_size + 1, window_size + 1, config.CAM_FX, config.CAM_FY,
        window_size // 2, window_size // 2
    )
    view_control.convert_from_pinhole_camera_parameters(cam_params)
    view_control.set_constant_z_far(1000)

    render_option = viewer.get_render_option()
    render_option.load_from_json('./render_option.json')
    viewer.update_renderer()

    ############ input visualization ############
    pygame.init()
    display = pygame.display.set_mode((window_size, window_size))
    pygame.display.set_caption('Minimal Hand - input')

    ############ misc ############
    mesh_smoother = OneEuroFilter(4.0, 0.0)
    clock = pygame.time.Clock()
    model = ModelPipeline()

    while True:
        frame_large = capture.read()
        if frame_large is None:
            continue
        if frame_large.shape[0] > frame_large.shape[1]:
            margin = int((frame_large.shape[0] - frame_large.shape[1]) / 2)
            frame_large = frame_large[margin:-margin]
        else:
            margin = int((frame_large.shape[1] - frame_large.shape[0]) / 2)
            frame_large = frame_large[:, margin:-margin]

        frame_large = np.flip(frame_large, axis=1).copy()
        frame = imresize(frame_large, (128, 128))

        xyz, theta_mpii = model.process(frame)

        fixed_heatmap = (xyz * 1/2 + 1) * 200
        handimg = np.ones(shape=(300, 300, 3), dtype='uint8') * 255
        plot_hand(fixed_heatmap, None, handimg)
        cv2.imshow('heatmap', handimg)
        cv2.waitKey(50)

        theta_mano = mpii_to_mano(theta_mpii)

        v = hand_mesh.set_abs_quat(theta_mano)
        v *= 2  # for better visualization
        v = v * 1000 + np.array([0, 0, 400])
        v = mesh_smoother.process(v)

        mesh.triangles = o3d.utility.Vector3iVector(hand_mesh.faces)
        mesh.vertices = o3d.utility.Vector3dVector(np.matmul(view_mat, v.T).T)
        mesh.paint_uniform_color(config.HAND_COLOR)
        mesh.compute_triangle_normals()
        mesh.compute_vertex_normals()
        print(np.array(mesh.vertices))

        # for some version of open3d you may need `viewer.update_geometry(mesh)`
        viewer.update_geometry()

        viewer.poll_events()

        display.blit(
            pygame.surfarray.make_surface(np.transpose(imresize(frame_large, (window_size, window_size)), (1, 0, 2))
            ),
            (0, 0)
        )
        pygame.display.update()

        clock.tick(30)


if __name__ == '__main__':
    live_application(OpenCVCapture())