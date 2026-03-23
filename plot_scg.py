import pandas as pd
import matplotlib.pyplot as plt
import os

# Hämta den senaste filen från din mapp
folder = "/sdcard/Documents/scg-raw-data/"
files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.csv')]
latest_file = max(files, key=os.path.getctime)

data = pd.read_csv(latest_file)

# Enkel plot av Z-axeln för att se hjärtslagen
plt.figure(figsize=(12, 4))
plt.plot(data['z_accel_m_s2'].values[500:1500]) # Visar ca 2 sekunder data
plt.title("Rå Seismokardiografi (SCG) - Pixel 10")
plt.ylabel("Acceleration (Z)")
plt.show()
