from flask import Flask, render_template
import csv

app = Flask(__name__)
def read_attendance():
    attendance_data = []
    with open('Attendance.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 2:  # Ensure the row has exactly 2 items
                name, time = row[0], row[1]
                attendance_data.append({'name': name, 'time': time})
    return attendance_data

@app.route('/')
def attendance():
    data = read_attendance()
    return render_template('attendance.html', attendance_data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
