from sense_hat import SenseHat
from datetime import datetime
from csv import writer
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep, time
import cv2

def get_sense_data():
    sense_data = []
    # Get environmental data
    sense_data.append(sense.get_temperature())
    sense_data.append(sense.get_pressure())
    sense_data.append(sense.get_humidity())
    # Get orientation data
    orientation = sense.get_orientation()
    sense_data.append(orientation["yaw"])
    sense_data.append(orientation["pitch"])
    sense_data.append(orientation["roll"])
    # Get compass data
    mag = sense.get_compass_raw()
    sense_data.append(mag["x"])
    sense_data.append(mag["y"])
    sense_data.append(mag["z"])
    # Get accelerometer data
    acc = sense.get_accelerometer_raw()
    sense_data.append(acc["x"])
    sense_data.append(acc["y"])
    sense_data.append(acc["z"])
    #Get gyroscope data
    gyro = sense.get_gyroscope_raw()
    sense_data.append(gyro["x"])
    sense_data.append(gyro["y"])
    sense_data.append(gyro["z"])
    # Get the date and time
    sense_data.append(datetime.now())

    return sense_data

sense = SenseHat()
camera = PiCamera()
camera.resolution = (860, 540)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(860, 540))
sleep(1)
with open('data.csv', 'w', newline='') as f:
    data_writer = writer(f)
    
    data_writer.writerow(['temp', 'pres', 'hum',
                          'yaw', 'pitch', 'roll',
                          'mag_x', 'mag_y', 'mag_z',
                          'acc_x', 'acc_y', 'acc_z',
                          'gyro_x', 'gyro_y', 'gyro_z',
                          'datetime'])
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array
        # show the frame
        cv2.imshow("Frame", image)
        
        data = get_sense_data()
        data_writer.writerow(data)
        
        cv2.imwrite(f"cam_records/{data[-1]}.jpg", image)
        
        key = cv2.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
        

  


