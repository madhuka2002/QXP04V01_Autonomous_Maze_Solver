from controller import Robot

TIME_STEP = 64
BASE_SPEED = 3.0
CORRECTION = 0.8
THRESHOLD = 80

FORWARD_SPEED = 3.0
TURN_SPEED = 2.0

robot = Robot()

left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")

left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))

left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

sensor_names = [
    "ps0",
    "ps1",
    "ps2",
    "ps3",
    "ps4",
    "ps5",
    "ps6",
    "ps7"
]

sensors = []

for name in sensor_names:
    sensor = robot.getDevice(name)
    sensor.enable(TIME_STEP)
    sensors.append(sensor)


def left_wall():
    return (
        sensors[5].getValue() > THRESHOLD
        or sensors[6].getValue() > THRESHOLD
    )


def front_wall():
    return (
        sensors[0].getValue() > THRESHOLD
        or sensors[7].getValue() > THRESHOLD
    )


def right_wall():
    return (
        sensors[1].getValue() > THRESHOLD
        or sensors[2].getValue() > THRESHOLD
    )


def stop():
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)


def move_forward(duration = 10):
    left_motor.setVelocity(BASE_SPEED)
    right_motor.setVelocity(BASE_SPEED)

    for _ in range(duration):
        robot.step(TIME_STEP)

    stop()


def turn_left():
    left_motor.setVelocity(-TURN_SPEED)
    right_motor.setVelocity(TURN_SPEED)

    for _ in range(12):
        robot.step(TIME_STEP)

    stop()


def turn_right():
    left_motor.setVelocity(TURN_SPEED)
    right_motor.setVelocity(-TURN_SPEED)

    for _ in range(12):
        robot.step(TIME_STEP)

    stop()


def turn_around():
    left_motor.setVelocity(TURN_SPEED)
    right_motor.setVelocity(-TURN_SPEED)

    for _ in range(24):
        robot.step(TIME_STEP)

    stop()


def steer_left():
    left_motor.setVelocity(BASE_SPEED - CORRECTION)
    right_motor.setVelocity(BASE_SPEED + CORRECTION)


def steer_right():
    left_motor.setVelocity(BASE_SPEED + CORRECTION)
    right_motor.setVelocity(BASE_SPEED - CORRECTION)


while robot.step(TIME_STEP) != -1:

    left = left_wall()
    front = front_wall()
    right = right_wall()

    print(f"L:{left} F:{front} R:{right}")

    # Wall directly ahead
    if front:

        if not left:
            turn_left()

        elif not right:
            turn_right()

        else:
            turn_around()

    # Corridor
    else:

        if left:
            steer_right()      # Too close to left wall
        elif right:
            steer_left()       # Too close to right wall
        else:
            move_forward()