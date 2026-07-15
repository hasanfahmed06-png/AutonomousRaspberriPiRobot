Step 1
import RPi.GPIO as GPIO
import time
import sys
import lcd
 
from gpiozero import DistanceSensor 
 
 
mode=GPIO.getmode()
# Cleanup any pre-existing configurations
GPIO.cleanup()
# Define motor control pins
motor1_forward=5
motor1_backward=0
motor2_forward=7
motor2_backward=6
# Define LED pins
status_LED = 19
led1 = 12
led2 = 26
# Define buzzer pin
buzzer_pin =16
 
# Define servo motor
GPIO.setmode(GPIO.BCM) 
GPIO.setup(21, GPIO.OUT) 
servo = GPIO.PWM(21,50) 
 
# Define GPIO pins for the stepper motor 
 
out1 = 17 
 
out2 = 22 
 
out3 = 27 
 
out4 = 10 
 
# Define the time between each step (in seconds) and the number of steps. 
 
step_sleep = 0.02 
 
step_count = 100 
# Initialize the DistanceSensor with the echo pin set to GPIO 24 and the trigger pin set to GPIO 23. 
ultrasonic = DistanceSensor(echo=24, trigger=23) 
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Configure the pin as an output
GPIO.setup(status_LED, GPIO.OUT)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
# Set the buzzer pin as an output
GPIO.setup(buzzer_pin, GPIO.OUT)
# Configure motor pins as outputs
GPIO.setup(motor1_forward, GPIO.OUT)
GPIO.setup(motor2_forward, GPIO.OUT)
GPIO.setup (motor1_backward, GPIO.OUT)
GPIO.setup(motor2_backward, GPIO.OUT)
 
 
def buzz():
    for X in range (100):
    # Turn ON the buzzer
        GPIO.output(buzzer_pin, True)
    # Keep the buzzer on for 0.01 seconds
        time.sleep(0.01)
    # Turn OFF the buzzer
        GPIO.output(buzzer_pin, False)
        time.sleep(0.01)
        
def forward(x):
    # Activate forward pins
    GPIO.output(motor1_forward, GPIO.HIGH)
    GPIO.output(motor2_forward, GPIO.HIGH)
    print("Moving Forward")
    time.sleep(x)
    # Turn off the motors after moving
    GPIO.output(motor1_forward, GPIO.LOW)
    GPIO.output(motor2_forward, GPIO.LOW)
    
def backward(x):
    # Activate backward pins
    GPIO.output(motor1_backward, GPIO.HIGH)
    GPIO.output(motor2_backward, GPIO.HIGH)
    print("Moving Backward")
    time.sleep(x)
    # Turn off the motors after moving
    GPIO.output(motor1_backward, GPIO.LOW)
    GPIO.output(motor2_backward, GPIO.LOW)
    
def cleanup():
    GPIO.output(motor1_forward, GPIO.LOW)
    GPIO.output(motor2_forward, GPIO.LOW)
    GPIO.output(motor1_backward, GPIO.LOW)
    GPIO.output(motor2_backward, GPIO.LOW)
    GPIO.output(out1, GPIO.LOW) 
    GPIO.output(out2, GPIO.LOW) 
    GPIO.output(out3, GPIO.LOW) 
    GPIO.output(out4, GPIO.LOW) 
 
    GPIO.cleanup()
try:
    #Setup LCD
    lcd.lcd_init()
    time.sleep(1)
    
except KeyboardInterrupt:
    pass
 
# Setting up 
 
GPIO.setmode(GPIO.BCM) 
 
GPIO.setup(out1,GPIO.OUT) 
 
GPIO.setup(out2,GPIO.OUT) 
 
GPIO.setup(out3,GPIO.OUT) 
 
GPIO.setup(out4,GPIO.OUT) 
 
# Initializing 
 
GPIO.output(out1, GPIO.LOW) 
 
GPIO.output(out2, GPIO.LOW) 
 
GPIO.output(out3, GPIO.LOW) 
 
GPIO.output(out4, GPIO.LOW) 
 
try:
    forward(2)
    
    # Start the PWM with an initial duty cycle of 0% (servo remains in its default position) 
    servo.start(0) 
    # Move the servo to a specific position by changing the duty cycle to 3% 
    servo.ChangeDutyCycle(3) 
    time.sleep(1) 
    # Change the duty cycle to 12% to move the servo to another position 
    servo.ChangeDutyCycle(12) 
    time.sleep(1) 
    # Stop the PWM and clean up the GPIO pins 
    servo.stop() 
    #GPIO.cleanup() 
 
    lcd.printer(str(ultrasonic.distance),"")
    
    if ultrasonic.distance < 1.0:
        GPIO.output(led1,GPIO.HIGH) 
        GPIO.output(led2,GPIO.HIGH) 
        GPIO.output(status_LED,GPIO.HIGH) 
        # Keep the LED on for 2 seconds 
 
        time.sleep(2) 
 
        # Turn OFF the status LED         
        GPIO.output(led1,GPIO.LOW)
        GPIO.output(led2,GPIO.LOW)
        GPIO.output(status_LED,GPIO.LOW)
        
        try: 
 
            i = 0 
        
            for i in range (step_count): 
        
                # This pattern energizes the motor coils in sequence to make it step. 
        
                if i%4==0: 
        
                    GPIO.output(out4, GPIO.HIGH) 
        
                    GPIO.output(out3, GPIO.LOW) 
        
                    GPIO.output(out2, GPIO.HIGH) 
        
                    GPIO.output(out1, GPIO.LOW) 
        
                elif i%4==1: 
        
                    GPIO.output(out4, GPIO.LOW) 
        
                    GPIO.output(out3, GPIO.LOW) 
        
                    GPIO.output(out2, GPIO.HIGH) 
        
                    GPIO.output(out1, GPIO.HIGH) 
        
                elif i%4==2: 
        
                    GPIO.output(out4, GPIO.LOW) 
        
                    GPIO.output(out3, GPIO.HIGH) 
        
                    GPIO.output(out2, GPIO.LOW) 
        
                    GPIO.output(out1, GPIO.HIGH) 
        
                elif i%4==3: 
        
                    GPIO.output(out4, GPIO.HIGH) 
        
                    GPIO.output(out3, GPIO.HIGH) 
        
                    GPIO.output(out2, GPIO.LOW) 
        
                    GPIO.output(out1, GPIO.LOW) 
        
                time.sleep(step_sleep) 
        
        except KeyboardInterrupt: 
        
            GPIO.cleanup() 
        
            exit(1) 
            
            
        time.sleep(2)
    
    lcd.printer("","")
except KeyboardInterrupt:
    GPIO.cleanup()
    exit(1)
 
try:
    backward(2)
    
    
 
   
    lcd.printer(str(ultrasonic.distance),"")
    if ultrasonic.distance < 1.0:
       buzz()
except KeyboardInterrupt:
    GPIO.cleanup()
    exit(1)
 
# Cleanup after the program finishes
cleanup()
exit(0)

Step 2 + 3
import RPi.GPIO as GPIO
import time
import sys
import lcd
from gpiozero import DistanceSensor
 
 
mode=GPIO.getmode()
# Cleanup any pre-existing configurations
GPIO.cleanup()
 
# Define motor control pins
motor1_forward=5
motor1_backward=0
motor2_forward=7
motor2_backward=6
 
# Define LED pins
status_LED = 19
led1 = 12
led2 = 26
 
# Define buzzer pin
buzzer_pin =16
# Set the buzzer pin as an output
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(buzzer_pin, GPIO.OUT)
freq = 100
buzzer_pin = GPIO.PWM(buzzer_pin, freq)
 
# Define servo motor
GPIO.setmode(GPIO.BCM) 
GPIO.setup(21, GPIO.OUT) 
servo = GPIO.PWM(21,50)
GPIO.setwarnings(False)
 
# Define GPIO pins for the stepper motor
out1 = 17
out2 = 22
out3 = 27
out4 = 10
 
# Define the time between each step (in seconds) and the number of steps.
step_sleep = 0.02
 
 
# Initialize the DistanceSensor with the echo pin set to GPIO 24 and the trigger pin set to GPIO 23. 
ultrasonic = DistanceSensor(echo=24, trigger=23)
 
# Setting up stepper motor
GPIO.setup(out1,GPIO.OUT)
GPIO.setup(out2,GPIO.OUT)
GPIO.setup(out3,GPIO.OUT)
GPIO.setup(out4,GPIO.OUT)
 
# Initializing
GPIO.output(out1, GPIO.LOW)
GPIO.output(out2, GPIO.LOW)
GPIO.output(out3, GPIO.LOW)
GPIO.output(out4, GPIO.LOW)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
# Configure the pin as an output
GPIO.setup(status_LED, GPIO.OUT)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
 
 
 
# Configure motor pins as outputs
GPIO.setup(motor1_forward, GPIO.OUT)
GPIO.setup(motor2_forward, GPIO.OUT)
GPIO.setup (motor1_backward, GPIO.OUT)
GPIO.setup(motor2_backward, GPIO.OUT)
 
def buzz(buzz_time, freq):
    buzzer_pin.start(freq)
    time.sleep(buzz_time)
    buzzer_pin.stop()
    
        
def forward(x):
    # Activate forward pins
    GPIO.output(motor1_forward, GPIO.HIGH)
    GPIO.output(motor2_forward, GPIO.HIGH)
    time.sleep(x)
    # Turn off the motors after moving
    GPIO.output(motor1_forward, GPIO.LOW)
    GPIO.output(motor2_forward, GPIO.LOW)
    
def backward(x):
    # Activate backward pins
    GPIO.output(motor1_backward, GPIO.HIGH)
    GPIO.output(motor2_backward, GPIO.HIGH)
    time.sleep(x)
    # Turn off the motors after moving
    GPIO.output(motor1_backward, GPIO.LOW)
    GPIO.output(motor2_backward, GPIO.LOW)
    
def stepper_motor(step_count):
    for i in range (step_count): 
        # This pattern energizes the motor coils in sequence to make it step.
        if i%4==0:
            GPIO.output(out4, GPIO.HIGH)
            GPIO.output(out3, GPIO.LOW) 
            GPIO.output(out2, GPIO.HIGH)
            GPIO.output(out1, GPIO.LOW)
        elif i%4==1:
            GPIO.output(out4, GPIO.LOW)
            GPIO.output(out3, GPIO.LOW)
            GPIO.output(out2, GPIO.HIGH)
            GPIO.output(out1, GPIO.HIGH)
        elif i%4==2:
            GPIO.output(out4, GPIO.LOW)
            GPIO.output(out3, GPIO.HIGH)
            GPIO.output(out2, GPIO.LOW)
            GPIO.output(out1, GPIO.HIGH) 
        elif i%4==3:
            GPIO.output(out4, GPIO.HIGH)
            GPIO.output(out3, GPIO.HIGH)
            GPIO.output(out2, GPIO.LOW)
            GPIO.output(out1, GPIO.LOW)
        time.sleep(step_sleep)
    
def get_data():
    try:
        # Start the PWM with an initial duty cycle of 0% (servo remains in its default position) 
        servo.start(0) 
        for i in range(15, 0, -3):
            servo.ChangeDutyCycle(i)
            lcd.printer(str(ultrasonic.distance),"")
            stepper_motor(100)
        servo.stop()
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit(1)
            
    
def cleanup():
    GPIO.output(motor1_forward, GPIO.LOW)
    GPIO.output(motor2_forward, GPIO.LOW)
    GPIO.output(motor1_backward, GPIO.LOW)
    GPIO.output(motor2_backward, GPIO.LOW)
    GPIO.output(out1, GPIO.LOW)
    GPIO.output(out2, GPIO.LOW)
    GPIO.output(out3, GPIO.LOW)
    GPIO.output(out4, GPIO.LOW)
    lcd.cleanup()
    GPIO.cleanup()
 
def step1():
    GPIO.output(status_LED, GPIO.HIGH)
    lcd.printer("Hello", "")
    
def step2():  
    buzz(2, 80)
    lcd.printer("Moving Forward", "")
    GPIO.output(led1, GPIO.HIGH)
    GPIO.output(led2, GPIO.HIGH)
    forward(4)
    get_data()
 
def step3():
    lcd.printer("Pause", "")
    GPIO.output(led1, GPIO.LOW)
    GPIO.output(led2, GPIO.LOW)
    GPIO.output(status_LED, GPIO.LOW)
    time.sleep(4)
    
    
def step4():
    buzz(1, 50)
    status_LED_PWM = GPIO.PWM(status_LED,500)
    status_LED_PWM.start(20)
    backward(4)
 
def step5():
    status_LED_PWM = GPIO.PWM(status_LED,500)
    status_LED_PWM.stop()
    lcd.printer("Goodbye", "")
    time.sleep(2)
    lcd.printer("", "")
    
 
step1()
step2()
step3()
step4()
step5()
 
# Part three
 
def turn(direction):
    if direction == "Right":
        GPIO.output(motor1_forward, GPIO.HIGH)
        GPIO.output(motor2_backward, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(motor1_forward, GPIO.LOW)
        GPIO.output(motor2_backward, GPIO.LOW)
    elif direction == "Left":
        GPIO.output(motor1_backward, GPIO.HIGH)
        GPIO.output(motor2_forward, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(motor1_backward, GPIO.LOW)
        GPIO.output(motor2_forward, GPIO.LOW)
    else:
        print("Invalid input")
try: 
    direction = str(input("Choose direction: "))
except ValueError:
    print("Invalid input")
    
    
turn(direction)
cleanup()
