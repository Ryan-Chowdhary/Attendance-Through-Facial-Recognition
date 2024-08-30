from datetime import datetime

def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
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

markAttendance("Kishlay")
