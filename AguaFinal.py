# import required modules
from machine import ADC, Pin, I2C
from ssd1306 import SSD1306_I2C
import utime

 
# use variables instead of numbers:
soil = ADC(Pin(28)) # Soil moisture PIN reference
relay = Pin(18, Pin.OUT)
 
#Calibraton values
min_moisture=19200
max_moisture=49300
 
readDelay = 0.5 # delay between readings
 
WIDTH  = 128                                            # oled display width
HEIGHT = 64                                            # oled display height
 
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=200000)       # Init I2C using pins GP0 & GP1 
print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
print("I2C Configuration: "+str(i2c))                   # Display I2C config
 
 
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display
 
while True:
    oled.fill(0)
    # read moisture value and convert to percentage into the calibration range
    moisture = (max_moisture-soil.read_u16())*100/(max_moisture-min_moisture) 
    # print values
    print("moisture: " + "%.2f" % moisture +"% (adc: "+str(soil.read_u16())+")")
    
    oled.text("Soil Moisture",10,15)
    oled.text(str("%.2f" % moisture)+" %",35,35)
    oled.show()
    
    if moisture <= 70.0:
        relay.value(0)
        print('On')
        utime.sleep(2)
        print('Off')
        relay.value(1)
        print('On')
        utime.sleep(2)
        print('Off')
    
    utime.sleep(readDelay) # set a delay between readings  