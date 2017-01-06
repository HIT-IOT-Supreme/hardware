int sunPin = 9;	//“模拟日光”LED引脚
int warnPin = 7; //“危险警告”LED引脚
int buzzer = 8; //“危险警告”蜂鸣器引脚
int closePin = 5; //“关闭所有”指示LED引脚

float sinVal;
int ledVal;
float toRadian = (3.1412/180);
char val;

void setup() {
  pinMode(sunPin,OUTPUT);  
  pinMode(warnPin,OUTPUT);
  pinMode(closePin,OUTPUT);
  pinMode(buzzer,OUTPUT);

  Serial.begin(9600);
  
}

void loop() {
  val = Serial.read();
 
  if(val == 'H'){
    Serial.println("sun is rasing~");
    for(int x=91; x<180; x++){
      sinVal = (1-sin(x*toRadian));
      ledVal = int(sinVal*255);
      analogWrite(sunPin,ledVal);
      delay(350);
    }
    delay(100);
    digitalWrite(sunPin,LOW);
  }
  else if(val =='W'){
    int i;
    int j;
    for(j = 0;j<5;j++){
      for(i=0;i<80;i++)//输出一个频率的声音
    {
      digitalWrite(buzzer,HIGH);//发声音
      delay(1);//延时1ms
      digitalWrite(buzzer,LOW);//不发声音
      delay(1);//延时ms
    }
      digitalWrite(warnPin,HIGH);
      delay(1000);
      digitalWrite(warnPin,LOW);
      delay(50);
    }
    
    
  }else if(val == 'C'){
    digitalWrite(closePin,HIGH);
    delay(5000);
    digitalWrite(closePin,LOW);
  }
  
}
