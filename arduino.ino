int led = 13;
void setup () {
   pinMode(led, OUTPUT); //LED 13 como salida
   Serial.begin(9600); //Inicializo el puerto serial a 9600 baudios
}

void loop () {
   if (Serial.available()) { //Si está disponible
      int c = Serial.read(); //Guardamos la lectura en una variable char
      if (c == '1') { //Si es una 'H', enciendo el LED
         digitalWrite(led, HIGH);
         delay(1000);         
      } else if (c == '0') { //Si es una 'L', apago el LED
        digitalWrite(led, LOW);
        delay(1000);        
      }
   }
}
