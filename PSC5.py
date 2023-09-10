import RPi.GPIO as GPIO
import time
import logging
import asyncio
import tkinter as tk

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

def custom_angle():
    angle = int(custom_angle_entry.get())
    if 0 <= angle <= 180:
        set_servo_angle(angle)
    else:
        logging.warning("Invalid angle. Please enter a value between 0 and 180.")

def create_gui():
    global custom_angle_entry
    root = tk.Tk()
    root.title("Servo Control")

    tk.Button(root, text="Move to Middle Position", command=alltomiddle).pack()
    tk.Button(root, text="Move to Rest Position", command=alltorest).pack()
    tk.Button(root, text="Move to Max Position", command=alltomax).pack()

    custom_angle_frame = tk.Frame(root)
    custom_angle_frame.pack()
    tk.Label(custom_angle_frame, text="Custom Angle (0-180):").pack(side=tk.LEFT)
    custom_angle_entry = tk.Entry(custom_angle_frame)
    custom_angle_entry.pack(side=tk.LEFT)
    tk.Button(custom_angle_frame, text="Set Angle", command=custom_angle).pack(side=tk.LEFT)

    tk.Button(root, text="Quit", command=root.quit).pack()

    return root

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    global pwm
    pwm = GPIO.PWM(SERVO_PIN, 50)
    pwm.start(0)

    try:
        logging.info("Servo control started.")
        root = create_gui()
        root.mainloop()

    except KeyboardInterrupt:
        pass
    finally:
        pwm.stop()
        GPIO.cleanup()
        logging.info("Servo control stopped.")

if __name__ == "__main__":
    main()

