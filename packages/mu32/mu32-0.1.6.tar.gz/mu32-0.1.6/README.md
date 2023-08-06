# Mu32

Python MegaMicro Mu32 driver.

*Megamicro 32 (Mu32)* is an antenna with 8 to 32 microphones used to locate, characterize and classify sound sources. For more information, visit the website [DistalSense.com](https://distalsense.com).

This repository gathers the drivers allowing to use the *Mu32* system, an API to write your application programs as well as many illustrative examples.

Consult the documentation on the site [DistalSense.io](https://DistalSense.io).

## Changelog

### 0.1.6 (2022-06-16)

* Update MuH5 with analog channels that had been forgotten
* Add mu32cv.py example program with video monitoring
* Add video monitoring to core_base program

### 0.1.5 (2022-06-14)

* Add muH5-check program for H5 file checking
* Write Mu256 based examples
* Test analogic channels on 256 MegaMicro device
* Fix channels number error in H5 writing method

### 0.1.4 (2022-05-30)

* Add core APIs in documentation
* Add many use case examples
* Add server task scheduling
* Add server H5 file management

### 0.1.3 (2022-05-23)

* Add server H5 playing mode
* Add server H5 recording through clients (H5 pass through)
* Add post processing user function handling in Mu32ws

### 0.1.2 (2022-05-22)

* Fix an error in packaging of mu32-doa console script

### 0.1.1 (2022-05-21)

* Update documentation (H5 recording and playing, networking)
* add muH5 class for H5 file reading
* add H5 data recording to mu32 classes
* add networking examples
* add mu32 server with websocket networking protocol as server
* add mu32ws class with websocket networking protocol as client

### 0.1.0 (2022-03-22)

* Update documentation
* New release branch 0.1

### 0.0.6 (2022-03-20)

* Corrects examples to conform them to previous changes
* change callbacks data exchange format from numpy array of rows buffer (n_mems X n_samples) to n-d numpy array where n is the number of microphones: (n_mems, n_samples)
* fix misalignment of data between FPGA and USB transfer by reseting FX3 Usb adapter every time a loss of data occurs
* control loss of data which occurs when user callback function takes too long
* fix wrong code sequence for FPGA resetting
* fix wrong code for FX3 resetting
* fix the impossibility of writing a valuable code for sending the FX3 reset command
* add counter channel acquisition and set it as default

### 0.0.5 (2022-03-15)

* Fix some bugs due to logging update done in previous release
* Add mu32doa realtime example
* Update documentation

### 0.0.4 (2022-03-13)

* Add beamformer and synthesis modules
* Add jupyter examples files for beamforming
* Remove Mu32Exception and Logging tools from core: create new corresponding separate files

### 0.0.3 (2022-03-06)

* Add examples/mu32save.py example program for saving data in HDF5 format

### 0.0.2 (2022-02-20)

* Fixes the data unflushing warning (adds a function to empty Mu32 internal buffers)

### 0.0.1 (2022-02-18)

* Initial release
