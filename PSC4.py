import RPi.GPIO as GPIO
import time
import logging
import asyncio

SERVO_PIN_1 = 3  # Pin number for servo 1
SERVO_PIN_2 = 4  # Pin number for servo 2

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to set the servo angle
async def set_servo_angle(pin, angle):
    try:
        duty = angle / 18 + 2
        GPIO.output(pin, True)
        pwm[pin].ChangeDutyCycle(duty)
        await asyncio.sleep(1)  # Non-blocking sleep
        GPIO.output(pin, False)
        pwm[pin].ChangeDutyCycle(0)
        logging.info(f"Servo on pin {pin} set to {angle} degrees")
    except Exception as e:
        logging.error(f"An error occurred while setting the servo angle: {e}")

# Move both servos to a custom angle concurrently
async def move_servos_to_custom_angle():
    angle1 = int(input("Enter a custom angle for servo 1 (0-180): "))
    angle2 = int(input("Enter a custom angle for servo 2 (0-180): "))
    
    # Execute both functions concurrently
    await asyncio.gather(
        set_servo_angle(SERVO_PIN_1, angle1),
        set_servo_angle(SERVO_PIN_2, angle2)
    )

async def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN_1, GPIO.OUT)
    GPIO.setup(SERVO_PIN_2, GPIO.OUT)
    global pwm
    pwm = {
        SERVO_PIN_1: GPIO.PWM(SERVO_PIN_1, 50),
        SERVO_PIN_2: GPIO.PWM(SERVO_PIN_2, 50)
    }
    pwm[SERVO_PIN_1].start(0)
    pwm[SERVO_PIN_2].start(0)

    try:
        logging.info("Servo control started.")
        await move_servos_to_custom_angle()  # Call the asynchronous function

    except KeyboardInterrupt:
        pass
    finally:
        pwm[SERVO_PIN_1].stop()
        pwm[SERVO_PIN_2].stop()
        GPIO.cleanup()
        logging.info("Servo control stopped.")

if __name__ == "__main__":
    asyncio.run(main())

