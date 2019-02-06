char command[8];
char response[8];

void setup() {
  Serial.begin(9600);
  arduino_flush();    // removes previous values in serial buffer
  delay(1000);        // allows time for command to be sent
}

void loop() {
  if (Serial.available() > 0) {
    read_command();
    process_command();
    write_response();
  }
}

void arduino_flush() {
  while (Serial.available() > 0) {
    Serial.read();
  }
}

void read_command() {
  command[0] = Serial.read();
  for (int i = 0; i < command[0] - '0'; i++) {
    command[i+1] = Serial.read();
  }
}

void process_command() {
  switch (command[1]) {
    case '0':
      arduino_move();
      break;
    case '1':
      arduino_water();
      break;
    default:
      break;
  }
  
  Serial.flush();    // wait for serial writes to finish before continuing
}

void write_response() {
  Serial.write(response[0]);
  for (int i = 0; i < response[0] - '0'; i++) {
    Serial.write(response[i+1]);
  }
}

void arduino_move() {
  delay(1000);
  // will add in later
  
  char result[] = {'4', 'm', 'o', 'v', 'e'};
  for (int i = 0; i < sizeof(result); i++) {
    response[i] = result[i];
  }
}

void arduino_water() {
  delay(1000);
  // will add in later
  
  char result[] = {'5', 'w', 'a', 't', 'e', 'r'};
  for (int i = 0; i < sizeof(result); i++) {
    response[i] = result[i];
  }
}

