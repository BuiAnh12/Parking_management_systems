


# Computer Vision Application

## 1. Introduction

This document outlines the system pipeline for our computer vision application. The pipeline describes the data flow and processes from input to output, detailing each component and its function within the system.

## 2. Pipeline Overview

Our computer vision pipeline consists of the following main stages:

- Initialize streaming device
- Initialize application
- Submitting Jobs
- Detection
- Sending Email


## 3. Detailed Pipeline Stages


### 3.1 Initialize Streaming Device

In this project, we will create streaming from video using FFMPEG, which creates a real-time camera with an RTSP link to read that stream. To simplify the setup process, the stream will be converted into a UDP format, suitable for use in a Windows environment. This functionality will be handled in `device.py`.

### 3.2 Initialize Application

After setting up the streaming device, we need a frontend application to read the stream using `CV2` and process the video to display the time. The application is also responsible for object detection and submitting job actions. This functionality is implemented in `app/stream_app.py`.

### 3.3 Submitting Jobs

From the application tier, users can submit jobs to schedule detection at a specific date and time. The pre-processing logic will be handled in `app/stream_app.py`, which will pass data into a job manager located in `detection/scheduler.py`. This module will manage the jobs and call the detection process when it's time to execute.

### 3.4 Detection

The detection process is implemented in `detection/detection_handler.py`, which determines which detection method to use and draws bounding boxes after obtaining bounding box coordinates and metadata. 

To add more detection methods, ensure the new file is named `{detection_name}_detection.py`, update the `detection_mapping` inside `app/stream_app.py`, and ensure the output format is as follows:

## Example of bounding boxes and metadata
```
bounding_boxes = [
    [x1, y1, x2, y2],  # For example: [100, 50, 200, 150]
]

metadata = [
    {"label": "Person", "confidence": 0.95},
]
```
### 3.5 Sending Email

Once detection is complete, an email will be sent to the end user with the detection results. The application will use the first frame (picture) from the stream, process it for detection, and notify users if necessary.

## 4. Setup Instructions

To run the project:

1. Create a folder named `model` in the root directory.
2. Add the `yolov8m.pt` file into the `model` folder.
3. Create the `.env` file to the root and add EMAIL_APP_ACCOUNT and EMAIL_APP_PASSWORD
4. Install all required libraries by running:
   pip install -r requirements.txt
5. Run `device.py` to start the stream.
6. Finally, run `main.py` to start the application and enjoy!

### Note:
There is a known bug with the stream selection. If the stream does not pop up after selection, try selecting a different option to make it work.
Also, there is just human_detection is working other model handle will be updated later

## 5. Troubleshooting

- If you encounter issues with streaming:
  - Ensure that the FFMPEG installation is properly configured.
  - Check the UDP URL and make sure it is correctly formatted.

- For detection errors:
  - Verify that the model file (`yolov8m.pt`) is correctly placed in the `model` directory.
  - Ensure all required libraries are installed.
