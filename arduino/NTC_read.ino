// تنظیمات NTC
int ssrPin = 9;
const float R_FIXED = 9330.0; // مقاومت سری (Ω)
const float R0 = 100000;      // مقاومت NTC در 25°C (Ω)
const float T0 = 25.0 + 273.15; // دمای مرجع (کلوین)
const float BETA = 3950.0;      // مقدار Beta

const int NTC_PIN = A0; // پین آنالوگ

unsigned long lastTime = 0;
const unsigned long Ts = 400;

void setup() {
  pinMode(ssrPin, OUTPUT);
  Serial.begin(9600);
  while(!Serial.available()){
    ; // don nothing untill python code runs.
  }
  Serial.read();
}

void loop() {
  unsigned long now = millis();
  int adc = analogRead(NTC_PIN);
  

  float R_ntc = R_FIXED * ((1023.0 / adc) - 1.0);
  

  float T = 1.0 / ( (1.0 / BETA) * log(R_ntc / R0 ) + (1.0 / T0) );
  

  float Tc = T - 273.15;

  if (Tc < 92){
    digitalWrite(ssrPin, HIGH);
  }else{
    digitalWrite(ssrPin, LOW);
  }
  
  if (now - lastTime >= Ts){
    lastTime = millis();
    Serial.print(now);
    Serial.print(",");
    Serial.println(Tc);
  }
}
