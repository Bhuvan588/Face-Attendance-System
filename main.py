from flask import Flask, render_template, Response, request
import face_recognition
import numpy as np
import cv2
import csv
from datetime import datetime
from pyzbar.pyzbar import decode

app = Flask(__name__)
video_capture = cv2.VideoCapture(0)

# Store face encodings
kohli_image = face_recognition.load_image_file("photos/virat.jpeg")
kohli_encoding = face_recognition.face_encodings(kohli_image)[0]

rohit_image = face_recognition.load_image_file("photos/rohit.jpeg")
rohit_encoding = face_recognition.face_encodings(rohit_image)[0]

bumrah_image = face_recognition.load_image_file("photos/Bumrah.jpeg")
bumrah_encoding = face_recognition.face_encodings(bumrah_image)[0]



known_face_encodings = [kohli_encoding, rohit_encoding, bumrah_encoding]
known_face_names = ["Virat", "Rohit", "Bumrah"]

students = known_face_names.copy()
entries = {}

face_locations = []
face_encodings = []
face_names = []
recording = False

def gen_frames():
    global recording
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    filename = current_date + '.csv'
    
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        if recording:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []

            for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distance)

                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

                # Drawing a face
                cv2.rectangle(frame, (left*4, top*4), (right*4, bottom*4), (0, 0, 255), 2)
                cv2.rectangle(frame, (left*4, bottom*4 - 35), (right*4, bottom*4), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left * 4 + 6, bottom * 4 - 6), font, 1.0, (255, 255, 255), 1)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Barcode part
            barcodes = decode(gray)
            person_usn = ""

            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")
                barcode_type = barcode.type

                # Get the coordinates of the barcode
                (x, y, w, h) = barcode.rect

                # Draw a rectangle around the barcode
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, f"Barcode: {barcode_data}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                person_usn = barcode_data

            if person_usn and any(name in known_face_names for name in face_names):
                current_time = datetime.now().strftime("%H:%M:%S")
                student_name = next(name for name in face_names if name in known_face_names)

                # Check for anomalies
                if person_usn in entries and entries[person_usn] != student_name:
                    print(f"Anomaly detected: {person_usn} already exists for a different person.")
                elif student_name in entries.values() and any(key != person_usn for key, value in entries.items() if value == student_name):
                    print(f"Anomaly detected: {student_name} has used a different person_usn.")
                else:
                    # No anomaly present
                    with open(filename, 'a', newline='') as f:
                        lnwriter = csv.writer(f)
                        lnwriter.writerow([student_name, person_usn, current_time])
                        entries[person_usn] = student_name
                        print("Written to csv: ", student_name, person_usn)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_recording', methods=['POST'])
def start_recording():
    global recording
    recording = True
    return "Recording started"

@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    global recording
    recording = False
    return "Recording stopped"

if __name__ == "__main__":
    app.run(debug=True)
