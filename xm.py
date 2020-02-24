



from robust import MQTTClient


import utime,ujson,urequests,ntptime


import network


from machine import RTC,Pin





#gpio 控制的引脚


#st 引脚的值


def pin(gpio=2,st=1):


    if st==1:


        Pin(gpio,Pin.OUT).value(1)


    elif st==0:


        Pin(gpio,Pin.OUT).value(0)
    elif st==2:
        return Pin(gpio).value()


def wifi(ssd,pwd):


    #连接WiFi




    wifi0 = network.WLAN(network.STA_IF)  #创建连接对象 如果让ESP32接入WIFI的话使用STA_IF模式,若以ESP32为热点,则使用AP模式








    if not wifi0.isconnected(): #判断WIFI连接状态








        print('connecting to network[正在连接]...')


        wifi0.active(True) #激活WIFI


        wifi0.connect(ssd, pwd) #essid为WIFI名称,password为WIFI密码


        while not wifi0.isconnected():


            pass # WIFI没有连接上的话做点什么,这里默认pass啥也不做
    print('network config[网络信息]:', wifi0.ifconfig())
    
def json(j):
  #json解析成对象
  return  ujson.loads(j)

def getInfo(auth,type_="light"):
    #获取信息
    # 电灯"&miType=light"
    #插座"&miType=outlet"
    #多个插座"&miType=multi_outlet"
    #传感器&miType=sensor"
    #设置设备类型
    host = 'https://iot.diandeng.tech'
    url = '/api/v1/user/device/diy/auth?authKey=' + auth + "&miType="+type_+"&version=1.2.2"
    print (host + url)
    data =  json(urequests.get(host + url).text) 
    ''' 
    deviceName = data['detail']['deviceName'] iotId =
    data['detail']['iotId'] iotToken = data['detail']['iotToken']
    productKey = data['detail']['productKey'] uuid =
    data['detail']['uuid'] broker = data['detail']['broker']] 
    ''' 
    return data
def MI(msg):


  #2秒内响应否则小爱会说设备不理他


  #回应小爱


  #可按需发送 也可分开发送


  #当小爱同学向设备发起控制, 设备端需要有对应控制处理函数


  #参考来源：https://github.com/blinker-iot/blinker-library/blob/20125223dc3511ecf08a5afe73de0dadef5519c0/src/Functions/BlinkerMIOT.h 

  #看起来一起把消息发给小爱服务器比较妥当


  '''


  #数据结构


  {"pState":"true",#反馈电源状态  [必须]


  'State':'True', #设备状态  [必须]








  'mode":'',      #反馈运行模式 [为电灯或温度计时可不加] [DAY	日光,NIGHT	月光,COLOR	彩光,WARMTH	温馨,TV 电视模式,READING  阅读模式,COMPUTER	电脑模式]








  'num':'0',      # 未知 0 或 ""


  'temp':'100',   #温度摄氏度[当设备为温度计时]


  'humi':'0',     #湿度      [当设备为温度计时]








  'pm25':'10',    #PM2.5浓度 [当设备为温度计时]






  'pm10':'10',    #PM 10浓度 [当设备为温度计时]








  'co2':'10'      #co2浓度   [当设备为温度计时]


  }
灯
[57373] Got: {"deviceType":"DiyArduino","data":{"get":"state"},"fromDevice":"MIOT","toDevice":"448D910CAQAQ5CWMT6PW41K7"}
[57406] isJson: {"data":{"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
#如果是温度则发送回应就可以了 {"temp":"20","humi":"20","pm25":"20","co2":"20"}



  '''


  #c.publish(pubtopic,playload({'pState':'true', 'State':'True','num':'1','temp':'100','humi':'0', 'pm25':'10','pm10':'10','co2':'10'},toDevice='MIOT_r',deviceType='vAssistant'))

  #处理小爱响应  
  try:
    if(msg['get']=="state"):
      c.publish(pubtopic,playload({"State":"True","pState":"true","num":"0","temp":"100","humi":"0", "pm25":"10","pm10":"10","co2":"10"},toDevice="MIOT_r",deviceType="vAssistant"))
      pass
  except:
    pass
  #作为电灯时的操作  
  
  try:
    if(msg['set']['pState']==1):
      if pin(2,2)==0:
        pass
      else:
        pin(2,0)
      print("开启")
    if(msg['set']['pState']==0):
      if pin(2,2)==1:
        pass
      else:
        pin(2,1)
      print ("关闭")
    #获取电源状态，操作完毕回复小爱 
    pin_State= "true" if pin(2,2)==0 else "false"
    c.publish(pubtopic,playload({"pState":pin_State, 'State':'True',},toDevice='MIOT_r',deviceType='vAssistant'))
  except:
    pass
  print ("已回复小爱")
#mqtt消息处理  
def sub_cb(topic, msg):
  print("Mqtt接收<<<<",msg)
  msgs=str(json(msg))
  msg=json(msg)['data']
  if msgs.find("MIOT")!=-1:
      MI(msg)
  #APP心跳回复
  c.publish(pubtopic,playload('{"state":"online"}') )
  
  
wifi("PDCN","1234567788")
#授权KEY
key='60975280bf3e'
# 电灯"light"
#插座"outlet"
#多个插座"multi_outlet"
#传感器s"ensor"
#设置设备类型
devTpye="light"
info=  getInfo(key,type_=devTpye)


def playload(msg,toDevice=info['detail']['uuid'],deviceType='OwnApp'):


    #处理需要发送的数据


   _data= ujson.dumps({


   'fromDevice': info['detail']['deviceName'] ,


   'toDevice':   toDevice,

   'data':       msg , 
   'deviceType': deviceType})
   print ("Mqtt发送>>>>",_data)
   return _data
#mqtt 连接部分

SERVER = "public.iot-as-mqtt.cn-shanghai.aliyuncs.com"
USER=info['detail']['iotId']
PWD=info['detail']['iotToken']
CLIENT_ID =  info['detail']['deviceName']
c=MQTTClient(client_id=CLIENT_ID,server=SERVER,user=USER,password=PWD,keepalive=300)
c.DEBUG = True
c.set_callback(sub_cb)
subtopic="/"+info['detail']['productKey']+"/"+info['detail']['deviceName']+"/r"
pubtopic=b"/"+info['detail']['productKey']+"/"+info['detail']['deviceName']+"/s"
print(subtopic,"/r",pubtopic)
if not c.connect(clean_session=False):
      print("Ne session being set .")
      c.subscribe(subtopic)
#发送连接状态
c.publish(pubtopic,playload('{"state":"connected"}'))      
while 1:
  utime.sleep(1)
  c.check_msg()
