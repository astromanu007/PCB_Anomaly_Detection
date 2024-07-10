
# PCB Fault Detection Using Infrared Images and Camera

## Project Description
This project aims to detect faults on a printed circuit board (PCB) by using an infrared (IR) camera to capture thermal images. The system identifies overheated components on the PCB by applying image processing techniques and highlights these faulty components with colored rectangles.

## Components Needed
- **FLIR Lepton 3.5 Thermal Camera Module**
- **PureThermal 2 Board** (Interface board for the Lepton module)
- **Raspberry Pi** (Any model with USB interface, e.g., Raspberry Pi 4)
- **Python 3** installed on your Raspberry Pi
- **Dependencies**: OpenCV, NumPy, Lepton SDK

## Hardware Setup
1. Attach the FLIR Lepton 3.5 module to the PureThermal 2 board.
2. Connect the PureThermal 2 board to the Raspberry Pi via USB.

## Software Setup
### Step 1: Update and Install Dependencies
Open a terminal on your Raspberry Pi and run the following commands:

```bash
sudo apt-get update
sudo apt-get install cmake libjpeg-dev python3-pip
pip3 install opencv-python numpy
```

### Step 2: Install Lepton SDK
Clone the Lepton SDK repository and build it:

```bash
git clone https://github.com/groupgets/LeptonModule.git
cd LeptonModule/software/raspberrypi_libs/leptonSDKEmb32PUB
mkdir build
cd build
cmake ..
make
```

### Step 3: Clone the Project Repository
Clone the project repository from GitHub:

```bash
git clone https://github.com/astromanu007/PCB_Anomaly_Detection.git
cd PCB_Anomaly_Detection
```

### Step 4: Create the Python Script
Create a Python script (e.g., `pcb_fault_detection.py`) and paste the code:


## Running the Project
1. Ensure your hardware is correctly set up and connected.
2. Run the Python script:

```bash
python3 pcb_fault_detection.py
```

## Explanation
1. **capture_thermal_image**: Captures a thermal image using the Lepton camera.
2. **detect_overheated_component**: Detects overheated components by applying a threshold to the image.
3. **mark_faulty_components**: Converts the grayscale image to a BGR (color) image and draws red rectangles around the detected faulty components.
4. **main**: Orchestrates the image capture, processing, and display.

## Customization
- **Threshold Value**: Adjust the threshold value in the `main()` function to suit your specific needs and the thermal characteristics of your PCB.
- **Color of Rectangles**: Change the color of the rectangles in the `mark_faulty_components()` function by modifying the `(0, 0, 255)` tuple to another BGR color code.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements
- FLIR Systems for the Lepton camera module.
- OpenCV community for the image processing library.
- GroupGets for the Lepton SDK and hardware interface support.
- [PCB Anomaly Detection GitHub Repository](https://github.com/astromanu007/PCB_Anomaly_Detection) for additional resources and code examples.
