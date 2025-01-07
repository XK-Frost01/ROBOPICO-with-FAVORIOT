# ROBOPICO-with-FAVORIOT
This project leverages the Robo Pico board, integrated with the Raspberry Pi Pico WH, to showcase IoT data communication with the FAVORIOT platform. The project demonstrates real-time data transmission and device control using the MQTT protocol via CircuitPython.

**Sensors Used**:
  * Ultrasonic Sensor (HC-SR04): Detects obstacles and measures distance.
  * Line Maker Sensor: Enables line-following functionality for robotic applications.
  * LDR Sensor: Measures ambient light intensity.
  * DHT11 Sensor: Monitors temperature and humidity levels.
  * Air Quality Sensor: Detects gas and air pollutants.

**Actuators Used**:
  * 2 Motors: Controls robotic movement and navigation.
  * 2 RGB LEDs: Provides multicolor visual feedback for system status or alerts.
  * Buzzer: Emits sound alerts and notifications.

**Project Highlights**:
  * Sensor data is transmitted to the FAVORIOT platform using the MQTT protocol, showcasing its effectiveness in IoT applications.
  * Commands received from FAVORIOT enable remote control of the actuators, including motors, LEDs, and the buzzer.
  * The project emphasizes the seamless integration of the Robo Pico board with FAVORIOT for IoT functionality.

By focusing on MQTT as the sole communication protocol, this project highlights how real-time data exchange and device control can be achieved efficiently using the Robo Pico board and FAVORIOT platform.

tukar gambar
<p align="center"><img src="https://github.com/XK-Frost01/Hibiscus-Sense-with-FAVORIOT/blob/main/Reference/PROJECT%20SETUP.png" width="900"></p>
<br>

## PROJECT SETUP

### Step 1: Installing CircuitPython firmware

* To install [CircuitPython](https://circuitpython.org/downloads), visit the official website and download the latest version:

```URL
https://circuitpython.org/downloads
```

<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/circuit%20python_1.png" width="900"></p>
<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/circuit%20python_2.png" width="900"></p>

> It is recommended to download the latest version of CircuitPython firmware for smoother library configuration and compatibility

* Next, visit the [CircuitPython Library](https://circuitpython.org/libraries) page to download the appropriate Python libraries:

```URL
https://circuitpython.org/libraries
```

<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/circuit%20python_3.png" width="900"></p>
<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/circuit%20python_4.png" width="900"></p>
 
 > Download the CircuitPython library bundle that matches the firmware version. For example, if the latest firmware version is 9.x, ensure you download the 9.x library bundle.
 
* Next, navigate back to the download page and click the following [link](https://learn.adafruit.com/pico-w-wifi-with-circuitpython/installing-circuitpython) to proceed to the next step.
* Download  flash resetting file to deep clean the Pico's RP1-RP2 (D:) drive
```URL
https://learn.adafruit.com/pico-w-wifi-with-circuitpython/installing-circuitpython
```

<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/circuit%20python_5.png" width="900"></p>
<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/circuit%20python_6.png" width="900"></p>
<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/circuit%20python_7.png" width="500"></p>

> note that, sometime resetting the Pico driver or changing firmware can be resulting to Pico not working as expected. So it recommended that, deep clean is done everytime you want to change the firmware

<br><br>

### Step 2: Install Mu editor

* Once all the CircuitPython libraries are installed, download and install the [Mu editor](https://codewith.mu/)

```URL
https://codewith.mu/
```

<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/mu%20editor_1.png" width="900"></p>
<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/mu%20editor_2.png" width="900"></p>
<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/mu%20editor_3.png" width="900"></p>
<br><br>

### Step 3: Pico's RP1-RP2(D:) Disk setup

* Open the RP1-RP2(D:) drive on your Pico by holding the BOOTSEL button while connecting the USB cable to your laptop.

<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/circuit%20python_8.png" width="500"></p>

* then, transfer all the file in sequence into pico (D:) as below:
    * flash_nuke.uf2
    * adafruit-circuitpython-raspberry_pi_pico_w-en_US-9.2.0.uf2

<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/circuit%20python_10.png" width="500"></p>
<br>

<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/NUKE%20transfer.gif" width="900"></a></p>

> 'drag and drop' flash_nuke.uf2 file into RP1-RP2(D:)

<br>

<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/FIRMWARE%20transfer.gif" width="900"></a></p>

> 'drag and drop' circuitpython firmware into RP1-RP2(D:)

<br>

* after finish you can unplug it and attach it to robopico board

<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/plug%20in.jpeg" width="500"></p>
<br><br>

### Step 4: setup favoriot platform

 * This project integrate the use if robopico with [FAVORIOT platform](https://platform.favoriot.com/login)
 * to open favoriot platform, you can search:

```URL
https://platform.favoriot.com/login
```

<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/FAVORIOT_1.png" width="900"></p>

 * For a beginner-friendly tutorial on getting started with the FAVORIOT platform and creating a device for your project, refer to the link provided below:

```URL
https://www.youtube.com/playlist?list=PLeB7L9fw2CnIrfLRYK42tPN2LJohwfGtu
```

> You can go through vedio 1 to 5 and decide on how to setup your project in FAVORIOT platform

 * or you can refer to FAVORIOT recources tab:

<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/FAVORIOT_2.png" width="900"></p>
<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/FAVORIOT_3.png" width="900"></p>
<br><br>

### Step 5: Uploading code inside CIRCUITPY(D:)

* After completing the device setup within the FAVORIOT platform for the Raspberry Pi Pico WH, launch the Mu Editor application

<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/run%20pico_1.png" width="500"></p>

* Switch the mode to CircuitPython.

<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/run%20pico_2.png" width="900"></p>

* then, open load file from CIRCUITPY(D:) which is code.py

<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/run%20pico_3.png" width="900"></p>

* You can select the code from the folder above which containing the python code for ROBOPICO and copy-paste it into code.py
* Then, click save file

<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/run%20pico_4.png" width="900"></p>

* After that, open serial monitor and click CTRL+D to reboot the program

<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/run%20pico_5.png" width="900"></p>

* Some libraries may be missing due to the newly downloaded firmware on the Pico. You will need to add the required libraries from the previously downloaded library bundle.

<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/run%20pico_6.png" width="900"></p>

* Note that the library bundle folder is too large to fit in the CIRCUITPY (D:) memory.
* Therefore, select only the necessary libraries and transfer them to CIRCUITPY (D:) > lib by either dragging and dropping or copy-pasting.

<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/run%20pico_7.png" width="500"></p>
<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/run%20pico_8.png" width="500"></p>

<br><br>

<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/LIB%20transfer.gif" width="900"></a></p>

> repeat the process until there is no error

<br><br>

* when, the library is added the code will rerun by itself

<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/run%20pico_9.png" width="500"></p>

 * then you can refer favoriot data stream to see if there is data entering

<p align="center"><img src="https://github.com/XK-Frost01/ROBOPICO-with-FAVORIOT/blob/main/Reference(R)/FAVORIOT_4.png" width="900"></p>
<br><br>
