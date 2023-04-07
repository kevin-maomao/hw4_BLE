from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate
import struct

NOTIF_ON = struct.pack('BB', 0x01, 0x00)

# user configuration
DEVICE_NAME = "Kevin's Sensor"

HEART_SERVICE_UUID = 0x180d
HEART_RATE_UUID = 0x2a37
HEART_LOCATION_UUID = 0x2a38

MAG_SERVICE_UUID = 0xa000
MAG_X_RATE_UUID = 0xa001
MAG_Y_RATE_UUID = 0xa002
MAG_Z_RATE_UUID = 0xa003

# DefaultDelegate: to receive Bluetooth message asynchronously

def dataParsing(data):
    data_list = list(data)
    if len(data_list) < 4:
        print("\n//--HeartRate--//")
        print("Data: ", data_list[1])
    else:
        if data_list[3]==2:
            print("//--MagXRate--//")
        elif data_list[3]==3:
            print("//--MagYRate--//")
        elif data_list[3]==4:
            print("//--MagZRate--//")

        if data_list[0]==0:
            final_data = int(data_list[2])*256+int(data_list[1])
            print("Data: ", final_data)
        elif data_list[0]==1:
            final_data = int(data_list[2])*256+int(data_list[1])-65536
            print("Data: ", final_data)

# ScanDelegate: to scan for BLE devices which are broadcasting data
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

# PeripheralDelegate: to handle notification from BLE server
class PeripheralDelegate(DefaultDelegate):
    def __init__(self, handle):
        DefaultDelegate.__init__(self)
        #print("handleNotification init")
        self.hndl = handle

    def handleNotification(self, cHandle, data):
        dataParsing(data)

# withDelegate: to stores a reference to a delegate object, which receives callbacks when broadcasts from devices are received
scanner = Scanner().withDelegate(ScanDelegate()) 
devices = scanner.scan(3.0)
n = 0
device_num = 0
for dev in devices:
    print ("%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr, dev.addrType, dev.rssi))
    n += 1
    for (adtype, desc, value) in dev.getScanData():
        if (value == DEVICE_NAME):
            print('/////////////////////////////////////////////////////////////////')
            print('HERE IS THE NAME OF YOUR DEVICE:')
            print("%s, %s" % (desc, value))
            print('/////////////////////////////////////////////////////////////////')
            device_num = n-1
        else:
            print ("%s, %s" % (desc, value))

print ("Connecting...")
dev = Peripheral(list(devices)[device_num].addr, 'random')

try:

    print ("Services...")
    for service in dev.services:
        print (str(service))

    print("Characteristics...")
    heart_service = dev.getServiceByUUID(UUID(HEART_SERVICE_UUID))
    ch_heartrate = dev.getCharacteristics(uuid=UUID(HEART_RATE_UUID))[0]
    ch_heartlocation = dev.getCharacteristics(uuid=UUID(HEART_LOCATION_UUID))[0]

    mag_service = dev.getServiceByUUID(UUID(MAG_SERVICE_UUID))
    ch_mag_x_rate = dev.getCharacteristics(uuid=MAG_X_RATE_UUID)[0]
    ch_mag_y_rate = dev.getCharacteristics(uuid=MAG_Y_RATE_UUID)[0]
    ch_mag_z_rate = dev.getCharacteristics(uuid=MAG_Z_RATE_UUID)[0]

    ch_heartrate_handle_cccd = ch_heartrate.getDescriptors(forUUID=0x2902)[0]
    ch_mag_x_handle_cccd = ch_mag_x_rate.getDescriptors(forUUID=0x2902)[0]
    ch_mag_y_handle_cccd = ch_mag_y_rate.getDescriptors(forUUID=0x2902)[0]
    ch_mag_z_handle_cccd = ch_mag_z_rate.getDescriptors(forUUID=0x2902)[0]

    dev = dev.withDelegate(PeripheralDelegate(ch_heartrate_handle_cccd))
    
    ch_heartrate_handle_cccd.write(NOTIF_ON)
    ch_mag_x_handle_cccd.write(NOTIF_ON)
    ch_mag_y_handle_cccd.write(NOTIF_ON)
    ch_mag_z_handle_cccd.write(NOTIF_ON)

    while True:
        if dev.waitForNotifications(3.0):
            continue

        print ("Waiting...")
    
finally:
    dev.disconnect()