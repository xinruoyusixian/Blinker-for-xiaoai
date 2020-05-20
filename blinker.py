

import ujson,utime
from robust import MQTTClient
from urequests import get 


class  blinker:
  '''
  # key:密码
  #devTpye 设置设备类型:电灯:light,插座:outlet,多个插座:multi_outlet,传感器:sensor
  #cb 回调函数 例如 def cb(topic, msg):
  '''
  def __init__(self,key,cb,devTpye="light"):
    self.devTpye=devTpye
    self.info=  self.getInfo(key,self.devTpye) 
    SERVER = "public.iot-as-mqtt.cn-shanghai.aliyuncs.com"
    USER=self.info['detail']['iotId']
    PWD=self.info['detail']['iotToken']
    CLIENT_ID =  self.info['detail']['deviceName']
    self.c=MQTTClient(client_id=CLIENT_ID,server=SERVER,user=USER,password=PWD,keepalive=300)
    self.c.DEBUG = True
    self.c.set_callback(cb)
    self.subtopic="/"+self.info['detail']['productKey']+"/"+self.info['detail']['deviceName']+"/r"
    self.pubtopic=b"/"+self.info['detail']['productKey']+"/"+self.info['detail']['deviceName']+"/s"
    print("user:",USER,"CLIENT_ID:",CLIENT_ID,self.subtopic,"/r",self.pubtopic)
    if not self.c.connect(clean_session=False):
          print("New session being set .")
          self.c.subscribe(self.subtopic)
         
  #获取登录信息
  def getInfo(self,auth,type_="light"):
      host = 'https://iot.diandeng.tech'
      url = '/api/v1/user/device/diy/auth?authKey=' + auth + "&miType="+type_+"&version=1.2.2"
      print (host ,url)
      data =  ujson.loads(get(host + url).text)
      return data

  #心跳回复
  def ping(self):  
    self.c.publish(self.pubtopic,self.playload({"state":"online"})) 

  #处理要发送的信息
  def playload(self,msg,toDevice="",deviceType='OwnApp'):
     if toDevice=="":
       toDevice=self.info['detail']['uuid']
     _data= ujson.dumps({
     'fromDevice': self.info['detail']['deviceName'] ,
     'toDevice':   toDevice,
     'data':       msg ,
     'deviceType': deviceType})
     print ("[",utime.time(),"]Mqtt发送>>>>",_data)
     return _data




if __name__ == "__main__": 
  import  lib
  def cb(topic, msg):
        print("[",utime.time(),"]Mqtt接收<<<<",msg)
        #传感器操作
        mq.c.publish(mq.pubtopic,mq.playload({"pState":"True","temp":"25.8","humi":"66.8", "pm25":"10","co2":"10"},"MIOT_r","vAssistant"))
        #电灯操作
        msg=eval(str(msg)[2:-1])
        if msg['fromDevice']=='MIOT':
          print (msg)
          try:
            msg['data']['get']
            #判断电灯状态      
            if(lib.pin_s[12]==0):
              print("up_on")
              #mq.c.publish(mq.pubtopic,mq.playload({"pState":"True"},"MIOT_r","vAssistant"))
            else:
              print("up_off")
              #mq.c.publish(mq.pubtopic,mq.playload({"pState":"False"},"MIOT_r","vAssistant"))
          except:
            pass
          #设定电灯状态   
          try:
            if(msg['data']['set']['pState']=='true'):
              print("on")
              lib.pin(12,1)
              mq.c.publish(mq.pubtopic,mq.playload({"pState":"True"},"MIOT_r","vAssistant"))
            else:
              print("off")
              lib.pin(12,0)
              mq.c.publish(mq.pubtopic,mq.playload({"pState":"False"},"MIOT_r","vAssistant"))
          except:
            pass        
        mq.ping()

  mq=blinker("e914cadf0ffd",cb,'sensor')  
  while 1:
          utime.sleep(1)
          mq.c.check_msg()
