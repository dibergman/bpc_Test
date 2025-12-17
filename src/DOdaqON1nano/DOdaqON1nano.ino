/*This program controls Arduino Nano digital output bits in response to serial messages

nano_chan_controller reversed ON1 (2,3,4,5) and RST (10,11,12,13) lines for CH2 and CH4

*/


void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);

pinMode(2, OUTPUT);
pinMode(3, OUTPUT);
pinMode(4, OUTPUT);
pinMode(5, OUTPUT);
pinMode(6, OUTPUT);
pinMode(7, OUTPUT);
pinMode(8, OUTPUT);
pinMode(9, OUTPUT);
pinMode(10, OUTPUT);
pinMode(11, OUTPUT);
pinMode(12, OUTPUT);
pinMode(13, OUTPUT);


digitalWrite(2, LOW);
digitalWrite(3, LOW);
digitalWrite(4, LOW);
digitalWrite(5, LOW);
digitalWrite(6, LOW);
digitalWrite(7, LOW);
digitalWrite(8, LOW);
digitalWrite(9, LOW);
digitalWrite(10, LOW);
digitalWrite(11, LOW);
digitalWrite(12, LOW);
digitalWrite(13, LOW);

}

char str[2];
int num;
int i;
unsigned long tk;
unsigned long tk_10ms = 0;
int CH1_ON1 = 0;
int CH2_ON1 = 0;
int CH3_ON1 = 0;
int CH4_ON1 = 0;
int ON1_pulse_train = LOW;
int cmd_format=1;


void loop() {
  // put your main code here, to run repeatedly:
tk = millis();

if(tk - tk_10ms > 5) { // run code and toggle ON1 every 10 ms

if (Serial.available() > 0) {
  num = Serial.readBytes(str, 2); // read 2 bytes
  i = atoi(str);
  
switch(i){
  case 1: 
  //digitalWrite(2, HIGH);
  CH1_ON1 = 1;
  Serial.print("Ch1 On\n") ;
  break;

  case 2: 
  //digitalWrite(3, HIGH);
  CH2_ON1 = 1;
  Serial.print("Ch2 On\n") ;
  break;

  case 3: 
  //digitalWrite(4, HIGH);
  CH3_ON1 = 1;
  Serial.print("Ch3 On\n") ;
  break;

  case 4:
  //digitalWrite(5, HIGH);
  CH4_ON1 = 1;
  Serial.print("Ch4 On\n") ;
  break;

  case 5: 
  //digitalWrite(2, LOW);
  CH1_ON1 = 0;
  Serial.print("Ch1 Off\n") ;
  break;

  case 6: 
  //digitalWrite(3, LOW);
  CH2_ON1 = 0;
  Serial.print("Ch2 Off\n") ;
  break;

  case 7: 
  //digitalWrite(4, LOW);
  CH3_ON1 = 0;
  Serial.print("Ch3 Off\n") ;
  break;

  case 8: 
  //digitalWrite(5, LOW);
  CH4_ON1 = 0;
  Serial.print("Ch4 Off\n") ;
  break;

  case 9: 
  digitalWrite(6, HIGH);
  Serial.print("Ch1 PSC Direct Enable\n") ;
  break;

  case 10: 
  digitalWrite(7, HIGH);
  Serial.print("Ch2 PSC Direct Enable\n") ;
  break;

  case 11: 
  digitalWrite(8, HIGH);
  Serial.print("Ch3 PSC Direct Enable\n") ;
  break;

  case 12: 
  digitalWrite(9, HIGH);
  Serial.print("Ch4 PSC Direct Enable\n") ;
  break;

  case 13: 
  digitalWrite(6, LOW);
  Serial.print("Ch1 PSC Direct Inhibit\n") ;
  break;

  case 14: 
  digitalWrite(7, LOW);
  Serial.print("Ch2 PSC Direct Inhibit\n") ;
  break;

  case 15: 
  digitalWrite(8, LOW);
  Serial.print("Ch3 PSC Direct Inhibit\n") ;
  break;

  case 16: 
  digitalWrite(9, LOW);
  Serial.print("Ch4 PSC Direct Inhibit\n") ;
  break;

  case 17: 
  digitalWrite(10, HIGH);
  delay(25);
  digitalWrite(10, LOW);
  Serial.print("Ch1 Reset\n") ;
  break;

  case 18: 
  digitalWrite(3, HIGH);
  delay(25);
  digitalWrite(3, LOW);
  Serial.print("Ch2 Reset\n") ;
  break;

  case 19: 
  digitalWrite(12, HIGH);
  delay(25);
  digitalWrite(12, LOW);
  Serial.print("Ch3 Reset\n") ;
  break;

  case 20: 
  digitalWrite(5, HIGH);
  delay(25);
  digitalWrite(5, LOW);
  Serial.print("Ch4 Reset\n") ;
  break;

  case 21:
  cmd_format=0;
  break;

  case 22:
  cmd_format=1;
  break;
  }
i=22;
}

ON1_pulse_train = !ON1_pulse_train;

if (CH1_ON1 && cmd_format) digitalWrite(2, ON1_pulse_train);
if (CH1_ON1 && !cmd_format) digitalWrite(2, HIGH);

if (CH2_ON1 && cmd_format) digitalWrite(11, ON1_pulse_train);
if (CH2_ON1 && !cmd_format) digitalWrite(11, HIGH);

if (CH3_ON1 && cmd_format) digitalWrite(4, ON1_pulse_train);
if (CH3_ON1 && !cmd_format) digitalWrite(4, HIGH);

if (CH4_ON1 && cmd_format) digitalWrite(13, ON1_pulse_train);
if (CH4_ON1 && !cmd_format) digitalWrite(13, HIGH);

if (!CH1_ON1) digitalWrite(2, LOW);
if (!CH2_ON1) digitalWrite(11, LOW);
if (!CH3_ON1) digitalWrite(4, LOW);
if (!CH4_ON1) digitalWrite(13, LOW);

tk_10ms = tk;
}

}
