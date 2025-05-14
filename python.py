from flask import Flask, render_template
import serial
import time

app = Flask(__name__)

# Set up the serial line
ser = serial.Serial('/dev/ttyACM0', 9600)  # Change '/dev/ttyACM0' to your serial port
time.sleep(2)

def get_temp_comment(temp_str):
    try:
        temp = float(temp_str)
        if temp < 10:
            return "It's quite cold. Bundle up!"
        elif 10 <= temp < 20:
            return "A bit chilly — a light jacket might be good."
        elif 20 <= temp < 30:
            return "Nice and warm!"
        else:
            return "It's hot! Stay cool and hydrated."
    except:
        return "Temperature data unavailable."

# Read and record the data
def get_temp_data():
    ser.flushInput()
    try:
        ser_bytes = ser.readline()
        decoded_bytes = ser_bytes.decode("utf-8").strip()  # Assuming the Arduino prints the temperature followed by newline
        # Assuming the Arduino Serial prints something like "Current Temperature: 23.45"
        temp_value = decoded_bytes.split(": ")[1]  # Split the string and take the second part as the temperature value
        print(decoded_bytes)  # for debugging
        return temp_value
    except Exception as e:
        print(f"Error reading from the serial port: {e}")
        return "Error"  # Return a placeholder or last known good value


# Home page that displays the temperature
@app.route("/")
def index():
    temp = get_temp_data()
    comment = get_temp_comment(temp)
    return render_template('index.html', temp=temp, comment=comment)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
