





import ujson
from simple import MQTTClient
from urequests import get 

class  blinker:
  '''
  # key:密码
  #devTpye 设置设备类型:电灯:light,插座:outlet,多个插座:multi_outlet,传感器:sensor
  #cb 回调函数 例如 def cb(topic, msg):
  '''
  def __init__(self,key,cb,devTpye="light"):
    self.devTpye=devTpye
    self.state=0
    self.cb=cb
    self.key=key
    #self.info=  self.getInfo(key,self.devTpye) 
    self.info= self.input_json_data_from_file("blinker_login_conf.py")
    self.SERVER = "public.iot-as-mqtt.cn-shanghai.aliyuncs.com"
    self.USER=self.info['detail']['iotId']
    self.PWD=self.info['detail']['iotToken']
    self.CLIENT_ID =  self.info['detail']['deviceName']
    self.connect()
         
  #获取登录信息
  def getInfo(self,auth,type_="light"):
      host = 'https://iot.diandeng.tech'
      url = '/api/v1/user/device/diy/auth?authKey=' + auth + "&miType="+type_+"&version=0.1.0"
      data =  get(host + url).text
      fo = open("blinker_login_conf.py", "w")
      fo.write(str(data))
      fo.close()
      return data


  #MQQT 连接    
  def connect(self):
    self.c=MQTTClient(client_id=self.CLIENT_ID,server=self.SERVER,user=self.USER,password=self.PWD,keepalive=30)
    self.c.DEBUG = True
    self.c.set_callback(self.cb)
    self.subtopic="/"+self.info['detail']['productKey']+"/"+self.info['detail']['deviceName']+"/r"
    self.pubtopic=b"/"+self.info['detail']['productKey']+"/"+self.info['detail']['deviceName']+"/s"
    print("user:",self.USER,"CLIENT_ID:",self.CLIENT_ID,self.subtopic,"/r",self.pubtopic)
    try:
      print("connect: try",self.state,"times")
      if not self.c.connect(clean_session=False):
            try: 
              self.c.subscribe(self.subtopic)
            except:
              print("connect:Failed")
              self.state+=1
              self.getInfo(self.key,self.devTpye)
              self.__init__(self.key,self.devTpye)
            print("New session being set .")
            self.state=0
    except:
      print("check NETWORK and login infomtaion")
  #mqtt 信息轮询
  def check_msg(self):
      try:
        self.c.check_msg()
      except OSError as e:
        print ("check:",e)
        self.reconnect()
  #mqtt 重连      
  def reconnect(self):
    try:
      self.c.connect(False)
      print("reconnected!")
    except OSError as e:
        self.state+=1
        print ("reconnect:",e)
        self.connect()
  #mqtt 心跳回复
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
     
  #mqtt 发布消息
  def publish(self,dict,toDevice="app"):
      if toDevice=="app":
         toDevice=''
         deviceType='OwnApp'
      if toDevice=="mi":
         toDevice='MIOT_r'
         deviceType='vAssistant'
      try:   
        self.c.publish(self.pubtopic,self.playload(dict,toDevice,deviceType))
      except OSError as e:
        print ("publish:",e)
        self.reconnect()
        
        
  
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
   import   time ,lib,blinker


  def cb(topic, msg):
          print("Mqtt REC<<<<",msg)
          #传感器操作
          msg=eval(str(msg)[2:-1])
          print("Mqtt接收<<<<",msg)
          #电灯操作
          try:
            if msg['data']['btn-sw']=='tap':
               if lib.pin_s[12]==0:
                 lib.pin(12,1)
                 mq.publish({"btn-sw":{"col":"#000000", }})    
               else:
                lib.pin(12,0)
                mq.publish({"btn-sw":{"col":"#FFFFFF", }})
          except:
            pass        
          if msg['fromDevice']=='MIOT':

            try:
              if(msg['data']['set']['pState']=='true'):
                print("on")
                lib.pin(12,1)

              else:
                print("off")
                lib.pin(12,0)

            except:
              pass 

          mq.ping()
          print("exec")

  a="0"
  mq=blinker.blinker("b14b891ec11b",cb,'light')




  t=1
  lib.pin(2,1)
  lib.pin(12,0)
  mq.ping()
  while 1:
      if t%120==0:
        mq.ping()
      time.sleep(1)
      t+=1
      mq.check_msg()
      print(t)
