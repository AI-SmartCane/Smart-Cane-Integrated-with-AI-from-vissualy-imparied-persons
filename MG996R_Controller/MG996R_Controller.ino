#include <Servo.h>

Servo myServo;

const int SERVO_PIN = 9;
int currentAngle = 90;

void moveServo(int targetAngle) {

  if (targetAngle > currentAngle) {
    for (int angle = currentAngle; angle <= targetAngle; angle++) {
      myServo.write(angle);
      delay(20);
    }
  }
  else {
    for (int angle = currentAngle; angle >= targetAngle; angle--) {
      myServo.write(angle);
      delay(20);
    }
  }

  currentAngle = targetAngle;
}

void setup() {
  Serial.begin(115200);

  myServo.attach(SERVO_PIN);
  myServo.write(90);

  delay(500);
  Serial.println("Servo ready");
}

void loop() {

  if (Serial.available()) {

    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "MOVE_LEFT") {
      moveServo(60);
    }

    else if (command == "MOVE_RIGHT") {
      moveServo(120);
    }

    else if (command == "GO_FORWARD") {
      moveServo(90);
    }

    else if (command == "STOP") {
      moveServo(90);
    }
  }
}
