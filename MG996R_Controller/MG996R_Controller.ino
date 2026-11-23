#include <Servo.h>

Servo myServo;

const int SERVO_PIN  = 9;
const int SWITCH_PIN = 2;
const int AUDIO_PIN  = 11;            // OC2A (Timer2 PWM)

int currentAngle = 90;
unsigned long lastReport = 0;

const uint16_t BUF_SIZE = 512;        // must be a power of 2
const uint16_t CHUNK    = 64;         // bytes the Jetson sends per "K" request
volatile uint8_t  audioBuf[BUF_SIZE];
volatile uint16_t headIdx = 0;
volatile uint16_t tailIdx = 0;
volatile uint8_t  silenceLevel = 0;
volatile uint8_t  divider = 0;

// Timer2 overflows at 62.5 kHz; every 8th overflow plays one sample = 7812.5 Hz
ISR(TIMER2_OVF_vect) {
  if (++divider < 8) return;
  divider = 0;
  if (tailIdx != headIdx) {
    OCR2A = audioBuf[tailIdx];
    tailIdx = (tailIdx + 1) & (BUF_SIZE - 1);
  } else {
    OCR2A = silenceLevel;
  }
}

uint16_t readTail() {
  noInterrupts();
  uint16_t t = tailIdx;
  interrupts();
  return t;
}

void audioStart() {
  headIdx = 0;
  tailIdx = 0;
  silenceLevel = 0;
  OCR2A = 0;
  pinMode(AUDIO_PIN, OUTPUT);
  TCCR2A = _BV(COM2A1) | _BV(WGM21) | _BV(WGM20);
  TCCR2B = _BV(CS20);
  TIMSK2 = _BV(TOIE2);
  for (int v = 0; v <= 128; v += 4) {
    silenceLevel = v;
    delay(2);
  }
}

void audioStop() {
  for (int v = 128; v >= 0; v -= 4) {
    silenceLevel = v;
    delay(2);
  }
  TIMSK2 = 0;
  TCCR2A = 0;
  TCCR2B = 0;
  digitalWrite(AUDIO_PIN, LOW);
}

void reportSwitch() {
  if (millis() - lastReport >= 50) {
    lastReport = millis();
    if (digitalRead(SWITCH_PIN) == LOW) {
      Serial.println("SWITCH_ON");
    } else {
      Serial.println("SWITCH_OFF");
    }
  }
}

void playAudio(long total) {
  long requested = 0;
  long received  = 0;
  unsigned long lastData = millis();

  audioStart();

  while (received < total || readTail() != headIdx) {
    while (Serial.available() && received < total) {
      audioBuf[headIdx] = (uint8_t)Serial.read();
      headIdx = (headIdx + 1) & (BUF_SIZE - 1);
      received++;
      lastData = millis();
    }

    uint16_t used = (headIdx - readTail()) & (BUF_SIZE - 1);
    long inflight = requested - received;
    while (requested < total &&
           (long)used + inflight + (long)CHUNK < (long)(BUF_SIZE - 8)) {
      Serial.println("K");
      long n = total - requested;
      if (n > CHUNK) n = CHUNK;
      requested += n;
      inflight += n;
    }

    reportSwitch();

    if (millis() - lastData > 2000) {
      Serial.println("ERR");
      break;
    }
  }

  audioStop();
  while (Serial.available()) Serial.read();
  Serial.println("DONE");
}

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

  pinMode(SWITCH_PIN, INPUT_PULLUP);
  pinMode(AUDIO_PIN, OUTPUT);
  digitalWrite(AUDIO_PIN, LOW);

  myServo.attach(SERVO_PIN);
  myServo.write(90);

  delay(500);
  Serial.println("Servo ready");
}

void loop() {

  reportSwitch();

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

    else if (command.startsWith("PLAY ")) {
      long total = command.substring(5).toInt();
      if (total > 0) {
        playAudio(total);
      }
    }
  }
}
