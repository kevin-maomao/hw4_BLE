# hw4_BLE

# How to Run Code

## On Mbed Program

* `git clone https://github.com/ARMmbed/mbed-os-example-ble`
* `cd mbed-os-example-ble`
* New an mbed studio project, delete the `main.cpp`
* Copy the files under the directory `BLE_GattServer_AddService` to the new project
* Replace `mbed_app.json` with `./server/mbed_app.json`
* Replace `source/main.cpp` with `./server/main.cpp`
* Put the files under `./server/MagnetoService.h` into `mbed-os/connectivity/FEATURE_BLE/include/ble/services/`
* Put the files `./server/mbed files/BSP_B-L475E-IOT01` into the project
