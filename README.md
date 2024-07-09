
# Face Attendance System

Using OpenCV and Flask, I have built this Face Attendance System which detects and recognizes a face along with a barcode on a video capture and marks it's attendance.


## Demo
![WhatsApp Image 2024-07-09 at 12 37 52 AM](https://github.com/Bhuvan588/Face-Attendance-System/assets/68458621/29954546-aebc-4a02-86a4-f666a751edd8)
![WhatsApp Image 2024-07-09 at 12 38 59 AM](https://github.com/Bhuvan588/Face-Attendance-System/assets/68458621/e47107a1-1248-45fc-95e9-8a941a8af262)


## Project Need

Why did I think of making this? Well our college's ID card contains out photo and a barcode which on decoding gives our college roll number. So we could use this system in order to take automatic attendance
## Installation

1. Clone the project into your required folder

2. The photos folder contains the images of students whose attendance you want to track.

3. If you change the student pics, make sure to do the same for face encodings in the main.py folder

4. Open terminal. Run python main.py and show the image as in the above example and the attendance will be stored in a newly created CSV file
    
## Libraries and Tools Used

- OpenCV - Computer Vision Library
- Pyzbar - Used to detect and decode barcodes
- Flask - Used for routing
- Face-recognition - Library to store face encodings and to compare faces

## Note:
- Make sure to generate a custom barcode for your use from various online sites.
- Make sure that the face and barcode are shown to the camera at the same time
- It may not detect barcodes easily so try to adjust the barcode
