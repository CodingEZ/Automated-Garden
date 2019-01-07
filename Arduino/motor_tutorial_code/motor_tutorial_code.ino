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

  int X_pins[2];
  int X_limit_switch_result[2];

  X_pins[0] = X_MIN_PIN;  //target pin
  X_pins[1] = X_MAX_PIN;  //opposite pin
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
// task 1 (basic reading): write a function that reads a signal outputs of Y_MAX_PIN continuously
// task 2 (distance measuring): write a function that switches the motor direction whenever you connect the limit switch (like in the garden), and print out the number of ticks between this click and the previous click
// task 3 (E-stop): copy the function you created in task 2, and use another pin for disabling the motor.
// task 4 (multi-axis control): write a function that switches between driving two motors each time you connect the limit switch. Make sure e-stop is enabled.
// task 5 (synchronized control): write a function that turns two steppers at the same time, and be able to switch direction at the same time. Set delay time to 2000. Make sure e-stop is enabled.
// task 6 (put it all together): write a function that takes in the name of motor, number of ticks, delay time as the inputs. Make sure e-stop is enabled.

//Useful Tips:
// 1. basic forward and reverse motion control:

void print_signal(int pin) {
  //2. basic printing pin value example
  int signal = digitalRead(pin);
  Serial.println(signal);
}

void move_forward(int dir_pin, int step_pin) {
  digitalWrite(dir_pin, HIGH); // Enables the motor to move in a particular direction
  // Makes 200 pulses for making one full cycle rotation
  //example of how to move the motor shaft forward then backwards
  for (int x = 0; x < forward_ticks; x++) {
    digitalWrite(step_pin, HIGH); 
    delayMicroseconds(forward_delay);//this delay dictates how fast it goes
    digitalWrite(step_pin, LOW); 
    delayMicroseconds(forward_delay);
  }
  //print_signal(min_pin);
  //print_signal(max_pin);
}

void move_backward(int dir_pin, int step_pin) {
  digitalWrite(dir_pin, LOW); //turn off the direction pin voltage to switch to reverse direction
  for (int x = 0; x < reverse_ticks; x++) {
    digitalWrite(step_pin, HIGH); 
    delayMicroseconds(reverse_delay); 
    digitalWrite(step_pin, LOW); 
    delayMicroseconds(reverse_delay);
  }
  //print_signal(min_pin);
  //print_signal(max_pin);
}

void limit_switch_hit(int pins[], int limit_result[]) {
  if (digitalRead(pins[0])) {
    if (digitalRead(pins[1])) {
      limit_result[0] = false;
      limit_result[1] = false;
    } else {
      limit_result[0] = true;
      limit_result[1] = true;
    }
    int hold = pins[0];
    pins[0] = pins[1];
    pins[1] = hold;
  }
  limit_result[0] = true;
  limit_result[1] = false;
}

void task3() {
}

void task4() {
}

void task5() {
}

void task6(char motor, int ticks, int delay_time) {
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
