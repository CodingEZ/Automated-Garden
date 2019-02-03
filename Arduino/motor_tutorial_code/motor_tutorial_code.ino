#define X_STEP_PIN         54
#define X_DIR_PIN          55
#define X_ENABLE_PIN       38
#define X_MIN_PIN           3
#define X_MAX_PIN           2

#define Y_STEP_PIN         60
#define Y_DIR_PIN          61
#define Y_ENABLE_PIN       56
#define Y_MIN_PIN          14
#define Y_MAX_PIN          15

#define Z_STEP_PIN         46
#define Z_DIR_PIN          48
#define Z_ENABLE_PIN       62
#define Z_MIN_PIN          18
#define Z_MAX_PIN          19

#define E_STEP_PIN         26
#define E_DIR_PIN          28
#define E_ENABLE_PIN       24

#define Q_STEP_PIN         36
#define Q_DIR_PIN          34
#define Q_ENABLE_PIN       30

#define SDPOWER            -1
#define SDSS               53
#define LED_PIN            13

#define FAN_PIN            9

#define PS_ON_PIN          12
#define KILL_PIN           -1

#define HEATER_0_PIN       10
#define HEATER_1_PIN       8
#define TEMP_0_PIN          13   // ANALOG NUMBERING
#define TEMP_1_PIN          14   // ANALOG NUMBERING

int reverse_delay = 200; // dictates how fast your motor moves
int reverse_ticks = 1000; // dictates the angular distance you move
int forward_delay = 100;
int forward_ticks = 2000;

//ground the other wire of the limit switch, and one to the signal input
void setup() {
  //setup only runs once when the Arduino starts up
  Serial.begin(9600);
  pinMode(X_MIN_PIN, INPUT_PULLUP);
  pinMode(X_MAX_PIN, INPUT_PULLUP);
  pinMode(Y_MIN_PIN, INPUT_PULLUP);
  pinMode(Y_MAX_PIN, INPUT_PULLUP);
  pinMode(Z_MIN_PIN, INPUT_PULLUP);
  pinMode(Z_MAX_PIN, INPUT_PULLUP);
  pinMode(FAN_PIN , OUTPUT);
  pinMode(HEATER_0_PIN , OUTPUT);
  pinMode(HEATER_1_PIN , OUTPUT);
  pinMode(LED_PIN  , OUTPUT);
  
  pinMode(X_STEP_PIN  , OUTPUT);
  pinMode(X_DIR_PIN    , OUTPUT);
  pinMode(X_ENABLE_PIN    , OUTPUT);
  
  pinMode(Y_STEP_PIN  , OUTPUT);
  pinMode(Y_DIR_PIN    , OUTPUT);
  pinMode(Y_ENABLE_PIN    , OUTPUT);
  
  pinMode(Z_STEP_PIN  , OUTPUT);
  pinMode(Z_DIR_PIN    , OUTPUT);
  pinMode(Z_ENABLE_PIN    , OUTPUT);
  
  pinMode(E_STEP_PIN  , OUTPUT);
  pinMode(E_DIR_PIN    , OUTPUT);
  pinMode(E_ENABLE_PIN    , OUTPUT);
  
  pinMode(Q_STEP_PIN  , OUTPUT);
  pinMode(Q_DIR_PIN    , OUTPUT);
  pinMode(Q_ENABLE_PIN    , OUTPUT);
  
  digitalWrite(X_ENABLE_PIN    , LOW); //when set to HIGH, motor is disabled
  digitalWrite(Y_ENABLE_PIN    , LOW);
  digitalWrite(Z_ENABLE_PIN    , LOW);
  digitalWrite(E_ENABLE_PIN    , LOW);
  digitalWrite(Q_ENABLE_PIN    , LOW);
}

void loop() {
  //loop() runs again and again
  limit_switch_hit(X_pins, X_limit_switch_result);
  if (!X_limit_switch_result[0]) {
  
  } else if (X_limit_switch_result[1] {
    move_backward(X_DIR_PIN, X_STEP_PIN);
    delay(1000);
  } else {
    move_forward(X_DIR_PIN, X_STEP_PIN);
    delay(1000);
  }
}

// to run your functions, call it in loop()
// task 1 (distance measuring): write a function that switches the motor direction whenever you connect the limit switch (like in the garden),
    // and print out the number of ticks between this click and the previous click
// task 2 (E-stop): copy the function you created in task 2, and use another pin for disabling the motor.
// task 3 (multi-axis control): write a function that switches between driving two motors each time you connect the limit switch. Make sure e-stop is enabled.
// task 4 (synchronized control): write a function that turns two steppers at the same time, and be able to switch direction at the same time
    // Set delay time to 2000. Make sure e-stop is enabled.

//Useful Tips:
// 1. basic forward and reverse motion control:

void print_signal(int pin){
  int signal = digitalRead(pin);
  Serial.println(signal);
}

// forward direction, set dir as HIGH
void move_forward(int dir_pin, int step_pin) {
  digitalWrite(dir_pin, HIGH); // Enables the motor to move in forward direction
  for (int x = 0; x < forward_ticks; x++) {
    digitalWrite(step_pin, HIGH); 
    delayMicroseconds(forward_delay);//this delay dictates how fast it goes
  }
}

// backward direction, set dir as LOW
void move_backward(int dir_pin, int step_pin) {
  digitalWrite(dir_pin, LOW); // Disables forward direction, moves backward
  for (int x = 0; x < reverse_ticks; x++) {
    digitalWrite(step_pin, HIGH); 
    delayMicroseconds(reverse_delay);
  }
}

// make sure pin matches the limit pin when this function is used
// forward direction is toward maximum
// backward direction is toward minimum
int limit_hit(int limit_pin) {
  return digitalRead(limit_pin);
}

void enable(int enable_pin) {
  digitalWrite(enable_pin, LOW);
}

void disable(int enable_pin) {
  digitalWrite(enable_pin, HIGH);
}

void task1() {
}

void task2() {
}

void task3() {
}

void task4(char motor, int ticks, int delay_time) {
  int MIN_PIN;
  int MAX_PIN;
  int STEP_PIN;
  int DIR_PIN;
  int ENABLE_PIN;
  switch (motor) {
    //complete this section by assigning pin numbers
    case 'X':
      break;
    case 'Y':
      break;
    case 'Z':
      break;
    case 'Q':
      break;
    case 'E':
      break;
  }
}
