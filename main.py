import cv2
from datetime import datetime
from simple_facerec import SimpleFacerec
from time import sleep
from freshest_camera_frame import FreshestFrame

# Recticle corner coords
# [Top-left, Bottom-left, Top-right, Bottom-right, thickness]
rect = [(),(),(),(),]
Draw_recticle = False # PLEASE SET TO FALSE IF NO RECTICLE IS REQUIRED


cap = cv2.VideoCapture('rtsp://admin:admin@192.168.16.142:1935')
if not cap.isOpened():
    print('cam not connected')
    exit()

sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

new_cap = FreshestFrame(cap)

def markAttendance(name):
    now = datetime.now()
    tdate = now.date()
    date = f'{date.day}-{date.month}-{date.year}'
    with open(f'AttendanceRecords/attendance_{date}.csv', 'r+') as f:
        mydatalist = f.readlines()
        namelist = []
        
        # Extract names from the current CSV file
        for line in mydatalist:
            entry = line.strip().split(',')
            namelist.append(entry[0])
        
        # Add name if it is not already in the CSV file
        if name not in namelist:
            dtstring = now.strftime('%H:%M:%S')
            f.write(f'{name},{dtstring}\n')
            print(f'Attendance marked for {name} at {dtstring}')

def rec_face():
    while True:
        ret, frame = new_cap.read()
        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x1, y2, x2 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            # check if the match crosses a certain threshold
            # execute only if threshold is met
            if name[1] > 0.6: # threshold is set at 0.6 for now
                # Draw a rectangle around the face
                (w, h), _ = cv2.getTextSize(name[0] + ':' + name[1], cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                cv2.rectangle(frame, (x1,y1-20), (x2 + w, y2), (0, 0, 200), 2)
                # Write the name of the face at the bottom of the rectangle
                cv2.putText(frame, f'{(name[0].split('_'))[0]}:{name[1]}', (x1, y1-5), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0,0,200), 1, cv2.LINE_AA)
                markAttendance(face_names)
            else:
                (w, h), _ = cv2.getTextSize("unknown"+ ':' + name[1], cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                cv2.rectangle(frame, (x1,y1-20), (x2 + w, y2), (0, 0, 200), 2)
                cv2.putText(frame, f'unknown:{name[1]}', (x1, y1-5), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0,0,200), 1, cv2.LINE_AA)
        if Draw_recticle:
            # Draw a square recticle around the centre of frame
            cv2.line(frame, rect[0], rect[1], (100,0,100), rect[4]) # top-left corner
            cv2.line(frame, rect[1], rect[3], (100, 0, 100), rect[4]) # bottom-left
            cv2.line(frame, rect[3], rect[2], (100, 0, 100), rect[4]) # top-right
            cv2.line(frame, rect[2], rect[0], (100, 0, 100), rect [4]) # bottom-right
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break



rec_face()
cap.release()
cv2.destroyAllWindows()
