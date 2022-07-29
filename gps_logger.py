from gps import *
import time
from csv import writer

running = True

keys_tpv = ['class', 'device', 'status', 'mode', 'time', 'leapseconds', 'lat', 'lon', 'altHAE', 'altMSL', 'alt', 'track', 'magtrack', 'magvar', 'speed', 'climb', 'geoidSep']

def logGPSData(gps):
    nx = gpsd.next()
    # For a list of all supported classes and fields refer to:
    # https://gpsd.gitlab.io/gpsd/gpsd_json.html
    values = []
    if nx['class'] == 'TPV':
        for k in keys_tpv:
            values += [nx[k]]
        print(nx['lat'], nx['lon'])
        return values
        
gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

with open('gps_log.csv', 'w', newline='') as f:
    data_writer = writer(f)
    data_writer.writerow(keys_tpv)

try:
        print("Logging started!")
        while running:
            logdata = logGPSData(gpsd)
            if logdata:
                with open('gps_log.csv', 'a', newline='') as f:        
                    data_writer = writer(f)
                    data_writer.writerow(logdata)
except(KeyboardInterrupted):
    print("Logging closed!")

