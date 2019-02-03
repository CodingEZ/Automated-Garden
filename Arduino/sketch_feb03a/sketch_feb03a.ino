int reverse_delay = 200; // dictates how fast your motor moves
int reverse_ticks = 1000; // dictates the angular distance you move
int forward_delay = 100;
int forward_ticks = 2000;

//ground the other wire of the limit switch, and one to the signal input
void setup() {
  // Pin setup ...
  int pin_curr_dir = X_DIR_PIN;
  int pin_curr_limit = X_MAX_PIN;   // start forward
  int pin_next_limit = X_MIN_PIN;
  int pin_curr_step = X_STEP_PIN;
}

// Currently just moves from one end to the other continuously
void loop();

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

int measure_distance(dir_pin, pin_curr_limit, pin_next_limit, step_pin);


void task4(char motor, int ticks, int delay_time);
