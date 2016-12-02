#include "IBT2MotorShield.h"

// Constructors ////////////////////////////////////////////////////////////////
// LEFT:1 RIGHT:2
IBT2MotorShield::IBT2MotorShield()
{
  //Pin map
  _FPWM1 = 7;
  _BPWM1 = 6;
  _FPWM2 = 5;
  _BPWM2 = 4;
}

IBT2MotorShield::IBT2MotorShield(unsigned char FPWM1, unsigned char BPWM1,
                                 unsigned char FPWM2, unsigned char BPWM2)
{
  //Pin map
  _FPWM1 = FPWM1;
  _BPWM1 = BPWM1;
  _FPWM2 = FPWM2;
  _BPWM2 = BPWM2;
}

// Public Methods //////////////////////////////////////////////////////////////
void IBT2MotorShield::init()
{
// Define pinMode for the pins and set the frequency for timer1.

  pinMode(_FPWM1,OUTPUT);
  pinMode(_BPWM1,OUTPUT);
  pinMode(_FPWM2,OUTPUT);
  pinMode(_BPWM2,OUTPUT);

  // #if defined(__AVR_ATmega168__)|| defined(__AVR_ATmega328P__) || defined(__AVR_ATmega32U4__)
  // // Timer 1 configuration
  // // prescaler: clockI/O / 1
  // // outputs enabled
  // // phase-correct PWM
  // // top of 400
  // //
  // // PWM frequency calculation
  // // 16MHz / 1 (prescaler) / 2 (phase-correct) / 400 (top) = 20kHz
  // TCCR1A = 0b10100000;
  // TCCR1B = 0b00010001;
  // ICR1 = 400;
  // #endif
}
// Set speed for motor 1, speed is a number betwenn -400 and 400
void IBT2MotorShield::setM1Speed(int speed)
{
  unsigned char reverse = 0;

  if (speed < 0)
  {
    speed = -speed;  // Make speed a positive quantity
    reverse = 1;  // Preserve the direction
  }
  if (speed > 400)  // Max PWM dutycycle
    speed = 400;

  if (speed == 0)
  {
    analogWrite(_FPWM1,0);   // Make the motor coast no
    analogWrite(_BPWM1,0);   // matter which direction it is spinning.
  }
  else if (reverse)
  {
    analogWrite(_FPWM1,0);
    analogWrite(_BPWM1,(speed*80/51));
  }
  else
  {
    analogWrite(_FPWM1,(speed*80/51));
    analogWrite(_BPWM1,0);
  }
}

// Set speed for motor 2, speed is a number betwenn -400 and 400
void IBT2MotorShield::setM2Speed(int speed)
{
  unsigned char reverse = 0;

  if (speed < 0)
  {
    speed = -speed;  // Make speed a positive quantity
    reverse = 1;  // Preserve the direction
  }
  if (speed > 400)  // Max PWM dutycycle
    speed = 400;

  if (speed == 0)
  {
    analogWrite(_FPWM2,0);   // Make the motor coast no
    analogWrite(_BPWM2,0);   // matter which direction it is spinning.
  }
  else if (reverse)
  {
    analogWrite(_FPWM2,0);
    analogWrite(_BPWM2,(speed*80/51));
  }
  else
  {
    analogWrite(_FPWM2,(speed*80/51));
    analogWrite(_BPWM2,0);
  }
}

// Set speed for motor 1 and 2
void IBT2MotorShield::setSpeeds(int m1Speed, int m2Speed)
{
  setM1Speed(m1Speed);
  setM2Speed(m2Speed);
}
