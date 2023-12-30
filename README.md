# IMAGE AND VIDEO PROCESSING PROGRAM
#### Video Demo: [Youtube Link](https://youtu.be/cQlk5ukuXYE)
#### Files and Folder:
- `images`: This folder contains the image sequences for demonstration.
- `project.py`: The main python source code for the image processing and video generation program.
- `test_project.py`: A python test file for testing functions used in  `project.py`.
- `requirement.txt`: A text file containing the libraries used in this project.

#### Description:
The program is subdivided into **two** categories:
1. Image Processing
1. Video Generation

##### Image Processing Section
This part of the program takes in an image file with a valid format and apply the following operations on it:
- Rotation
- Blur
- Contrast
- Brightness
- Sharpness
- Cropping
- Saturation
- Flipping

In `project.py`, the image processing uses the **pillow** and **argparse** library: 
```python
from PIL import ImageEnhance
def process_img(args, img):
    if args.brightness:
        img = ImageEnhance.Brightness(img)
        img = img.enhance(args.brightness)
    ...
    return img
```

#### Video Generation
This section uses OpenVC to create a single video file with the valid format from an image sequence.  
These sequences are processed by the image processing section to apply any effect and later used by OpenCV to generate the video with a specified frame rate. The program is sampled with `images` folder for demonstration.  
In `project.py`, the following function handles the video generation
```python
def create_video(args):
    # Uses the process_img(args, img) to apply various effects
    ...
```

#### Libraries and utilities
- Argparse: this third-party library was used to parse the command-line arguments from the user.
Type `python project.py --help` to show how to input the right arguments in their right format.
- Pillow (PIL): this third-party library was used to open, show and apply effects on image file.
- OpenCV: this third-party library was used to generate and show video output of valid format. 
- Numpy: this third-party library was used to transfrom Pillow image to OpenCV matrix.
- sys: This built-in python library was used to access the system directories to generate file or folder paths, test if path is a file or folder, get the extension of a file path and to create directory.

