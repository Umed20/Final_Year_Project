from RPi.GPIO import GPIO

import serial
import time
import json
from datetime import datetime
from adafruit_fingerprint import Adafruit_Fingerprint


# Pin configurations
ALCOHOL_SENSOR = 17
GAS_SENSOR = 27
LDR_SENSOR = 22
BRAKE_SENSOR = 23
TOWED_SENSOR = 24
ACCIDENT_SENSOR = 25
IGNITION_SENSOR = 4
TEMP_SENSOR = 18

# GSM configuration
GSM_PORT = '/dev/ttyUSB0'
GSM_BAUDRATE = 9600

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    # Setup input pins
    input_pins = [ALCOHOL_SENSOR, GAS_SENSOR, LDR_SENSOR, BRAKE_SENSOR, 
                 TOWED_SENSOR, ACCIDENT_SENSOR, IGNITION_SENSOR]
    for pin in input_pins:
        GPIO.setup(pin, GPIO.IN)
    
    # Setup DHT11 temperature sensor
    GPIO.setup(TEMP_SENSOR, GPIO.IN)

def get_fingerprint_status():
    try:
        # Initialize fingerprint sensor
        uart = serial.Serial("/dev/ttyUSB1", baudrate=57600, timeout=1)
        finger = Adafruit_Fingerprint(uart)
        
        # Try to read fingerprint
        if finger.get_image() == Adafruit_Fingerprint.OK:
            if finger.image_2_tz(1) == Adafruit_Fingerprint.OK:
                return 'Pass'
        return 'Fail'
    except Exception as e:
        print(f"Fingerprint sensor error: {e}")
        return 'Fail'

def get_vehicle_status():
    return {
        'ignition': 'ON' if GPIO.input(IGNITION_SENSOR) else 'OFF',
        'brake': 'ON' if GPIO.input(BRAKE_SENSOR) else 'OFF',
        'towed_status': 'ON' if GPIO.input(TOWED_SENSOR) else 'OFF',
        'accident_detection': 'ON' if GPIO.input(ACCIDENT_SENSOR) else 'OFF'
    }

def read_dht11():
    # Basic DHT11 reading implementation
    # You might want to use a DHT11 library for more reliable readings
    try:
        GPIO.setup(TEMP_SENSOR, GPIO.OUT)
        GPIO.output(TEMP_SENSOR, GPIO.LOW)
        time.sleep(0.02)
        GPIO.output(TEMP_SENSOR, GPIO.HIGH)
        GPIO.setup(TEMP_SENSOR, GPIO.IN)
        
        # Wait for response
        count = 0
        while GPIO.input(TEMP_SENSOR) == GPIO.LOW:
            count += 1
            if count > 100:
                return 25  # Return default value if reading fails
                
        count = 0
        while GPIO.input(TEMP_SENSOR) == GPIO.HIGH:
            count += 1
            if count > 100:
                return 25
        
        # Read data (simplified)
        data = []
        for i in range(40):
            count = 0
            while GPIO.input(TEMP_SENSOR) == GPIO.LOW:
                count += 1
                if count > 100:
                    return 25
            
            count = 0
            while GPIO.input(TEMP_SENSOR) == GPIO.HIGH:
                count += 1
                if count > 100:
                    return 25
            
            if count > 28:
                data.append(1)
            else:
                data.append(0)
                
        # Convert to temperature (simplified)
        temp = int(''.join(map(str, data[16:24])), 2)
        return temp
    except Exception as e:
        print(f"Temperature sensor error: {e}")
        return 25

def get_safety_metrics():
    temperature = read_dht11()
    
    # Read analog sensors through GPIO
    return {
        'alcohol_detection': 'ON' if GPIO.input(ALCOHOL_SENSOR) else 'OFF',
        'temperature': f"{temperature}°C",
        'speed_level': get_speed_level(),
        'gas_detection': 'ON' if GPIO.input(GAS_SENSOR) else 'OFF',
        'light_level': get_light_level()
    }

def get_speed_level():
    # This would typically come from a speed sensor or CAN bus
    # For now, we'll return a default value
    return 'Medium'

def get_light_level():
    if GPIO.input(LDR_SENSOR):
        return 'HIGH'
    return 'LOW'

def get_location_data():
    try:
        # Initialize GSM module for GPS
        gsm = serial.Serial(GSM_PORT, GSM_BAUDRATE, timeout=1)
        
        # Send AT command to get GPS data
        gsm.write(b'AT+CGPSINF=0\r')
        time.sleep(1)
        
        if gsm.in_waiting:
            response = gsm.readline().decode('utf-8').strip()
            # Parse GPS data (format depends on your GSM module)
            # This is an example format, adjust according to your module
            parts = response.split(',')
            if len(parts) >= 4:
                lat = float(parts[1])
                lon = float(parts[2])
                return {
                    'latitude': lat,
                    'longitude': lon,
                    'location_name': 'Current Location'  # You might want to use reverse geocoding here
                }
        
        gsm.close()
        
    except Exception as e:
        print(f"GPS error: {e}")
    
    # Return default location if GPS fails
    return {
        'latitude': 19.0760,
        'longitude': 72.8777,
        'location_name': 'Location Unavailable'
    }

def send_sms_alert(message, phone_number):
    try:
        # Initialize GSM module
        gsm = serial.Serial(GSM_PORT, GSM_BAUDRATE, timeout=1)
        
        # Set SMS text mode
        gsm.write(b'AT+CMGF=1\r')
        time.sleep(1)
        
        # Set phone number
        gsm.write(f'AT+CMGS="{phone_number}"\r'.encode())
        time.sleep(1)
        
        # Send message
        gsm.write(message.encode() + b'\x1A')
        time.sleep(1)
        
        # Check response
        if gsm.in_waiting:
            response = gsm.readline().decode('utf-8').strip()
            gsm.close()
            return 'OK' in response
            
        gsm.close()
        return False
        
    except Exception as e:
        print(f"SMS error: {e}")
        return False