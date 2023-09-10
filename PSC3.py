import RPi.GPIO as GPIO
import time
import logging
import asyncio

SERVO_PIN = 3  # Pin number for servo control

# Configure logging to print messages to the terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to set the servo angle
def set_servo_angle(angle):
    try:
        duty = angle / 18 + 2  # Calculate duty cycle from angle
        GPIO.output(SERVO_PIN, True)
        pwm.ChangeDutyCycle(duty)
        time.sleep(1)
        GPIO.output(SERVO_PIN, False)
        pwm.ChangeDutyCycle(0)
        logging.info(f"Servo angle set to {angle} degrees")
    except Exception as e:
        logging.error(f"An error occurred while setting the servo angle: {e}")
        return False
    return True

# Functions to move the servo to predefined positions
def alltomiddle():
    return set_servo_angle(90)

def alltorest():
    return set_servo_angle(0)

def alltomax():
    return set_servo_angle(180)

# Process user's command from the menu
def process_command(command):
    try:
        if command == '1':
            return alltomiddle()
        elif command == '2':
            return alltorest()
        elif command == '3':
            return alltomax()
        elif command == '4':
            angle = int(input("Enter a custom angle (0-180): "))
            if 0 <= angle <= 180:
                return set_servo_angle(angle)
            else:
                logging.warning("Invalid angle. Please enter a value between 0 and 180.")
                return False
        else:
            logging.warning("Invalid selection. Please choose a valid option from the menu.")
            return False
    except Exception as e:
        logging.error(f"An error occurred while processing the command: {e}")
        return False

# Display the control menu to the user
def display_menu():
    print("\nServo Control Menu:")
    print("1. Move to Middle Position")
    print("2. Move to Rest Position")
    print("3. Move to Max Position")
    print("4. Enter Custom Angle")
    print("q. Quit")
    return input("Please select an option: ")

# Main asynchronous function
async def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    global pwm
    pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz frequency
    pwm.start(0)

    try:
        logging.info("Servo control started.")
        while True:
            command = display_menu().strip().lower()
            if command == 'q':
                break
            process_command(command)
            await asyncio.sleep(0)  # Yield control to event loop

    except KeyboardInterrupt:
        pass
    finally:
        pwm.stop()
        GPIO.cleanup()
        logging.info("Servo control stopped.")

# Entry point for the script
if __name__ == "__main__":
    asyncio.run(main())

