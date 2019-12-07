#include <Filters.h>

const int sensorPin = 0;
float sensorValue = 0;

float output;

int queue[50];
int size = 50;
float sum;
int old;

const bool voltmeterMode = false;

void setup(){
  Serial.begin(9600);
  for(int i = 0; i < size; i++){
    queue[i] = 0;
  }
  sum = 0;
  old = 0;
}


void loop() { 
  if(voltmeterMode){
    output = getPin(sensorPin);
  } else {    
    sensorValue = abs(analogRead(sensorPin)-511);
    sum = sum + sensorValue - queue[old];
    queue[old] = sensorValue;
    old++;
    if(old == size) {
      old = 0;
    }
    output = sum / size;
  }

  Serial.println(output);
  delay(15);
}


float modifyOutput(float in) {
  float out = abs(in);
  return(out);  
}

float getPin(int pin) {
  return(analogRead(pin));
}
