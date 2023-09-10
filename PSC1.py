import RPi.GPIO as GPIO
import time

SERVO_PIN = 3

# Function to set the servo angle
def set_servo_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(SERVO_PIN, False)
    pwm.ChangeDutyCycle(0)

def alltomiddle():
    set_servo_angle(90)

def alltorest():
    set_servo_angle(0)

def alltomax():
    set_servo_angle(180)

# Initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
pwm = GPIO.PWM(SERVO_PIN, 50) # 50Hz frequency
pwm.start(0)

try:
    while True:
        command = input("Enter the servo position (middle, rest, max) or an angle value (0-180): ").strip().lower()
        if command == "middle":
            alltomiddle()
        elif command == "rest":
            alltorest()
        elif command == "max":
            alltomax()
        elif command.isdigit() and 0 <= int(command) <= 180:
            angle = int(command)
            set_servo_angle(angle)
        else:
            print("Invalid command. Please enter 'middle', 'rest', 'max', or a value between 0 and 180.")

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()

