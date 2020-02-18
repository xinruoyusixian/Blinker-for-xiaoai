from robust import MQTTClient
import utime,ujson,urequests,lib,network


def wifi(ssd,pwd):
    wifi0 = network.WLAN(network.STA_IF)  #创建连接对象 如果让ESP32接入WIFI的话使用STA_IF模式,若以ESP32为热点,则使用AP模式
    if not wifi0.isconnected(): #判断WIFI连接状态
        print('connecting to network[正在连接]...')
        wifi0.active(True) #激活WIFI
        wifi0.connect(ssd, pwd) #essid为WIFI名称,password为WIFI密码
        while not wifi0.isconnected():
            pass # WIFI没有连接上的话做点什么,这里默认pass啥也不做
    print('network config[网络信息]:', wifi0.ifconfig())
##这里自己写连接WiFiSSD 和密码的
lib.wifi("PDCN","1234567788")
lib.update_time()
#json解析成对象
def json(j):
  return  ujson.loads(j)
#获取信息
def getInfo(auth):
    host = 'https://iot.diandeng.tech'
    url = '/api/v1/user/device/diy/auth?authKey=' + auth
    print (host + url)
    data =  json(urequests.get(host + url).text)
    
    ''' deviceName = data['detail']['deviceName'] iotId =
    data['detail']['iotId'] iotToken = data['detail']['iotToken']
    productKey = data['detail']['productKey'] uuid =
    data['detail']['uuid'] broker = data['detail']['broker']] ''' 
    return data
#授权KEY
key='授权KEY'
# 电灯"&miType=light"
#插座"&miType=outlet"
#多个插座"&miType=multi_outlet"
#传感器&miType=sensor"
type="https://iot.diandeng.tech/api/v1/user/device/diy/auth?authKey="+key+"&miType=light&version=1.2.2"
print ("这个复制到浏览器运行只要运行一次就可以了/r"+type)
info=  getInfo(key)
def playload(msg,toDevice=info['detail']['uuid'],deviceType='OwnApp'):
   _data= ujson.dumps({
   'fromDevice': info['detail']['deviceName'] ,
   'toDevice':   toDevice,
   'data':       msg , 
   'deviceType': deviceType})
   print ("Mqtt发送>>>>",_data)
   return _data

#处理小爱响应  
def MI(msg):
  msg=json(msg)
  try:
    if(msg['data']['get']=="state"):
      #回应小爱
      c.publish(pubtopic,playload('{"State":True}',toDevice='MIOT',deviceType='vAssistant'))
      c.publish(pubtopic,playload({ 'temp':'100','humi':'0', 'pm25':'10','pm10':'10','co2':'10'},toDevice='MIOT_r',deviceType='vAssistant'))
  except:
    pass
  try:  
    if(msg['data']['set']['pState']==1):
      print("开启")
    if(msg['data']['set']['pState']==0):
      print ("关闭")
  except:
    pass
 
#mqtt消息处理  
def sub_cb(topic, msg):
  print("Mqtt接收<<<<",msg)
  msgs=str(json(msg))
  if msgs.find("MIOT")!=-1:
      MI(msg)
  if msgs.find("btn")!=-1:
    if json(msg)['data']['btn-abc']=="tap":
      c.publish(pubtopic,playload('{"vibrate":1000}')) 
      print ("已发送")
  #APP心跳回复
  c.publish(pubtopic,playload('{"state":"online"}') )  
#设置设备类型       

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
