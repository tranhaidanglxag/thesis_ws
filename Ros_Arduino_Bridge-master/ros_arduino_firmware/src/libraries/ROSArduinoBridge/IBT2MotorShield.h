#ifndef IBT2MotorShield_h
#define IBT2MotorShield_h

#include <Arduino.h>

class IBT2MotorShield
{
  public:  
    // CONSTRUCTORS
    IBT2MotorShield(); // Default pin selection.
    IBT2MotorShield(unsigned char FPWM1, unsigned char BPWM1,
                    unsigned char FPWM2, unsigned char BPWM2); // User-defined pin selection. 
    
    // PUBLIC METHODS
    void init(); // Initialize TIMER 1, set the PWM to 20kHZ. 
    void setM1Speed(int speed); // Set speed for M1.
    void setM2Speed(int speed); // Set speed for M2.
    void setSpeeds(int m1Speed, int m2Speed); // Set speed for both M1 and M2.

//Pin map   
  private:
    unsigned char _FPWM1;
    unsigned char _BPWM1;
    unsigned char _FPWM2;
    unsigned char _BPWM2;
    
};

#endif
