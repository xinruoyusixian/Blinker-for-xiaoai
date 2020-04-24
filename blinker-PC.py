

import time
import paho.mqtt.client as mqtt
from requests import get 
from json import loads
from json import dumps
class  blinker:
  '''
  # key:密码
  #devTpye 设置设备类型:电灯:light,插座:outlet,多个插座:multi_outlet,传感器:sensor
  #cb 回调函数 例如 def cb(topic, msg):
  '''
  def __init__(self,key,on_message,devTpye="light"):
    self.devTpye=devTpye
    self.info=  self.getInfo(key,self.devTpye) 
    SERVER = "public.iot-as-mqtt.cn-shanghai.aliyuncs.com"
    USER=self.info['detail']['iotId']
    PWD=self.info['detail']['iotToken']
    CLIENT_ID =  self.info['detail']['deviceName']
    self.subtopic="/"+self.info['detail']['productKey']+"/"+self.info['detail']['deviceName']+"/r"
    self.pubtopic='/'+self.info['detail']['productKey']+'/'+self.info['detail']['deviceName']+'/s'

    #pubtopic=bytes(pubtopic, encoding='utf8') 转码为字节
    
    self.c = mqtt.Client(CLIENT_ID, transport='tcp')
    self.c.username_pw_set(USER, PWD)  # 必须设置，否则会返回「Connected with result code 4」
    self.c.connect(SERVER, 1883, 60)  # 此处端口默认为1883，通信端口期keepalive默认60
    self.c.loop_start()
    #self.c.subscribe(self.subtopic, 1) #订阅制定消息
    self.c.on_message= on_message
    print("user:",USER,"CLIENT_ID:",CLIENT_ID,self.subtopic,"/r",self.pubtopic)

         
  #获取登录信息
  def getInfo(self,auth,type_=""):
      host = 'https://iot.diandeng.tech'
      url = '/api/v1/user/device/diy/auth?authKey=' + auth + "&miType="+type_+"&version=1.2.2"
      print (host ,url)
      data =  loads(get(host + url).text)
      return data

  #心跳回复
  def ping(self): 
    self.c.publish(self.pubtopic,self.playload({"state":"online"}))
  def send(self,s): 
    self.c.publish(self.pubtopic,self.playload(s))
  #处理要发送的信息
  def playload(self,msg,toDevice="",deviceType='OwnApp'):
     if toDevice=="":
       toDevice=self.info['detail']['uuid']
     _data= dumps({
     'fromDevice': self.info['detail']['deviceName'] ,
     'toDevice':   toDevice,
     'data':       msg ,
     'deviceType': deviceType})
     print ("[",time.time(),"]Mqtt发送>>>>",_data)
     return _data


if __name__ == "__main__": 
  
  
  def on_message(msc, obj, msg):
        print("[",time.time(),"]Mqtt接收<<<<",msg.topic,":",msg.payload)
        mq.send("12")
        mq.c.publish(mq.pubtopic,mq.playload({"pState":"True","temp":"99","humi":"23", "pm25":"10","co2":"10"},"MIOT_r","vAssistant"))
        mq.ping()
        
  #你的binker key,on_message:回调函数名称,最后一个是设备类型可填可不填
  mq=blinker("6090bf3",on_message,'')
  while 1:
          time.sleep(1)
          #mq.ping()

