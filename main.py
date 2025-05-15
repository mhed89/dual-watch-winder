from machine import Pin
from time import sleep
from lib.power_ctrl_2350 import PowerCtrl

# Motor A
IN1 = Pin(16, Pin.OUT)
IN2 = Pin(17, Pin.OUT)
IN3 = Pin(18, Pin.OUT)
IN4 = Pin(19, Pin.OUT)

# Motor B
IN1_B = Pin(20, Pin.OUT)
IN2_B = Pin(21, Pin.OUT)
IN3_B = Pin(22, Pin.OUT)
IN4_B = Pin(26, Pin.OUT)

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
    for _ in range(rotations):
        step_motor(STEPS_PER_REV, direction=1, motor='A')
        step_motor(STEPS_PER_REV, direction=1, motor='B')
    for _ in range(rotations):
        step_motor(STEPS_PER_REV, direction=-1, motor='A')
        step_motor(STEPS_PER_REV, direction=-1, motor='B')

pwr = PowerCtrl()

while True:
    wind_watch(rotations=2)
    pwr.disable_while_sleeping(
        pwr.EN1_CLK_SYS_XIP,
        pwr.EN1_CLK_SYS_SRAM9,
        pwr.EN1_CLK_SYS_SRAM8,
        pwr.EN1_CLK_SYS_SRAM7,
        pwr.EN1_CLK_SYS_SRAM6,
        pwr.EN1_CLK_SYS_SRAM5,
        pwr.EN1_CLK_SYS_SRAM4,
        pwr.EN1_CLK_SYS_SRAM3,
        pwr.EN1_CLK_SYS_SRAM2,
        pwr.EN1_CLK_SYS_SRAM1,
        pwr.EN1_CLK_SYS_SRAM0
    )
    # Set all motor pins to low
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)
    IN1_B.value(0)
    IN2_B.value(0)
    IN3_B.value(0)
    IN4_B.value(0)
    sleep(30 * 60)