'''
2/18
Reflection:
After we finished the code for generating an image of the Braille from english text. We started on 
building the website for generating the braille and along that generating the 3D files with it. Though
We originally plan on producing an STL file using some of the libraries we looked at, we eventually 
landed on creating a obj file through the modelGenerator code. This is the actual 3D file, but to also
also create a preview of the 3D file, leo wei allowed us to use his code called modelImageGen, which renders a scence
of the braille file with lighting. Different Images used on the website are stored in a photo called 
static, which can be accessed through running the app.py code, which runs a website through the different
templates of HTML in the templates folder. We made sure to include an abouts page, a direction page, and
as well as a tranlate page. The finalized website is called E2B, or English to Braille. The user can input
a string of English text, which is translated to a braille list consisting information of the "dots" on
the braille. This image is then used to generate 2D images of the braille, 3D models for dowload, and an 
preview image of the 3D model that is renedered. The user can also specify the dimensions of the braille 
created. 

Ari Aureliano Joe
Sources: 
Description of Obj file: https://people.computing.clemson.edu/~dhouse/courses/405/docs/brief-obj-file-format.html
Comparison of Obj file with STL: https://www.sculpteo.com/en/glossary/obj-file-3d-printing-file-format/#:~:text=Yes%20you%20can%203D%20print,the%20colors%20of%20the%20object.
OMH
'''

from PIL import Image
from dataclasses import dataclass

# TEMPORARY SNIPPET OF CODE ---------------
# unoptimized and bad way of extracting bump locations because we pack and unpack the image for data
# Image analysis
fgColor = (255, 255, 255)
bgColor = (39, 42, 46)
scale = 1
# File path to the image of braille generated by ImageGen.py
def parseImage(p):
    bumpList = []
    brailleFilePath = "./Website/static/images/BrailleImage.png"
    brailleImg = Image.open(brailleFilePath)
    brailleSize = (int(brailleImg.size[0] / scale), int(brailleImg.size[1] / scale))
    # Used to to set the size of the baseplate and temporarily 
    for x in range(brailleSize[0]):
        for y in range(brailleSize[1]):
            # iterates through every pixel
            try:
                # If the pixel is the top left corner of a braille bump
                # up of it and left of it would be grey
                # down of it and right of it would be white
                if brailleImg.getpixel((x - 1, y)) == bgColor and brailleImg.getpixel((x, y - 1)) == bgColor and brailleImg.getpixel((x +1, y)) == fgColor and brailleImg.getpixel((x, y + 1)) == fgColor:
                    bumpList.append((int(x/scale), int(y/scale))) #adds to bump list
            except IndexError:
                continue #if the index is out of range it just skips the pixel
    p.plateWidth = brailleSize[0]
    p.plateLength = brailleSize[1]
    return bumpList
# ------------------------------------------

# dataclass of user preferences to customize their 3d model
@dataclass
class Preferences:
    plateWidth : float
    plateLength : float
    plateHeight : float
    brailleHeight : float
    brailleScale : float
p = Preferences(0, 0, 1, 30, 2)

modelFilePath = "./Website/static/model.obj"

# Gives the base vertices and faces for a simple 3d cube -----
# Used to create more rectangular prisms. The vertices are just scaled and shifted according to its origin and scale
rectFaces = [
    (1, 5, 7, 3),
    (4, 3, 7, 8),
    (8, 7, 5, 6),
    (6, 2, 4, 8),
    (2, 1, 3, 4),
    (6, 5, 1, 2)
]
rectVertices = [
    (1, 1, 0),
    (1, 0, 0),
    (1, 1, 1),
    (1, 0, 1),
    (0, 1, 0),
    (0, 0, 0),
    (0, 1, 1),
    (0, 0, 1)
]
# -------------------------------------------------------------
def createRectPrism(origin, scale, faces, vertices):
    # Needs the current amount of vertices so it can write the face data correctly
    # See this link: https://people.computing.clemson.edu/~dhouse/courses/405/docs/brief-obj-file-format.html
    vertexNum = len(vertices)
    for rectVertex in rectVertices:
        # Iterates through every vertice of the base cube 
        newVertex = [] # Empty vertex to apply adjustments to each (X, Z, Y) coordinate
        for i in range(3):
            # newVertex is the old vertex but scaled and shifted
            newVertex.append((rectVertex[i] * scale[i]) + origin[i])
        # Adds the new adjusted vertex to the vertice list
        vertices.append(newVertex) 
    
    # No adjustments need to be made to the face unlike the vertices
    # See 
    for face in rectFaces:
        # Iterates through base cube faces
        newFace = []
        for vertex in face:
            # Only adjustment needed is to update the vertex with the current amount of vertices so their is no vertex overlap
            newFace.append(vertex + vertexNum)
        faces.append(newFace)

def generateModel(filePath, vertices, faces):
    # Opens model path
    with open(filePath, 'w') as fp:
        # Write vertices
        for vertex in vertices:
            fp.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")

        fp.write("\n")
        # Write faces (vertex indices)
        for face in faces:
            fp.write("f ")
            fp.write(" ".join(str(index) for index in face))
            fp.write("\n")

def generateBraille():
    bumps = parseImage(p)
    faces = []
    vertices = []
    # Creates baseplate
    createRectPrism((0, 0, 0), (p.plateWidth, p.plateHeight, p.plateLength), faces, vertices)
    # Iterates through every bump and creates a rectangular prism for it based on user preferences
    for bump in bumps:
        createRectPrism((bump[0], p.plateHeight, bump[1]), (p.brailleScale, p.brailleHeight, p.brailleScale), faces, vertices)

    generateModel(modelFilePath, vertices, faces)