# 🤖 Quantheonix Robotics

# QXP04V01 - Autonomous Maze Solver

An autonomous maze-solving robot developed using the Webots simulator and the e-puck robot platform.

The robot navigates unknown static mazes using the **Left-Hand Rule** navigation algorithm combined with a **Finite State Machine (FSM)**. Navigation decisions are made using only proximity sensors without cameras, GPS, or external localization.

---

## Features

- Autonomous maze navigation
- Left-Hand Rule algorithm
- Finite State Machine (FSM)
- Left, right and dead-end handling
- Stable junction confirmation
- Proximity sensor-based wall detection
- Differential drive motion control
- Navigation statistics

---

## Technology Stack

- Webots R2025
- Python
- e-puck Robot

---

## Project Structure

```
QXP04V01_Autonomous_Maze_Solver/
│
├── controllers/
│   └── maze_solver/
│       └── maze_solver.py
│
├── worlds/
│
├── README.md
├── ABOUT.md
├── TEST.md
└── CHANGELOG.md
```

---

## Navigation Algorithm

```
IF Left Open
    Turn Left

ELSE IF Front Open
    Move Forward

ELSE IF Right Open
    Turn Right

ELSE
    Turn Around
```

---

## Current Status

✅ Completed

---

## Future Improvements

- Maze mapping
- SLAM
- Shortest-path planning
- Computer vision
- Dynamic obstacle avoidance

These features will be implemented in future Quantheonix Robotics projects.

---

**Project:** QXP04V01  
**Developer:** Quantheonix Robotics