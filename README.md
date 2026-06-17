## System Architecture & Data Flow

The warehouse automation system uses a distributed edge computing model split between high-level perception on a host PC (LattePanda Mu) and low-level execution on an ESP32 microcontroller:

1. 📷 **The Scanner (Python + OpenCV/YOLO):** Captures real-time video feeds of packages on the warehouse shelves, detects object labels, and extracts destination metadata.
2. 🧠 **The Decider (Python Routing Logic):** Evaluates the scanned data, determines the correct sorting bin destination, and executes inverse kinematics to calculate precise joint angles. It formats these into a serial instruction string.
3. ⚙️ **The Actuator (This ESP32 Core):** Receives the string payload over a dedicated high-speed UART line at 115200 baud, decodes the coordinates, handles hardware PWM distribution to the 5-DOF manipulator, and returns an execution handshake acknowledgment (`ACK`).
