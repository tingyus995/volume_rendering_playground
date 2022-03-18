# Volume Rendering Playground

This app displays 3D volumetric data from [this site](https://web.cs.ucdavis.edu/~okreylos/PhDStudies/Spring2000/ECS277/DataSets.html) using OpenGL.

## Dependencies
* [Python 3](https://www.python.org/)
* [glfw](https://pypi.org/project/glfw/)
* [PyOpenGL](https://pypi.org/project/PyOpenGL/)
* [PyGLM](https://pypi.org/project/PyGLM/)
* [numpy](https://pypi.org/project/numpy/)
* [imgui](https://github.com/pyimgui/pyimgui)

## Deployment

### Install dependencies
```
pip install glfw
pip install PyOpenGL PyOpenGL_accelerate
pip install PyGLM
pip install numpy
pip install imgui[glfw]
```
### Run the renderer
1. Download and extract the skull volume file from [here](https://web.cs.ucdavis.edu/~okreylos/PhDStudies/Spring2000/ECS277/Skull.vol.gz) into the project directory.
2. Run
```
python renderer.py
```
