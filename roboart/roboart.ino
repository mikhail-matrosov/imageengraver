#include <math.h>
#include <Servo.h> 


#define N 24// 4 params, with a space in between
#define Nparams 5
const int Nservos = 4;

char buf[N+1];
byte messageLengthReceived=0;

//servos
Servo ser[Nservos];
int serPin[Nservos]={6,9,10,11};

//params
String paramString[Nparams];
long paramValue[Nparams];
int indexStart[Nparams]={0,5,10,15,20};
int indexEnd[Nparams]={4,9,14,19,24};

void setup()
{
  Serial.begin(9600);
  for (int s=0;s<Nservos;s++)
  {
    ser[s].attach(serPin[s]);
    ser[s].writeMicroseconds( 1500 );
    paramValue[s] = 1500;
  }
}

void loop() 
{
  // send data only when you receive data:
  if (Serial.available() > 0) 
  {
    messageLengthReceived = Serial.readBytesUntil('|',buf,N+1);
    if (messageLengthReceived==N) //if data packet is of proper size
    {
      //Serial.println(messageLengthReceived);
      //Serial.println(buf);
      for (int p=0;p<Nparams;p++)
      {
        paramString[p]="";
        
        //Assembling a string corresponding to p-th parameter
        for (int i=0;i<indexEnd[p]-indexStart[p];i++)
        {
          paramString[p]+=buf[indexStart[p]+i];
        }
        
        paramValue[p]=str2int (paramString[p]); //THE MOST IMPORTANT PART
        //Serial.print("restored paremeter #");
        //Serial.print(p);
        //Serial.print(":");
        //Serial.println(paramValue[p] );
      }              
    }
    else
    {
      Serial.print("buf=");
      Serial.println(buf) ;//if data packet is of unproper size
      Serial.println("data is corrupted") ;//if data packet is of unproper size
    }
  }
  //let's make buf=""             
  int i=0;
  for (i=0;i<N;i++) 
  {
    buf[i]=0;
  }
  
  // test checksum
  long checksum = (paramValue[0] ^ paramValue[1] ^ paramValue[2] ^ paramValue[3]) % 10000;
  if (checksum != paramValue[4])
  {
    Serial.print("Wrong checksum - ignoring the command");
  }
  else
  {
    //let's write our shit into servos
    for (int s=0;s<Nservos;s++)
    {
      ser[s].writeMicroseconds( paramValue[s] );
      //delay(50);
    }
  }
}

int chr2int(char c)
{
  const int zerochar = (byte)'0';
  return (byte)c-zerochar;
}

long  str2int(String s)
{const int l=s.length();
  double  a[l];
  double  sum=0;
  for (int i=0;i<l;i++)
  {
    a[i]=chr2int( s.charAt(i) ); //?
   //for internal debugging
   // Serial.print( "a[" ); Serial.print( i );Serial.print( "]=" );Serial.println( a[i]);
    //Serial.println( pow(10,l-i-1 ));
    //Serial.println( a[i] * pow(10.0d,l-i-1) );
    sum+=a[i]*pow(10,(l-i-1));
  }
 
  return round(sum);
}
