from datetime import datetime

import configs

def get_sense_data(sense):
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

def get_GPS_data(gpsd):
    nx = gpsd.next()
    values = []
    if nx['class'] == 'TPV':
        for k in configs.keys_tpv:
            print(nx)
            if k in nx.keys():
                values += [nx[k]]
            else:
                values = []
                break
        return values