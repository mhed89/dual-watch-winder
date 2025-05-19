from machine import Pin
from time import sleep

# Note: Deep sleep works on RP2350 (Pico 2) but not on RP2040 (Pico 1)
try:
    from machine import deepsleep
except ImportError:
    deepsleep = None
from lib.power_ctrl_2350 import PowerCtrl

# Initialize PowerCtrl
pwr = PowerCtrl()

# Permanently disable unused hardware blocks
pwr.disable_while_sleeping(
    pwr.EN1_CLK_SYS_USBCTRL,  # USB controller
    pwr.EN1_CLK_SYS_UART1,    # UART1
    pwr.EN1_CLK_SYS_UART0,    # UART0
    pwr.EN1_CLK_SYS_TRNG      # True Random Number Generator
)

# Optimize sleep mode
pwr.disable_while_sleeping(
    pwr.EN1_CLK_SYS_XIP,      # Execute-in-place memory
    pwr.EN1_CLK_SYS_SRAM9,    # SRAM blocks
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

# Define GPIO pin for the onboard LED
LED_PIN = Pin(25, Pin.OUT)  # GPIO 25 is the onboard LED

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

def step_motor(steps, direction=1, delay=0.005, motor='A'):
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
    # Power saving: enter deep sleep for 30 minutes if available, else normal sleep
    if deepsleep:
        print("Entering deep sleep for 30 minutes...")  # Temporary debug statement
        LED_PIN.value(1)  # Turn on onboard LED
        deepsleep(30 * 60 * 1000)  # 30 minutes in milliseconds
    else:
        print("Sleeping for 30 minutes...")  # Temporary debug statement
        LED_PIN.value(1)  # Turn on onboard LED
        sleep(30 * 60)  # 30 minutes in seconds
    LED_PIN.value(0)  # Turn off onboard LED after waking up
