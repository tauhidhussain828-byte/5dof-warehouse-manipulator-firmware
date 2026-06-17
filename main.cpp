#include <Arduino.h>
#include <HardwareSerial.h>
#include <ESP32Servo.h> 

// --- Hardware Pin Configurations ---
#define TXD_PIN            17
#define RXD_PIN            16
#define RX_BUF_SIZE        1024

// Servo Pins
#define SERVO_BASE_PIN     18 // Joint 1: MG996R
#define SERVO_SHLDR_PIN    19 // Joint 2: MG996R
#define SERVO_ELBOW_PIN    21 // Joint 3: MG996R
#define SERVO_WRIST_PIN    22 // Joint 4: MG90S
#define SERVO_GRIP_PIN     23 // Joint 5: MG90S

// Create Servo Objects using the dedicated ESP32 library
Servo servoBase;
Servo servoShoulder;
Servo servoElbow;
Servo servoWrist;
Servo servoGripper;

// Setup custom serial port for communication with LattePanda Mu
HardwareSerial PandaSerial(1);

// --- FIX: Function defined HERE first so setup() can see it safely ---
void actuate_arm(int base, int shoulder, int elbow, int wrist, int gripper) {
    servoBase.write(base);
    servoShoulder.write(shoulder);
    servoElbow.write(elbow);
    servoWrist.write(wrist);
    servoGripper.write(gripper);
}

void setup() {
    // Initialize high-speed serial communication line
    PandaSerial.begin(115200, SERIAL_8N1, RXD_PIN, TXD_PIN);
    
    // Attach servos safely with accurate microsecond pulse limits for MG996R/MG90S
    servoBase.attach(SERVO_BASE_PIN, 500, 2500);
    servoShoulder.attach(SERVO_SHLDR_PIN, 500, 2500);
    servoElbow.attach(SERVO_ELBOW_PIN, 500, 2500);
    servoWrist.attach(SERVO_WRIST_PIN, 500, 2500);
    servoGripper.attach(SERVO_GRIP_PIN, 500, 2500);

    // Default startup position: 90-degree midpoint
    actuate_arm(90, 90, 90, 90, 90);
}

void loop() {
    if (PandaSerial.available() > 0) {
        String rx_buffer = PandaSerial.readStringUntil('\n');
        
        // Expected String format: "ARM:90,45,120,90,1"
        if (rx_buffer.startsWith("ARM:")) {
            long b = 0, s = 0, e = 0, w = 0, g = 0;
            
            // Parse strings using native tokenization
            int parse_count = sscanf(rx_buffer.c_str(), "ARM:%ld,%ld,%ld,%ld,%ld", &b, &s, &e, &w, &g);
            
            if (parse_count == 5) {
                actuate_arm(b, s, e, w, g);
                
                // Transmit handshake acknowledgment back to high-level computer
                PandaSerial.println("ACK_EXEC_SUCCESS");
            }
        }
    }
}