#include <Servo.h>

int ldrPin = A0;          
int pinled = 6;            
int echo = 13;             
int triger = 12;           

Servo servoMotor;

bool controlLuz = false;   // Control del LED
bool controlPuerta = false; // Control del servo

void setup() {
  Serial.begin(9600); 
  pinMode(echo, INPUT);
  pinMode(triger, OUTPUT);
  pinMode(pinled, OUTPUT);
  digitalWrite(pinled, LOW);
  servoMotor.attach(9);
  servoMotor.write(90); 
}

void loop() {
 
  if (Serial.available()) {
    String comando = Serial.readStringUntil('\n');
    if (comando == "ACTIVAR_LUZ") {
      controlLuz = true;
    } else if (comando == "DESACTIVAR_LUZ") {
      controlLuz = false;
      digitalWrite(pinled, LOW);
    } else if (comando == "ACTIVAR_PUERTA") {
      controlPuerta = true;
    } else if (comando == "DESACTIVAR_PUERTA") {
      controlPuerta = false;
      servoMotor.write(90); // Cierra la puerta
    }
  }


  int intensidadLuminosidad = analogRead(ldrPin);

  if (controlLuz && intensidadLuminosidad > 400) {
    digitalWrite(pinled, HIGH);
  } else {
    digitalWrite(pinled, LOW);
  }


  if (controlPuerta) {
    int tiempoEcho;
    int distancia;

 
    digitalWrite(triger, HIGH);
    delayMicroseconds(10);
    digitalWrite(triger, LOW);
    tiempoEcho = pulseIn(echo, HIGH);
    distancia = tiempoEcho / 59;

    Serial.print("Distancia: ");
    Serial.print(distancia);
    Serial.print(" - Intensidad de luz: ");
    Serial.println(intensidadLuminosidad);

 
    if (distancia < 10) {
      servoMotor.write(180); 
      delay(3000);           
      servoMotor.write(90);  
    }
  }
}



