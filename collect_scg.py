import time
import csv
import os
from jnius import autoclass

# 1. Konfigurera den lokala sökvägen (matchar din bild)
STORAGE_PATH = "/sdcard/Documents/scg-raw-data"
if not os.path.exists(STORAGE_PATH):
    # Om mappen mot förmodan inte hittas skapas den
    os.makedirs(STORAGE_PATH)

# 2. Android API-kopplingar för högfrekvent sampling
Context = autoclass('android.content.Context')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
activity = PythonActivity.mActivity
SensorManager = activity.getSystemService(Context.SENSOR_SERVICE)
Sensor = autoclass('android.hardware.Sensor')
SensorEventListener = autoclass('android.hardware.SensorEventListener')

class SCGListener(SensorEventListener):
    def __init__(self):
        self.data = []
        
    def onSensorChanged(self, event):
        # Vi fokuserar på Z-axeln (vibrationer vinkelrätt mot sternum)
        z_accel = event.values
        # Använd nanosekunder för att fånga snabba händelser som AO-toppen
        timestamp = time.time_ns()
        self.data.append((timestamp, z_accel))

    def onAccuracyChanged(self, sensor, accuracy):
        pass

# 3. Starta mätningen
listener = SCGListener()
accel = SensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)

# Använd SENSOR_DELAY_FASTEST för maximal samplingsfrekvens (~400-500Hz på Pixel 10)
SensorManager.registerListener(listener, accel, SensorManager.SENSOR_DELAY_FASTEST)

print(f"Mätning startad. Loggar till: {STORAGE_PATH}")
print("Håll Pixel 10 stilla på sternum i 30 sekunder...")

time.sleep(30) # Din 30-sekunders mätfas

# 4. Stoppa och spara
SensorManager.unregisterListener(listener)

file_name = f"SCG_{int(time.time())}.csv"
full_save_path = os.path.join(STORAGE_PATH, file_name)

with open(full_save_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp_ns', 'z_accel_m_s2'])
    writer.writerows(listener.data)

print(f"Mätning slutförd! Sparat {len(listener.data)} rader i {file_name}")
