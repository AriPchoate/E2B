# Creates matrices for vertices and faces to be used to generate a model
vertices = []
faces = []
objFp = "semmiSphere.obj"
with open(objFp, 'r') as fp:
    lines = fp.readlines()
    # Iterates through every line in the obj file
    for line in lines:
        # In an obj file vertices are indicated by a v at the start of the line
        if line[0] == "v":
            # Creates a new vertex in the vertex list
            vertices.append([])
            # String used to extract and concatonate each digit
            currentFloat = ""
            for i in range(2, len(line)):
                # Starts at the second index to skip unnecessary steps
                if line[i] == " " or line[i] == "\n":
                    # " " and "\n" indicate the end of a coordinate in a vertex\
                    # Adds the coordinate to the vertex created
                    vertices[-1].append(float(currentFloat))
                    # Resets the vertex
                    currentFloat = ""
                    continue

                currentFloat += line[i]
        
        # Faces are indicated by an f at the start of the line
        if line[0] == "f":
            faces.append([])
            length = len(line)
            # Starts at index 1 to skip unnecessary steps
            for i in range(1, length - 1):
                '''
                In an obj file face lines are more complicated as they account
                for vector normals and materials however it is easy to extract the vertex values
                The vertex value is the first number in this sequence a/b/c
                '''
                if line[i-1] == " ":
                    currentInt = ""
                    j = i
                    while True:
                        currentInt += line[j]
                        if line[j + 1] == "/" or j == "\n":
                            break
                        j += 1
                    faces[-1].append(int(currentInt))

with open("baseSphere.py", "w") as fp:
    fp.write("vertices = [\n")
    for vertex in vertices:
        fp.write(f"    {vertex},\n")
    fp.write("]\n\n")
    fp.write("faces = [\n")
    for face in faces:
        fp.write(f"    {face},\n")
    fp.write("]")