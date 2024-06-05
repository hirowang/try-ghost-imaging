<h1 align="center">
    A Ghost Imaging Demonstration System
</h1>
<p align="center">A Ghost Imaging Demonstration System for popular science purposes with Computer and Webcam. </p>
<p align="center">
    <img src="/images/demonstration.png" height="200">
    <img src="/images/screenshot.png" height="200">
    <img src="/images/result.jpg" height="200">
</p>
<p align="center">The equipment placement, system screenshots, and imaging results of the demonstration process.</p>


[Quantum Imaging (QI)](https://en.wikipedia.org/wiki/Quantum_imaging), also known as Ghost Imaging (GI), Correlated Imaging (CI), is an imaging method that utilizes second-order or higher-order correlations of light fields to obtain object information. Due to its imaging characteristics, quantum imaging technology has been applied in fields such as lithography, LiDAR, biological tissue imaging, and underwater imaging. The process of quantum imaging requires the use of professional instruments, which is not conducive to popular science popularization activities. This project is a science popularization system that only uses a personal computer and USB camera to demonstrate the quantum imaging process. The following are the steps to run this project.

## 1. Preparation

### Environment Preparation
Most of the required packages are in requirements.txt

You can prepare environments with the requirements.txt file in the repository directory.
```sh
pip install requirements.txt
```
### Equipment preparation

1. A computer to play speckle patterns and calculate results.

2. A USB [Webcam](https://en.wikipedia.org/wiki/Webcam) to simple.


## 2. Running the system

You can launch the graphical interface by running main.py

## 3. Conducting a demonstration

1. Click the adjustment button to adjust the camera position according to the display screen, so that the speckle pattern is exactly within the camera's shooting range.
2. Place objects that require imaging.
3. Set the number of samples and click the start button to start imaging.
4. The imaging results will be displayed on the page.
