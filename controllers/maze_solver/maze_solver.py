from controller import Robot

# ==========================================================
# CONFIGURATION
# ==========================================================

TIME_STEP = 64

FORWARD_SPEED = 3.0
TURN_SPEED = 2.0

SIDE_THRESHOLD = 100
FRONT_THRESHOLD = 180

TURN_90_STEPS = 17
TURN_180_STEPS = 35

CLEAR_JUNCTION_STEPS = 10

# Number of consecutive readings required before confirming
# an opening or obstacle.
JUNCTION_CONFIRM_STEPS = 3
FRONT_CONFIRM_STEPS = 2


# ==========================================================
# ROBOT INITIALIZATION
# ==========================================================

robot = Robot()

left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")

if left_motor is None or right_motor is None:
    raise RuntimeError("Wheel motors were not found.")

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
        raise RuntimeError(f"Sensor '{name}' was not found.")

    sensor.enable(TIME_STEP)
    sensors.append(sensor)


# Allow sensors to initialize.
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
# SENSOR CONFIRMATION COUNTERS
# ==========================================================

left_open_counter = 0
right_open_counter = 0
front_blocked_counter = 0


def reset_detection_counters():
    global left_open_counter
    global right_open_counter
    global front_blocked_counter

    left_open_counter = 0
    right_open_counter = 0
    front_blocked_counter = 0


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
    # COMPLETE LEFT TURN
    # ------------------------------------------------------

    if state == STATE_TURN_LEFT:
        steps_remaining -= 1

        if steps_remaining <= 0:
            move_forward()
            steps_remaining = CLEAR_JUNCTION_STEPS
            state = STATE_CLEAR_JUNCTION

        continue

    # ------------------------------------------------------
    # COMPLETE RIGHT TURN
    # ------------------------------------------------------

    if state == STATE_TURN_RIGHT:
        steps_remaining -= 1

        if steps_remaining <= 0:
            move_forward()
            steps_remaining = CLEAR_JUNCTION_STEPS
            state = STATE_CLEAR_JUNCTION

        continue

    # ------------------------------------------------------
    # COMPLETE TURNAROUND
    # ------------------------------------------------------

    if state == STATE_TURN_AROUND:
        steps_remaining -= 1

        if steps_remaining <= 0:
            move_forward()
            steps_remaining = CLEAR_JUNCTION_STEPS
            state = STATE_CLEAR_JUNCTION

        continue

    # ------------------------------------------------------
    # CLEAR CURRENT JUNCTION
    # ------------------------------------------------------

    if state == STATE_CLEAR_JUNCTION:
        steps_remaining -= 1

        if steps_remaining <= 0:
            reset_detection_counters()
            state = STATE_NAVIGATE

        continue

    # ------------------------------------------------------
    # READ SURROUNDINGS
    # ------------------------------------------------------

    left = left_wall()
    front = front_wall()
    right = right_wall()

    print(
        f"Walls | "
        f"L:{left} "
        f"F:{front} "
        f"R:{right}"
    )

    # ------------------------------------------------------
    # UPDATE SENSOR CONFIRMATION COUNTERS
    # ------------------------------------------------------

    if not left:
        left_open_counter += 1
    else:
        left_open_counter = 0

    if not right:
        right_open_counter += 1
    else:
        right_open_counter = 0

    if front:
        front_blocked_counter += 1
    else:
        front_blocked_counter = 0

    left_open_confirmed = (
        left_open_counter >= JUNCTION_CONFIRM_STEPS
    )

    right_open_confirmed = (
        right_open_counter >= JUNCTION_CONFIRM_STEPS
    )

    front_blocked_confirmed = (
        front_blocked_counter >= FRONT_CONFIRM_STEPS
    )

    # ======================================================
    # LEFT-HAND RULE
    # ======================================================

    # Confirmed left opening at a corner or junction.
    if left_open_confirmed and (front or right):
        decision_count += 1
        left_turns += 1

        print(
            f"Decision #{decision_count}: "
            "Confirmed Left Turn"
        )

        reset_detection_counters()

        start_left_turn()
        steps_remaining = TURN_90_STEPS
        state = STATE_TURN_LEFT

    # Front is open, so continue moving forward.
    elif not front:
        move_forward()
        print("Action: Forward")

    # Front is blocked and right side is confirmed open.
    elif front_blocked_confirmed and right_open_confirmed:
        decision_count += 1
        right_turns += 1

        print(
            f"Decision #{decision_count}: "
            "Confirmed Right Turn"
        )

        reset_detection_counters()

        start_right_turn()
        steps_remaining = TURN_90_STEPS
        state = STATE_TURN_RIGHT

    # Front, left and right are blocked.
    elif (
        front_blocked_confirmed
        and left
        and right
    ):
        decision_count += 1
        turn_arounds += 1

        print(
            f"Decision #{decision_count}: "
            "Confirmed Dead End - Turn Around"
        )

        reset_detection_counters()

        start_turn_around()
        steps_remaining = TURN_180_STEPS
        state = STATE_TURN_AROUND

    # Wait for enough stable readings.
    else:
        move_forward()
        print(
            "Action: Waiting for stable decision "
            f"| LeftCounter:{left_open_counter} "
            f"RightCounter:{right_open_counter} "
            f"FrontCounter:{front_blocked_counter}"
        )


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