# IP_camera-Audio_Detection
Using Fast Fourier Transform to detect audio levels in a RTSP input and reboots camera if no audio is detected

This code is tested using an ONCAM EVOLUTION 5 IP camera.
The camera reboot function uses selenium package to open up a headless(hidden) web browser to perform camera reboot
! Every camera brand and model have their own RTSP URL format. Please check with the camera OEM before running any code

Fast Fourier Transform (FFT) is a mathematical operation which transform raw signals to frequency spectrums.
Human audible frequency ranges from 20Hz to 20kHz. When the code executes, RTSP audio is processed and displayed on a frequency spectrum (like a mixer)
If audio exceeds a certain threshold (max_y), audio is present. Note that this threshold has to be set based on the normal environment of the camera which audio is present.

Audio is sampled at 1 per second, up to 60 seconds.
If audio is present for 50 out of 60 seconds, the code writes a log onto the desktop indicating that audio is present, together with a time stamp (for tracking purposes)
When the code runs for the first time, a new txt file is created on the desktop with the name "reboot log". Subsequent execution of code appends the row in the same txt file.

If audio is not present for more than 10 seconds, the code reboots the camera and then writes to "reboot log" with the time stamp, indicating that a reboot has taken place.
