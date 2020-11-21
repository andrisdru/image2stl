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
parser.add_argument("-c", "--color", type=int, default=255, help="Max Y vertices")
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument("-i", "--input",required=True ,type=str, help="Input png, jpg, gif...")

args = parser.parse_args()
#------------------------inputs---------------
img = Image.open(args.input)
max_size=(args.maxx,args.maxy)
color=args.color #0 white / 255 black
z=10 #height
#-----------------------------------------------
grey_img = img.convert('L') #convert to 8bit (0-255) greyscale
grey_img.thumbnail(max_size)
imageNp = np.array(grey_img)
(ncols,nrows)=grey_img.size


vertices=[]

for x in range(0, ncols-1):
  for y in range(0, nrows-1):  
    if imageNp[y][x] < color:
      u = True if imageNp[y][x+1] >= color  else False 
      r = True if imageNp[y+1][x] >= color  else False
      d = True if imageNp[y][x-1] >= color  else False
      l = True if imageNp[y-1][x] >= color  else False
      vertice=np.array([x, y, 0, u, r, d, l])
      vertices.append(vertice)


faces=[]
for i in range(0, np.shape(vertices)[0]):
    vertice = vertices[i]
    #print(vertice)
    vertice1 = (vertice[0],vertice[1],  vertice[2])
    vertice2 = (vertice[0]+1,vertice[1],vertice[2])
    vertice3 = (vertice[0],vertice[1]+1,vertice[2])
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
    
    vertice1 = (vertice[0]+1,vertice[1]+1,vertice[2]+z)
    vertice2 = (vertice[0]+1,vertice[1],  vertice[2]+z)
    vertice3 = (vertice[0],vertice[1]+1,  vertice[2]+z)
    face4 = np.array([vertice1,vertice2,vertice3])
    faces.append(face4)
    
    if vertice[3]==1:
        vertice1=(vertice[0]+1,vertice[1]+1,vertice[2])
        vertice2=(vertice[0]+1,vertice[1],vertice[2])
        vertice3=(vertice[0]+1,vertice[1]+1,vertice[2]+z)
        faceu = np.array([vertice1,vertice2,vertice3])
        faces.append(faceu)
       
        vertice1=(vertice[0]+1,vertice[1]+1,vertice[2]+z)
        vertice2=(vertice[0]+1,vertice[1],vertice[2]+z)
        vertice3=(vertice[0]+1,vertice[1],vertice[2])
        faceu = np.array([vertice1,vertice2,vertice3])
        faces.append(faceu)
  
    if vertice[4]==1:
        vertice1=(vertice[0],vertice[1]+1,vertice[2])
        vertice2=(vertice[0]+1,vertice[1]+1,vertice[2])
        vertice3=(vertice[0],vertice[1]+1,vertice[2]+z)
        faceu = np.array([vertice1,vertice2,vertice3])
        faces.append(faceu)
        
        vertice1=(vertice[0],vertice[1]+1,vertice[2]+z)
        vertice2=(vertice[0]+1,vertice[1]+1,vertice[2]+z)
        vertice3=(vertice[0]+1,vertice[1]+1,vertice[2])
        faceu = np.array([vertice1,vertice2,vertice3])
        faces.append(faceu)     
     
    if vertice[5]==1:
        vertice1=(vertice[0],vertice[1],vertice[2])
        vertice2=(vertice[0],vertice[1]+1,vertice[2])
        vertice3=(vertice[0],vertice[1]+1,vertice[2]+z)
        faceu = np.array([vertice1,vertice2,vertice3])
        faces.append(faceu)
        
        vertice1=(vertice[0],vertice[1],vertice[2]+z)
        vertice2=(vertice[0],vertice[1]+1,vertice[2]+z)
        vertice3=(vertice[0],vertice[1],vertice[2])
        faceu = np.array([vertice1,vertice2,vertice3])
        faces.append(faceu)
        
    if vertice[6]==1:
        vertice1=(vertice[0],vertice[1],vertice[2]+z)
        vertice2=(vertice[0]+1,vertice[1],vertice[2]+z)
        vertice3=(vertice[0]+1,vertice[1],vertice[2])
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


