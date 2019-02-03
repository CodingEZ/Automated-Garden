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
void setup();

void loop();

// to run your functions, call it in loop()
// task 1 (basic reading): write a function that reads a signal outputs of Y_MAX_PIN continuously
// task 2 (distance measuring): write a function that switches the motor direction whenever you connect the limit switch (like in the garden), and print out the number of ticks between this click and the previous click
// task 3 (E-stop): copy the function you created in task 2, and use another pin for disabling the motor.
// task 4 (multi-axis control): write a function that switches between driving two motors each time you connect the limit switch. Make sure e-stop is enabled.
// task 5 (synchronized control): write a function that turns two steppers at the same time, and be able to switch direction at the same time. Set delay time to 2000. Make sure e-stop is enabled.
// task 6 (put it all together): write a function that takes in the name of motor, number of ticks, delay time as the inputs. Make sure e-stop is enabled.


void print_signal(int pin);

// forward direction, set dir as HIGH
void move_forward(int dir_pin, int step_pin);

// backward direction, set dir as LOW
void move_backward(int dir_pin, int step_pin);

// make sure pin matches the limit pin when this function is used
// forward direction is toward maximum
// backward direction is toward minimum
int limit_hit(int limit_pin);

void enable(int enable_pin);

void disable(int enable_pin);

void task3();

void task4();

void task5();

void task6(char motor, int ticks, int delay_time);
