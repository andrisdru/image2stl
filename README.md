# image2stl image to STL converter for DLP printer PCB designing

In general this script converts PNG or other image to STL file, by defaul white color is converted as empty space.

1. Install python3 and its dependencies "pip3 install numpy-stl pillow argparse"
1. Export from easyeda PNG image with 2.5x size
2. run "python3 image2stl.py -i pcb.png -s 0.4" 

* scale 0.4 because 1/2.5 = 0.4
* if PCB traks are too fat use -f switch for offfseting pixels
* pcb.png example file is not created by me, somewhere found it on internet
* Follow those instructions
https://www.youtube.com/watch?v=-Qeq7ZgUOuE&t=34s
