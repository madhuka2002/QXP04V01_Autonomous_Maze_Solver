from controller import Robot

# ==========================================================
# CONFIGURATION
# ==========================================================

TIME_STEP = 64

FORWARD_SPEED = 3.0
TURN_SPEED = 2.0

SIDE_THRESHOLD = 100
FRONT_THRESHOLD = 180

TURN_90_STEPS = 17.25
TURN_180_STEPS = 34.5

CLEAR_JUNCTION_STEPS = 10


# ==========================================================
# ROBOT INITIALIZATION
# ==========================================================

robot = Robot()

left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")

left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))

left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)


# ==========================================================
# SENSOR INITIALIZATION
# ==========================================================

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

    if sensor is None:
        print(f"ERROR: Sensor '{name}' was not found.")
        raise RuntimeError(f"Missing sensor: {name}")

    sensor.enable(TIME_STEP)
    sensors.append(sensor)


# Allow proximity sensors to initialize
if robot.step(TIME_STEP) == -1:
    raise RuntimeError("Simulation ended during initialization.")


# ==========================================================
# WALL DETECTION
# ==========================================================

def left_wall():
    return (
        sensors[5].getValue() > SIDE_THRESHOLD
        or sensors[6].getValue() > SIDE_THRESHOLD
    )


def front_wall():
    return (
        sensors[0].getValue() > FRONT_THRESHOLD
        or sensors[7].getValue() > FRONT_THRESHOLD
    )


def right_wall():
    return (
        sensors[1].getValue() > SIDE_THRESHOLD
        or sensors[2].getValue() > SIDE_THRESHOLD
    )


# ==========================================================
# MOTOR CONTROL
# ==========================================================

def stop():
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)


def move_forward():
    left_motor.setVelocity(FORWARD_SPEED)
    right_motor.setVelocity(FORWARD_SPEED)


def start_left_turn():
    left_motor.setVelocity(-TURN_SPEED)
    right_motor.setVelocity(TURN_SPEED)


def start_right_turn():
    left_motor.setVelocity(TURN_SPEED)
    right_motor.setVelocity(-TURN_SPEED)


def start_turn_around():
    left_motor.setVelocity(TURN_SPEED)
    right_motor.setVelocity(-TURN_SPEED)


# ==========================================================
# CONTROLLER STATES
# ==========================================================

STATE_NAVIGATE = "NAVIGATE"
STATE_TURN_LEFT = "TURN_LEFT"
STATE_TURN_RIGHT = "TURN_RIGHT"
STATE_TURN_AROUND = "TURN_AROUND"
STATE_CLEAR_JUNCTION = "CLEAR_JUNCTION"

state = STATE_NAVIGATE
steps_remaining = 0


# ==========================================================
# NAVIGATION STATISTICS
# ==========================================================

decision_count = 0
left_turns = 0
right_turns = 0
turn_arounds = 0

simulation_start_time = robot.getTime()


# ==========================================================
# MAIN CONTROLLER LOOP
# ==========================================================

while robot.step(TIME_STEP) != -1:

    # ------------------------------------------------------
    # LEFT TURN STATE
    # ------------------------------------------------------

    if state == STATE_TURN_LEFT:
        steps_remaining -= 1

        if steps_remaining <= 0:
            move_forward()
            steps_remaining = CLEAR_JUNCTION_STEPS
            state = STATE_CLEAR_JUNCTION

        continue

    # ------------------------------------------------------
    # RIGHT TURN STATE
    # ------------------------------------------------------

    if state == STATE_TURN_RIGHT:
        steps_remaining -= 1

        if steps_remaining <= 0:
            move_forward()
            steps_remaining = CLEAR_JUNCTION_STEPS
            state = STATE_CLEAR_JUNCTION

        continue

    # ------------------------------------------------------
    # TURN AROUND STATE
    # ------------------------------------------------------

    if state == STATE_TURN_AROUND:
        steps_remaining -= 1

        if steps_remaining <= 0:
            move_forward()
            steps_remaining = CLEAR_JUNCTION_STEPS
            state = STATE_CLEAR_JUNCTION

        continue

    # ------------------------------------------------------
    # CLEAR JUNCTION STATE
    # ------------------------------------------------------

    if state == STATE_CLEAR_JUNCTION:
        steps_remaining -= 1

        if steps_remaining <= 0:
            state = STATE_NAVIGATE

        continue

    # ------------------------------------------------------
    # READ SURROUNDINGS
    # ------------------------------------------------------

    left = left_wall()
    front = front_wall()
    right = right_wall()

    print(
        f"L:{left} "
        f"F:{front} "
        f"R:{right}"
    )

    # ======================================================
    # LEFT-HAND RULE
    # ======================================================

    # Completely open area
    if not left and not front and not right:
        move_forward()
        print("Action: Forward through open area")

    # Left opening available
    elif not left and (front or right):
        decision_count += 1
        left_turns += 1

        print(
            f"Decision #{decision_count}: "
            "Turn Left"
        )

        start_left_turn()
        steps_remaining = TURN_90_STEPS
        state = STATE_TURN_LEFT

    # Front path available
    elif not front:
        move_forward()
        print("Action: Forward")

    # Right opening available
    elif not right:
        decision_count += 1
        right_turns += 1

        print(
            f"Decision #{decision_count}: "
            "Turn Right"
        )

        start_right_turn()
        steps_remaining = TURN_90_STEPS
        state = STATE_TURN_RIGHT

    # Dead end
    else:
        decision_count += 1
        turn_arounds += 1

        print(
            f"Decision #{decision_count}: "
            "Dead End - Turn Around"
        )

        start_turn_around()
        steps_remaining = TURN_180_STEPS
        state = STATE_TURN_AROUND


# ==========================================================
# SIMULATION ENDED
# ==========================================================

stop()

completion_time = robot.getTime() - simulation_start_time

print()
print("========================================")
print("       QXP04 CONTROLLER STOPPED")
print("========================================")
print(f"Runtime         : {completion_time:.2f} seconds")
print(f"Total decisions : {decision_count}")
print(f"Left turns      : {left_turns}")
print(f"Right turns     : {right_turns}")
print(f"Turnarounds     : {turn_arounds}")
print("========================================")