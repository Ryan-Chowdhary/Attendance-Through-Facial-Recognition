import cv2
from datetime import datetime
from simple_facerec import SimpleFacerec
from time import sleep
from freshest_camera_frame import FreshestFrame

cap = cv2.VideoCapture('rtsp://admin:admin@192.168.16.142:1935')
if not cap.isOpened():
    print('cam not connected')
    exit()

sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

new_cap = FreshestFrame(cap)

def markAttendance(name):
    with open('Attendance.csv') as f:
        mydatalist = f.readlines()
        namelist = []
        
        # Extract names from the current CSV file
        for line in mydatalist:
            entry = line.strip().split(',')
            namelist.append(entry[0])
        
        # Add name if it is not already in the CSV file
        if name not in namelist:
            now = datetime.now()
            dtstring = now.strftime('%H:%M:%S')
            f.write(f'{name},{dtstring}\n')
            print(f'Attendance marked for {name} at {dtstring}')
        else:
            print(f'{name} is already marked.')

def rec_face():
    while True:
        ret, frame = new_cap.read()
        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x1, y2, x2 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            cv2.rectangle(frame, (x1,y1), (x2, y2), (0, 0, 200), 2)
            cv2.putText(frame, name, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0,0,200), 1, cv2.LINE_AA)
            markAttendance(face_names)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break



rec_face()
cap.release()
cv2.destroyAllWindows()
