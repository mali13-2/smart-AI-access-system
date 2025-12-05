#include <SPI.h>
#include <MFRC522.h>
#include <Stepper.h>

// PIN CONFIG 
const uint8_t RED_LED   = 6;
const uint8_t GREEN_LED = 7;

// RC522 on Arduino MEGA
const uint8_t SS_PIN  = 49;   // SDA
const uint8_t RST_PIN = 53;   // RST

MFRC522 mfrc522(SS_PIN, RST_PIN);

// Stepper 28BYJ-48 + ULN2003
const int stepsPerRevolution = 2048;
// Wiring: IN1→8, IN2→9, IN3→10, IN4→11
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);

// CARD UID TO ACCEPT
byte ALLOWED_UID[4] = {0x84, 0x5E, 0x39, 0xD9};  // <<< this matches 84 5E 39 D9

// HELPERS
void sendline(const String &msg) {
  Serial.println(msg);
}

void printUID(const MFRC522::Uid &uid) {
  Serial.print("CARD_UID:");
  for (byte i = 0; i < uid.size; i++) {
    Serial.print(" ");
    if (uid.uidByte[i] < 0x10) Serial.print("0");
    Serial.print(uid.uidByte[i], HEX);
  }
  Serial.println();
}

bool uidMatches(const MFRC522::Uid &uid) {
  if (uid.size != 4) return false;
  for (byte i = 0; i < 4; i++) {
    if (uid.uidByte[i] != ALLOWED_UID[i]) return false;
  }
  return true;
}

// SEQUENCES
void unlockSequence() {
  sendline("[ARDUINO] APPROVED from PC – unlocking");

  // blink green 3×
  for (int i = 0; i < 3; i++) {
    digitalWrite(GREEN_LED, HIGH);
    digitalWrite(RED_LED, LOW);
    delay(200);
    digitalWrite(GREEN_LED, LOW);
    delay(200);
  }

  // move stepper one revolution forward then back
  myStepper.setSpeed(12); // RPM
  myStepper.step(stepsPerRevolution);
  delay(500);
  myStepper.step(-stepsPerRevolution);
}

void deniedSequence() {
  sendline("[ARDUINO] DENIED from PC – stay locked");

  // blink red 3×
  for (int i = 0; i < 3; i++) {
    digitalWrite(RED_LED, HIGH);
    digitalWrite(GREEN_LED, LOW);
    delay(200);
    digitalWrite(RED_LED, LOW);
    delay(200);
  }
}

// SETUP
void setup() {
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  digitalWrite(RED_LED, LOW);
  digitalWrite(GREEN_LED, LOW);

  Serial.begin(9600);
  while (!Serial) { ; }

  sendline("=== RFID + FACE + STEPPER ACCESS SYSTEM ===");
  sendline("[ARDUINO] Initialising RC522 on SDA=49, RST=53 ...");

  SPI.begin();
  mfrc522.PCD_Init();

  myStepper.setSpeed(12);

  sendline("[ARDUINO] System ready. Waiting for card + PC decision.");
}

//LOOP
void loop() {

  // 1) Listen for decision from Python
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    cmd.toUpperCase();

    if (cmd.length() > 0) {
      if (cmd == "APPROVED") {
        unlockSequence();
      } else if (cmd == "DENIED") {
        deniedSequence();
      } else {
        sendline("[ARDUINO] Unknown serial cmd: " + cmd);
      }
    }
  }

  // 2) Poll RFID – send UID to PC when card is tapped
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return;
  }
  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  // We have a card
  printUID(mfrc522.uid);

  // Also tell Python whether this UID is even allowed
  if (uidMatches(mfrc522.uid)) {
    sendline("CARD_OK");
  } else {
    sendline("CARD_UNKNOWN");
  }

  // Halt current card
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();

  delay(300); // small gap before next read
}
