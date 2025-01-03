
// adapted from:
// Nikon Remote Emulator by Gough Lui (http://goughlui.com)

int unsigned long startmillis = 0;
const int monitPin = 13;
const int sigPin = 12;


void setup() {
  pinMode(sigPin,OUTPUT);
  pinMode(monitPin,OUTPUT);
  digitalWrite(sigPin,LOW);
  digitalWrite(monitPin,LOW);
  Serial.begin(115200);
}

void loop() {
  // Read serial input:
  while (Serial.available() > 0) {
    int inChar = Serial.read();
    // when newline is recieved, print start message, then run the remote transmit routine.
    if (inChar == '\n') {
      digitalWrite(monitPin, !digitalRead(monitPin));
      startmillis = millis();
      Serial.print("start: ");
      Serial.println(millis()-startmillis);
      // call subroutine
      ML3(); //transmit the remote signal
      
      // print elapsed time about every 10 ms
      for (int i=0; i <= 30; i++){
        Serial.println(millis()-startmillis);
        delay(10);
      }            
    }
  }
}

void ML3(){
  // Delays are tuned to account for overhead of library code.
    tone(sigPin,38000);
    delay(2);
    noTone(sigPin);
    delay(28);//original delay 28ms
    tone(sigPin,38000);
    delayMicroseconds(200);
    noTone(sigPin);
    delayMicroseconds(1500);
    tone(sigPin,38000);
    delayMicroseconds(200);
    noTone(sigPin);
    delayMicroseconds(3300);
    tone(sigPin,38000);
    delayMicroseconds(200);
    noTone(sigPin);
}
