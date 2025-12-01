from pygame import mixer
import cv2
import os
import face_recognition
from DBConnection import Db
from PIL import Image
import datetime
import numpy as np
import sys,time
#--------------------------
# Constants
STATIC_PATH = r"C:\Users\athul\PycharmProjects\SecureZone\SecureZone_app\static\\"
db = Db()
def play_alert_sound():
    mixer.init()
    mixer.music.load(STATIC_PATH + 'attack2t22wav-14511.mp3')
    mixer.music.play()
    time.sleep(5)
    mixer.music.stop()
# Initialize webcam
cam = cv2.VideoCapture(0)#, cv2.CAP_DSHOW)
if not cam.isOpened():#
    print("Error: Could not access the webcam.")
    exit()


try:
    identified = []  # List to keep track of already identified students
    attendance_marked = set()  # Set to track students for whom attendance has been marked

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to capture frame. Exiting...")
            break

        print("Processing frame...")
        temp_image_path = os.path.join(STATIC_PATH, "captured_frame.jpg")
        cv2.imwrite(temp_image_path, frame)

        # Query all registered students
        securityperson = db.select("SELECT * FROM securezone_app_securityperson")
        if not securityperson:
            print("No students registered in the database.")
            break

        known_faces = []
        user_ids = []
        person_names = []

        for sp in securityperson:
            if sp["id"] in attendance_marked:  # Skip students who already have attendance marked
                continue

            pic = sp["image"]
            img_path = os.path.join(STATIC_PATH, os.path.basename(pic))

            if os.path.exists(img_path):
                student_image = np.array(Image.open(img_path))
                encodings = face_recognition.face_encodings(student_image)

                if encodings:
                    known_faces.append(encodings[0])
                    user_ids.append(sp["id"])
                    person_names.append(sp["security_name"])
                else:
                    print(f"Warning: No face encodings found for {sp['sname']}.")
            else:
                print(f"Error: Image not found for {sp['security_name']} at {img_path}.")

        captured_image = np.array(Image.open(temp_image_path))
        unknown_encodings = face_recognition.face_encodings(captured_image)
        t = 0

        if unknown_encodings:
            detected_valid_face = False  # Flag to track if a registered face is found

            for unknown_encoding in unknown_encodings:
                matches = face_recognition.compare_faces(known_faces, unknown_encoding, tolerance=0.45)
                if True in matches:
                    matched_idx = matches.index(True)
                else:
                    t = t+1

            if t > 0:
                play_alert_sound()
                print("Unregistered face detected..")

        else:
            print("No faces detected in the current frame. Adjust the camera angle or lighting.")

        print("Finished processing frame. Waiting for the next one...")

finally:
    cam.release()
    cv2.destroyAllWindows()
    print("Resources released.")
