int ssrPin = 9;      // SSR pin
int sensorPin = A0;  // NTC 100k pin

// PID parameteres
double Kp = 50;
double Ki = 0.03;
double Kd = 0.0;

double Wc = 2.2; //wc for derivative filter

// NTC 100k 
double R0 = 100000;     
double T0 = 298.15;   
double B = 3950;        
double Rseries = 9330; 

double setPoint = 85; 
double prevTemp = 0.0;
double u = 0.0;
double integral = 0.0;
double Ud = 0.0;
double lastError = 0.0;
double preheatTemp = 55.0;

const int windowSize = 2500; 
const unsigned long controlPeriod = 100;
unsigned long lastControlTime = 0;
unsigned long windowStartTime = 0;

const unsigned long logPeriod = 500;
unsigned long lastLogTime = 0;

double power = 1500;
double power_ratio = 0;

double t_on = 0;
double t_off = 0;


void setup() {
  pinMode(ssrPin, OUTPUT);
  Serial.begin(9600);

  while(!Serial.available()){
    ; // do nothing untill python code runs.
  }
  Serial.read();
  windowStartTime = millis();
}

double readNTC(int pin){
  int adc = analogRead(pin);
  double Rntc = Rseries * ((1023.0 / adc) - 1.0);

  double T = 1.0 / (1.0/T0 + (1.0/B) * log(Rntc/R0));
  T = T - 273.15; // kelvin to celsius
  return T;
}

void loop() {
  double currentTemp = readNTC(sensorPin);
  unsigned long now = millis();
  static bool pidStarted = false;
  // control p(t) every controlPeriod = 0.5s
  if (now - lastControlTime >= controlPeriod){

        double dt = (now - lastControlTime) / 1000.0;
        if (dt > 0){
          Ud = 1/(Wc * controlPeriod) * (Ud + Kd * Wc * (currentTemp - prevTemp));
          prevTemp = currentTemp;
        }
        lastControlTime = now;

        if (currentTemp < preheatTemp){
          power_ratio = 1;
          integral = 0;
          pidStarted = false;
        }
        else{

          if (!pidStarted){
            integral = 0;
            lastControlTime = now;
            pidStarted = true;
            
          }
          else{
              double error = setPoint - currentTemp;

              u =  Kp * error +  Ki * integral - Ud;
              power_ratio = u / power;

              if (power_ratio < 0.10){
                if (power_ratio >= 0.05) power_ratio = 0.10;
                if (power_ratio < 0.05) power_ratio = 0.0;
              }

              if (power_ratio > 0.90){
                if (power_ratio >= 0.95) power_ratio = 1;
                if (power_ratio < 0.95) power_ratio = 0.90;
              }


              
              
              if (currentTemp > 93.0) power_ratio = 0.0;
              
              integral += error * dt;
                
          }

          
        }

  }
  
  if ((now - windowStartTime) >= windowSize){
    windowStartTime += windowSize;
    t_on = power_ratio * windowSize;
  }

  if ((now - windowStartTime) < t_on){
    digitalWrite(ssrPin, HIGH); 
  } else {
    digitalWrite(ssrPin, LOW); 
  }

  if (now - lastLogTime >= logPeriod) {
    lastLogTime = now;
    Serial.print(now);
    Serial.print(",");
    Serial.print(t_on / windowSize);
    Serial.print(",");
    Serial.println(currentTemp);

  }

}
