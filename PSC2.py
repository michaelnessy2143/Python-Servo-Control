import RPi.GPIO as GPIO
import time
import logging

SERVO_PIN = 3

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def set_servo_angle(angle):
    try:
        duty = angle / 18 + 2
        GPIO.output(SERVO_PIN, True)
        pwm.ChangeDutyCycle(duty)
        time.sleep(1)
        GPIO.output(SERVO_PIN, False)
        pwm.ChangeDutyCycle(0)
        logging.info(f"Servo angle set to {angle} degrees")
    except Exception as e:
        logging.error(f"An error occurred while setting the servo angle: {e}")

def alltomiddle():
    set_servo_angle(90)

def alltorest():
    set_servo_angle(0)

def alltomax():
    set_servo_angle(180)

def process_command(command):
    try:
        if command == '1':
            alltomiddle()
        elif command == '2':
            alltorest()
        elif command == '3':
            alltomax()
        elif command == '4':
            angle = int(input("Enter a custom angle (0-180): "))
            if 0 <= angle <= 180:
                set_servo_angle(angle)
            else:
                logging.warning("Invalid angle. Please enter a value between 0 and 180.")
        else:
            logging.warning("Invalid selection. Please choose a valid option from the menu.")
    except Exception as e:
        logging.error(f"An error occurred while processing the command: {e}")

def display_menu():
    print("\nServo Control Menu:")
    print("1. Move to Middle Position")
    print("2. Move to Rest Position")
    print("3. Move to Max Position")
    print("4. Enter Custom Angle")
    print("q. Quit")
    return input("Please select an option: ")

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

try:
    logging.info("Servo control started.")
    while True:
        command = display_menu().strip().lower()
        if command == 'q':
            break
        process_command(command)

except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()
    logging.info("Servo control stopped.")

