






import ujson
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
    self.key=key
    self.info= self.input_json_data_from_file("blinker_login_conf.py")
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
          try: 
            self.c.subscribe(self.subtopic)
          except:
            print("login failed")
            self.getInfo(self.key,self.devTpye)
            self.__init__(self.key,self.devTpye)
         
  #获取登录信息
  
  def getInfo(self,auth,type_="light"):
      host = 'https://iot.diandeng.tech'
      url = '/api/v1/user/device/diy/auth?authKey=' + auth + "&miType="+type_+"&version=0.1.0"
      data =  get(host + url).text

      fo = open("blinker_login_conf.py", "w")


      fo.write(str(data))


      fo.close()
      return data


      


      

  #心跳回复
  def ping(self):  
    self.publish({"state":"online"}) 
    

  #数据整合成特定json
  def playload(self,msg,toDevice="",deviceType='OwnApp'):
     if toDevice=="":
       toDevice=self.info['detail']['uuid']
     _data= ujson.dumps({
     'fromDevice': self.info['detail']['deviceName'] ,
     'toDevice':   toDevice,
     'data':       msg ,
     'deviceType': deviceType})
     #print ("Mqtt发送>>>>",_data)
     return _data
  #发布消息   
  def publish(self,dict,toDevice="app"):
      if toDevice=="app":
         toDevice=''
         deviceType='OwnApp'
      if toDevice=="mi":
         toDevice='MIOT_r'
         deviceType='vAssistant'
      self.c.publish(self.pubtopic,self.playload(dict,toDevice,deviceType))
        

  def input_json_data_from_file(self,path):
      """
      从文件中获取json数据
      :param path: 文件路径
      :return json_data: 返回转换为json格式后的json数据
      """
      try:
          with open(path, 'r+') as f:
              try:
                  json_data = ujson.load(f)


              except Exception as e:


                  print('json format is error：' + str(e))


          return json_data


      except Exception as e:

          print("file is not exist")
          self.getInfo(self.key,self.devTpye)
          return  self.input_json_data_from_file("blinker_login_conf.py")
          
          
          
          
          
          
          
          
          
          
          
          
          
            

if __name__ == "__main__": 
  from machine import Pin
  import utime
  pin_s={}
  def pin(gpio=2,st=1):
      global pin_s
      if st==1:
          Pin(gpio,Pin.OUT).value(1)
          pin_s[gpio]=1
      elif st==0:
          Pin(gpio,Pin.OUT).value(0)
          pin_s[gpio]=0
      elif st==2:
          try: 
            return pin_s[gpio]
          except:
            pin_s[gpio]=0
            return 1
         
  def cb(topic, msg):

        print("Mqtt接收<<<<",msg)
        #传感器操作
        mq.publish({"pState":"True","temp":"25.8","humi":"66.8", "pm25":"10","co2":"10"},"mi")
        #电灯操作
        msg=eval(str(msg)[2:-1])
        if msg['fromDevice']=='MIOT':
          print (msg)
          try:
            msg['data']['get']
            #判断电灯状态      
            if(pin_s[12]==0):
              print("up_on")
              #mq.publish({"pState":"True"},"mi")
            else:
              print("up_off")
              #mq.publish({"pState":"False"},"mi")
          except:
            pass
          #设定电灯状态   
          try:
            if(msg['data']['set']['pState']=='true'):
              print("on")
              pin(12,1)
              mq.publish({"pState":"true"},"mi")
            else:
              print("off")
              pin(12,0)
              mq.publish({"pState":"False"},"mi")
          except:
            pass        
        mq.ping()

  mq=blinker("fbc6da5da621",cb,'sensor')  
  while 1:
          utime.sleep(1)
          mq.c.check_msg()
