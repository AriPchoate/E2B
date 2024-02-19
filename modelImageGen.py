# ALL OF THIS IS the "brightest programmer leo wei['s]" (as he requested to be cited) CODE
# The picture from 3d obj file is leo's code
# Adjustments were made to fit our braille project

import trimesh
import pyrender
from PIL import Image
import numpy as np

def getSize():
    brailleFilePath = "./Website/static/images/BrailleImage.png"
    brailleImg = Image.open(brailleFilePath)
    brailleSize = (int(brailleImg.size[0] / 2), int(brailleImg.size[1] / 2))
    return brailleSize

def normalize(vector):
    vector = np.array(vector)
    return vector / np.linalg.norm(vector)

def camera_matrix(right_degrees, up_degrees,pos):
    # convert degrees to radians
    right_radians = np.radians(right_degrees)
    up_radians = np.radians(up_degrees)

    # create rotation matrices for right and up rotations
    rotation_right = np.array([
        [np.cos(right_radians), 0, -np.sin(right_radians)],
        [0, 1, 0],
        [np.sin(right_radians), 0, np.cos(right_radians)]
    ])

    rotation_up = np.array([
        [1, 0, 0],
        [0, np.cos(up_radians), -np.sin(up_radians)],
        [0, np.sin(up_radians), np.cos(up_radians)]
    ])

    # combine the rotation matrices
    combined_rotation = np.dot(rotation_right, rotation_up)

    full_matrix = np.zeros((4,4))
    full_matrix[:3, :3] = combined_rotation
    full_matrix[0, 3] = pos[0]
    full_matrix[1, 3] = pos[1]
    full_matrix[2, 3] = pos[2]
    full_matrix[3, :] = [0,0,0,1]

    return full_matrix

def main():
    imgSize = getSize()
    # load ur obj file
    loaded = trimesh.load('./Website/static/model.obj')

    # check if the loaded object is a scene and if so get the mesh
    if isinstance(loaded, trimesh.Scene):
        mesh = trimesh.util.concatenate([mesh for mesh in loaded.geometry.values()])
    else:
        mesh = loaded

    # mesh is a Trimesh object which can be converted to a pyrender mesh
    mesh = pyrender.Mesh.from_trimesh(mesh)


    scene = pyrender.Scene(bg_color=(35+5, 37+5, 41+5), ambient_light=50)
    scene.add(mesh)
    # setup camera, lighting, etc., like before
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0, aspectRatio=1.0)

    

    # this is what u wanna experiment w/
    # so the first two values are like the rotations of the camera
    # so like the first one is how much you want to look to the right in degrees, or to the left if its negative ig
    # the second value is how much u wanna look up
    # the third is the camera position
    camera_pose = camera_matrix(0,-70, [imgSize[0]/2, 7*sum(imgSize)/8, imgSize[1] +10])

    scene.add(camera, pose=camera_pose)

    # oh yea the lighting is rlly simple but experiment with intensity
    light = pyrender.PointLight(color=((255, 200, 200)), intensity=50000.0)

    scene.add(light, pose=camera_matrix(0, 0, [imgSize[0] / 2, 100, imgSize[1] / 2]))
    scene.add(light, pose=camera_matrix(0, 0, [imgSize[0], 70, imgSize[1] / 2]))
    scene.add(light, pose=camera_matrix(0, 0, [0, 70, imgSize[1] / 2]))

    # render the scene
    r = pyrender.OffscreenRenderer(640, 480)
    color, _ = r.render(scene)

    img = Image.fromarray(color, 'RGB')
    # img.show()
    img.save("./Website/static/images/modelImage.png")