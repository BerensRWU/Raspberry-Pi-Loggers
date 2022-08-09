import pyaudio

root = f"/home/pi/Dokumente/allSensors/"
sensor_list = ["PiCamerHQ", "SenseHatv1.0", "VK-162", "USB Microphone"]


# --- Camera -----
camera_resolution = (864, 544)
camera_framerate = 32


# --- Microphone --
form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 40 # seconds to record
dev_index = 2 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'test1.wav' # name of .wav file


# --- GPS ----
keys_tpv = ['class', 'device', 'mode', 'time', 'leapseconds', 'ept', 'lat', 'lon', 'altHAE', 'altMSL', 'alt', 'epv', 'track', 'magtrack', 'magvar', 'speed', 'climb', 'eps', 'epc', 'geoidSep', 'eph']