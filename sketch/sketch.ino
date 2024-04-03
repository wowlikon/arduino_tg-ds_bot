bool bits[8]; // Bits of input

void setup() {
  Serial.begin(9600); // Open port
  while (!Serial); // !!!ONLY FOR ARDUINO LEONARDO!!!

  Serial.println("Hello world");
  pinMode(A0, OUTPUT); // Geen
  pinMode(A1, OUTPUT); // Red
  pinMode(A2, OUTPUT); // Blue
}

void loop() {
  byte data;
  if (Serial.available() > 0) { // Wait
    data = Serial.read(); //   Get data

    // Byte2Bits
    for (int i = 0; i < 8; i++) {
      bits[i] = bitRead(data, i);
    }

    // Set LEDs
    digitalWrite(A2, bits[0]); // Red
    digitalWrite(A0, bits[1]); // Geen
    digitalWrite(A1, bits[2]); // Blue

    // Return bits (DEBUG)
    for (int i = 7; i >= 0; i--) {
      Serial.print(bits[i]);
    } Serial.println();
  }
}