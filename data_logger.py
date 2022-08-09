from sense_hat import SenseHat
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
from time import sleep
from csv import writer
import pygame
from pygame.locals import *
import pyaudio
import wave
from gps import *
from datetime import datetime

import configs
from utils import get_sense_data, get_GPS_data

if os.path.exists(f"{configs.root}/record_meta.txt"):
    with open(f"{configs.root}/record_meta.txt", "rb") as f:
        try:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b"\n":
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        meta_data = f.readline().decode()
        recording_number = int(meta_data.split(",")[0]) + 1
        with open(f"{configs.root}/record_meta.txt", "a", newline="") as f:
            data_writer = writer(f)
            data_writer.writerow([recording_number, datetime.now()] + configs.sensor_list)
else:    
    recording_number = 0
    
    with open(f"{configs.root}/record_meta.txt", "a", newline="") as f:
        data_writer = writer(f)
        data_writer.writerow([recording_number, datetime.now()] + configs.sensor_list)

configs.root = f"{configs.root}/recording_{recording_number}"
os.mkdir(configs.root)
os.mkdir(f"{configs.root}/microphone_records")
os.mkdir(f"{configs.root}/camera_records")

is_running = True

# -- Camera ---
camera = PiCamera()
camera.resolution = configs.camera_resolution
camera.framerate = configs.camera_framerate
rawCapture = PiRGBArray(camera, size=configs.camera_resolution)
sleep(1)

# -- Microphone ---
audio = pyaudio.PyAudio() # create pyaudio instantiation
stream = audio.open(format = configs.form_1,rate = configs.samp_rate,channels = configs.chans, \
                    input_device_index = configs.dev_index, input = True, \
                    frames_per_buffer = configs.chunk)

# -- GPS ---
gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

with open(f"{configs.root}/gps_records.csv", "w", newline="") as f:
    data_writer = writer(f)
    data_writer.writerow(configs.keys_tpv)

# -- SenseHat ---
sense = SenseHat()

pygame.init()
pygame.display.set_mode((1, 1))

with open(f"{configs.root}/senseHat_records.csv", "w", newline='') as f:
    data_writer = writer(f)
    
    data_writer.writerow(["temp", "pres", "hum",
                          "yaw", "pitch", "roll",
                          "mag_x", "mag_y", "mag_z",
                          "acc_x", "acc_y", "acc_z",
                          "gyro_x", "gyro_y", "gyro_z",
                          "datetime"])

sense.set_pixels([(255,255,255)]*64)

try:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):        

        image = frame.array
        mic_data = stream.read(configs.chunk, exception_on_overflow = False)
        senseHat_data = get_sense_data(sense)
        gps_data = get_GPS_data(gpsd)
        
        with open(f"{configs.root}/senseHat_records.csv", "a", newline="") as f:
            data_writer = writer(f)
            data_writer.writerow(senseHat_data)

        cv2.imwrite(f"{configs.root}/camera_records/{senseHat_data[-1]}.jpg", image)
        rawCapture.truncate(0)
        

        with open(f"{configs.root}/microphone_records/{senseHat_data[-1]}.bit", "wb") as f:
            f.write(mic_data)
            
        if gps_data:
            with open(f"{configs.root}/gps_records.csv", "a", newline="") as f:        
                data_writer = writer(f)
                data_writer.writerow(gps_data + [senseHat_data[-1]])
                    
        key_event = pygame.event.get()
        if key_event:
            if key_event[0].type in [2,3] :
                sense.set_pixels([(0,255,0)]*64)
                is_running = False
                break       
                
finally:
    if is_running:
        sense.set_pixels([(255,0,0)]*64)
    # stop the stream, close it, and terminate the pyaudio instantiation
    stream.stop_stream()
    stream.close()
    audio.terminate()

