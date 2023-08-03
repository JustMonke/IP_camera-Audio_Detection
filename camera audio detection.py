import cv2
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime

def Audio_detection():

    # Initialize counter
    counter = 0
    start_time = time.time()
    
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Set audio parameters
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK_SIZE = 1024

    # Start audio stream
    stream = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE)

    # Initialize IP camera stream
    camera_url = "rtsp://admin:admin@192.168.18.238:554/h264/video.sdp?camera=25"
    cap = cv2.VideoCapture(camera_url)

    # Create a figure and axes for plotting
    fig, ax = plt.subplots()

    # Calculate the scaling factor for amplitude
    scaling_factor =  CHUNK_SIZE /1000


    for number in range(1, 61):
        # Capture a single video frame from IP camera
        ret, frame = cap.read()

        # Extract audio data from audio stream
        audio_data = stream.read(CHUNK_SIZE)
        audio_array = np.frombuffer(audio_data, dtype=np.int16)

        # Calculate the amplitude
        max_amplitude = np.max(np.abs(audio_array))

        # Calculate the frequency response using FFT
        fft_data = np.fft.fft(audio_array)
        fft_freq = np.fft.fftfreq(len(audio_array), d=1.0/RATE)

        # Clear the previous plot
        ax.clear()

        # Scale the magnitude values to represent amplitude
        amplitude_data = np.abs(fft_data) * scaling_factor
    
        # Plot the frequency response curve
        ax.plot(fft_freq, np.abs(fft_data))

        # Set the x-axis limits to the human audible range (20 Hz to 20,000 Hz)
        ax.set_xlim(20, 20000)

        ax.set_ylim(0, 50000)

        # Set labels and title
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Amplitude')
        ax.set_title('Frequency Response')

        # Print the maximum y-axis value
        max_y = np.max(amplitude_data)

        # Display the plot
        plt.draw()
        plt.pause(1)  # Pause for 1 second before generating the next plot

        if max_y<=7000:
            print(f"Audio loss at {number}, Amplitude = {max_y}")

        # Perform detection of amplitude
        if max_y>7000:
            counter = counter + 1
            print(f"Audio present at {number}, count = {counter}/60")
        if counter >= 50: # at least 50 seconds of video contains audio
            print("Audio count = 50/60, Camera audio is working normally")
            return True
            

    # Stop and release resources
    cap.release()
    stream.stop_stream()
    stream.close()
    p.terminate()

def Camera_reboot():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('log-level=3')
    driver = webdriver.Chrome(service_log_path='NUL', options=options)
    driver.get("http://admin:admin@192.168.18.238")

    admin = driver.find_element(By.XPATH, '//*[@id="panel2Header"]')
    admin.click()

    Maintenance = driver.find_element(By.CSS_SELECTOR, "#panel2Content > div:nth-child(15) > input:nth-child(1)")
    Maintenance.click()

    driver.switch_to.frame(0)
    Reboot = driver.find_element(By.CSS_SELECTOR, "input.button:nth-child(10)")
    Reboot.click()
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(1)
    driver.close()

def Write_log_naudio():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("C:/Users/Asus/Desktop/RebootLog.txt", "a") as file:
        file.write("Camera has been rebooted on "+ current_time +"\n")    

def Write_log_audio():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("C:/Users/Asus/Desktop/RebootLog.txt", "a") as file:
        file.write("Audio is present."+"\n") 


def Main():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #get current time
    with open("C:/Users/Asus/Desktop/RebootLog.txt", "a") as file:       #create file in specified folder and append
        file.write("Camera scan on " + current_time + "\n")              #log down time of scan

    if Audio_detection():                                                #if audio is detected, do nothing
        Write_log_audio()                                                #log down that audio is present
        pass
    else:
        Camera_reboot()                                                  #if no audio is detected, reboot camera
        Write_log_naudio()                                               #log down reboot time
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("Camera rebooted on " + current_time)

Main()

        
        
