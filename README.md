# image2stl

Image to STL converter for DLP pcb designing. In general this script converts PNG or other image to STL file, by defaul white color is converted as empty space.

1. Install python3 and its dependencies "pip3 install numpy-stl pillow argparse"
1. Export from easyeda PNG image with 2.5x size
2. run "python3 image2stl.py -i export.png -s 0.4" 
scale 0.4 because 1/2.5 = 0.4

Follow those instructions
https://www.youtube.com/watch?v=-Qeq7ZgUOuE&t=34s
