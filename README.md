# hw4_BLE

# How to Run Code

## On Mbed Program

* `git clone https://github.com/ARMmbed/mbed-os-example-ble`
* `cd mbed-os-example-ble`
* New an mbed studio project, delete the `main.cpp`
* Copy the files under the directory `BLE_GattServer_AddService` to the new project
* Modify `mbed_app.json`
* Put the files under `./server` into `mbed-os/connectivity/FEATURE_BLE/include/ble/services/`
