#pip3 install numpy-stl pillow argparse
import argparse
import numpy as np
from stl import mesh
from PIL import Image


parser = argparse.ArgumentParser(description='Converts image to STL for SLA Printers for PCB design')

parser.add_argument("-s", "--scale", type=float, default=1, help="Scale, Size * Scale")
parser.add_argument("-o", "--output", type=str, default='output.stl', help="output STL")
parser.add_argument("-x", "--maxx", type=int, default=1440, help="Max X vertices")
parser.add_argument("-y", "--maxy", type=int, default=2560, help="Max Y vertices")
parser.add_argument("-f", "--offset", type=int, default=0, help="Offset for lines")
parser.add_argument("-c", "--color", type=int, default=255, help="Color threshold, image is converted to greyscale where 0 white 255 black")
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument("-i", "--input",required=True ,type=str, help="Input png, jpg, gif...")
args = parser.parse_args()
z=10 #height # set default height
img = Image.open(args.input)
offset = args.offset
max_size=(args.maxx,args.maxy)
color=args.color #0 white / 255 black


grey_img = img.convert('L') #convert to 8bit (0-255) greyscale
grey_img.thumbnail(max_size)
imageNp = np.array(grey_img)
(ncols,nrows)=grey_img.size

def colored(pixel):
  if pixel < color:
    return True
  else:
    return False


# setting offset basically making lines thinner 
for i in range(offset):
  for x in range(1, ncols-1):
    for y in range(1, nrows-1): 
      if colored(imageNp[y][x]):
       if colored(imageNp[y-1][x]) and not colored(imageNp[y+1][x]): 
          imageNp[y][x] = 255

for i in range(offset):
  for x in range(ncols-1, 1, -1):
    for y in range(nrows-1, 1, -1):
      if colored(imageNp[y][x]):
        if colored(imageNp[y+1][x]) and not colored(imageNp[y-1][x]): 
          imageNp[y][x] = 255


for i in range(offset):
  for x in range(1, ncols-1):
    for y in range(1, nrows-1): 
      if colored(imageNp[y][x]):
       if colored(imageNp[y][x-1]) and not colored(imageNp[y][x+1]): 
          imageNp[y][x] = 255

for i in range(offset):
  for x in range(ncols-1, 1, -1):
    for y in range(nrows-1, 1, -1):
      if colored(imageNp[y][x]):
        if colored(imageNp[y][x+1]) and not colored(imageNp[y][x-1]): 
          imageNp[y][x] = 255



vertices=[]

for x in range(0, ncols-1):
  for y in range(0, nrows-1):  
    if colored(imageNp[y][x]):
      u = True if not colored(imageNp[y][x+1])  else False 
      r = True if not colored(imageNp[y+1][x])  else False
      d = True if not colored(imageNp[y][x-1])  else False
      l = True if not colored(imageNp[y-1][x])  else False
      vertice=np.array([x, y, 0, u, r, d, l])
      vertices.append(vertice)


faces=[]
for i in range(0, np.shape(vertices)[0]):
    vertice = vertices[i]
    #print(vertice)
    vertice3 = (vertice[0],vertice[1],  vertice[2])
    vertice2 = (vertice[0]+1,vertice[1],vertice[2])
    vertice1 = (vertice[0],vertice[1]+1,vertice[2])
    face1 = np.array([vertice1,vertice2,vertice3])
    #print(face1)
    faces.append(face1)
    
    vertice1 = (vertice[0]+1,vertice[1]+1,vertice[2])
    vertice2 = (vertice[0]+1,vertice[1],  vertice[2])
    vertice3 = (vertice[0],vertice[1]+1,  vertice[2])
    face2 = np.array([vertice1,vertice2,vertice3])
    faces.append(face2)
      
    #print(vertice)
    vertice1 = (vertice[0],vertice[1],  vertice[2]+z)
    vertice2 = (vertice[0]+1,vertice[1],vertice[2]+z)
    vertice3 = (vertice[0],vertice[1]+1,vertice[2]+z)
    face3 = np.array([vertice1,vertice2,vertice3])
   #print(face1)
    faces.append(face3)
    
    vertice3 = (vertice[0]+1,vertice[1]+1,vertice[2]+z)
    vertice2 = (vertice[0]+1,vertice[1],  vertice[2]+z)
    vertice1 = (vertice[0],vertice[1]+1,  vertice[2]+z)
    face4 = np.array([vertice1,vertice2,vertice3])
    faces.append(face4)
    
    if vertice[3]==1:
        vertice3=(vertice[0]+1,vertice[1]+1,vertice[2])
        vertice2=(vertice[0]+1,vertice[1],vertice[2])
        vertice1=(vertice[0]+1,vertice[1]+1,vertice[2]+z)
        faceu = np.array([vertice1,vertice2,vertice3])
        faces.append(faceu)
       
        vertice1=(vertice[0]+1,vertice[1]+1,vertice[2]+z)
        vertice2=(vertice[0]+1,vertice[1],vertice[2]+z)
        vertice3=(vertice[0]+1,vertice[1],vertice[2])
        faceu = np.array([vertice1,vertice2,vertice3])
        faces.append(faceu)
  
    if vertice[4]==1:
        vertice3=(vertice[0],vertice[1]+1,vertice[2])
        vertice2=(vertice[0]+1,vertice[1]+1,vertice[2])
        vertice1=(vertice[0],vertice[1]+1,vertice[2]+z)
        faceu = np.array([vertice1,vertice2,vertice3])
        faces.append(faceu)
        
        vertice1=(vertice[0],vertice[1]+1,vertice[2]+z)
        vertice2=(vertice[0]+1,vertice[1]+1,vertice[2]+z)
        vertice3=(vertice[0]+1,vertice[1]+1,vertice[2])
        faceu = np.array([vertice1,vertice2,vertice3])
        faces.append(faceu)     
     
    if vertice[5]==1:
        vertice3=(vertice[0],vertice[1],vertice[2])
        vertice2=(vertice[0],vertice[1]+1,vertice[2])
        vertice1=(vertice[0],vertice[1]+1,vertice[2]+z)
        faceu = np.array([vertice1,vertice2,vertice3])
        faces.append(faceu)
        
        vertice1=(vertice[0],vertice[1],vertice[2]+z)
        vertice2=(vertice[0],vertice[1]+1,vertice[2]+z)
        vertice3=(vertice[0],vertice[1],vertice[2])
        faceu = np.array([vertice1,vertice2,vertice3])
        faces.append(faceu)
        
    if vertice[6]==1:
        vertice1=(vertice[0],vertice[1],vertice[2])
        vertice2=(vertice[0]+1,vertice[1],vertice[2])
        vertice3=(vertice[0],vertice[1],vertice[2]+z)
        faceu = np.array([vertice1,vertice2,vertice3])
        faces.append(faceu)
        
        vertice3=(vertice[0],vertice[1],vertice[2]+z)
        vertice2=(vertice[0]+1,vertice[1],vertice[2]+z)
        vertice1=(vertice[0]+1,vertice[1],vertice[2])
        faceu = np.array([vertice1,vertice2,vertice3])
        faces.append(faceu)  
   

print(f"number of faces: {len(faces)}")
facesNp = np.array(faces)
# Create the mesh
surface = mesh.Mesh(np.zeros(facesNp.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
  for j in range(3):
     surface.vectors[i][j]=facesNp[i][j] * args.scale / 4

surface.remove_duplicate_polygons
surface.remove_empty_areas    
surface.save(args.output)
print("done")


