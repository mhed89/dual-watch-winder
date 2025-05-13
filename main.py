from machine import Pin
from time import sleep
try:
    from machine import deepsleep
except ImportError:
    deepsleep = None

# Define GPIO pins connected to IN1-IN4 on ULN2003 for Motor A
IN1 = Pin(16, Pin.OUT)
IN2 = Pin(17, Pin.OUT)
IN3 = Pin(18, Pin.OUT)
IN4 = Pin(19, Pin.OUT)

# Define GPIO pins connected to IN1-IN4 on ULN2003 for Motor B
IN1_B = Pin(20, Pin.OUT)
IN2_B = Pin(21, Pin.OUT)
IN3_B = Pin(22, Pin.OUT)
IN4_B = Pin(26, Pin.OUT)

# Step sequence for 28BYJ-48
step_sequence = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1],
]

def set_step(pins, motor='A'):
    if motor == 'A':
        IN1.value(pins[0])
        IN2.value(pins[1])
        IN3.value(pins[2])
        IN4.value(pins[3])
    else:
        IN1_B.value(pins[0])
        IN2_B.value(pins[1])
        IN3_B.value(pins[2])
        IN4_B.value(pins[3])

def step_motor(steps, direction=1, delay=0.001, motor='A'):
    for _ in range(steps):
        for i in range(8)[::direction]:
            set_step(step_sequence[i], motor)
            sleep(delay)

def wind_watch(rotations=2):
    STEPS_PER_REV = 4096
    # Both motors forward
    for _ in range(rotations):
        step_motor(STEPS_PER_REV, direction=1, motor='A')
        step_motor(STEPS_PER_REV, direction=1, motor='B')
    # Both motors backward
    for _ in range(rotations):
        step_motor(STEPS_PER_REV, direction=-1, motor='A')
        step_motor(STEPS_PER_REV, direction=-1, motor='B')

while True:
    wind_watch(rotations=2)
    if deepsleep:
        deepsleep(20 * 60 * 1000)
    else:
        sleep(20 * 60)