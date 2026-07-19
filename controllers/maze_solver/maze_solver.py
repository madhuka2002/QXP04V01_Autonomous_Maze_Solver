from controller import Robot

TIME_STEP = 64
MAX_SPEED = 6.28

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

while robot.step(TIME_STEP) != -1:
    values = [sensor.getValue() for sensor in sensors]
    
    print(
        f"Front Right: {values[0]:.2f} | "
        f"Front: {values[7]:.2f} | "
        f"Left: {values[5]:.2f} | "
    )
    
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)