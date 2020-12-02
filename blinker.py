





import ujson,time
from simple import MQTTClient
from urequests import get 
DEBUG=0

def log(arg1, *vartuple):
    # timeInfo = time.strftime("%H:%M:%S %Y", time.localtime())
    if DEBUG== False :
        return
    data = str(arg1)
    for var in vartuple:
        data = data + str(var)
    data = '[' + str(millis()) + '] ' + data
    print(data)


os_time_start = time.ticks_ms()
def millis():
    return time.ticks_ms() - os_time_start

    
class  blinker:
  '''
  # key:密码
  #devTpye 设置设备类型:电灯:light,插座:outlet,多个插座:multi_outlet,传感器:sensor
  #cb 回调函数 例如 def cb(topic, msg):
  '''
  def __init__(self,key,cb,devTpye="light"):
    self.blinker_path='_blinker_conf.py'
    self.keepalive=120
    self.connect_count=0
    self.devTpye=devTpye
    self.cb=cb
    self.key=key
    self.info= self.read_conf()
    self.SERVER = "public.iot-as-mqtt.cn-shanghai.aliyuncs.com"
    self.USER=self.info['detail']['iotId']
    self.PWD=self.info['detail']['iotToken']
    self.CLIENT_ID =  self.info['detail']['deviceName']
    self.c=MQTTClient(client_id=self.CLIENT_ID,server=self.SERVER,user=self.USER,password=self.PWD,keepalive=self.keepalive)
    self.c.DEBUG = True
    self.c.set_callback(self.cb)
    self.subtopic="/"+self.info['detail']['productKey']+"/"+self.info['detail']['deviceName']+"/r"
    self.pubtopic=b"/"+self.info['detail']['productKey']+"/"+self.info['detail']['deviceName']+"/s"
  #获取登录信息
  def getInfo(self,auth,type_="light"):
      log("getInfo:抓取登录信息")
      host = 'https://iot.diandeng.tech'
      url = '/api/v1/user/device/diy/auth?authKey=' + auth + "&miType="+type_+"&version=0.1.0"
      log("url:",url)
      data =  get(host + url).text
      log("data:",data)
      
      fo = open(self.blinker_path, "w")
      fo.write(str(data))
      fo.close()
      return data 


  #MQQT 连接    
  def connect(self):
    log("connect:准备连接....")

    if DEBUG:
      log("user:",self.USER,"CLIENT_ID:",self.CLIENT_ID,self.subtopic,"/r",self.pubtopic)
    try:
      if not self.c.connect(clean_session=False):
            try: 
              self.c.subscribe(self.subtopic)
              self.connect_count+=1
              self.log()
              log("新会话已连接.")
            except:
              log("连接失败")
              self.getInfo(self.key,self.devTpye)
              self.__init__(self.key,self.devTpye)
      
    except:
      log("检查网络或登录信息")
  #mqtt 信息轮询
  def log(self):
    if DEBUG:
      log("连接: ",self.connect_count," 次")
  def check_msg(self):
      try:
        self.c.check_msg()
      except OSError as e:
        self.connect()
  #mqtt 心跳回复
  def ping(self): 
    #
    
    
    
    
    try:
        self.c.ping()
        if DEBUG:
          print("Mqtt Ping")
    except OSError as e:
        self.connect()
  def onLine(self):
      try:
        self.publish({"state":"online"}) 
      except OSError as e:
        self.connect()     
  #数据整合成特定json
  def playload(self,msg,toDevice="",deviceType='OwnApp'):
     if toDevice=="":
       toDevice=self.info['detail']['uuid']
     _data= ujson.dumps({
     'fromDevice': self.info['detail']['deviceName'] ,
     'toDevice':   toDevice,
     'data':       msg ,
     'deviceType': deviceType})
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
        if DEBUG:
            log ("Mqtt发送>>>>",dict)        
      except OSError as e:
        if DEBUG:
           log ("publish:",e)
        self.connect()
        
        
  
  def read_conf(self):
      """
      从文件中获取json数据
      :param path: 文件路径
      :return json_data: 返回转换为json格式后的json数据
      """
      log("读取登录数据....")
      try:
          with open(self.blinker_path, 'r+') as f:
              try:
                  json_data = ujson.load(f)
              except Exception as e:
                log('不是json文件' + str(e))

          log("文件内容:",json_data)
          return json_data
      except Exception as e:
          log("文件不存在!")
          self.getInfo(self.key,self.devTpye)
          return  self.read_conf(self.blinker_path)



