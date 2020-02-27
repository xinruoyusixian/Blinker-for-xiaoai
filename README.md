基于Blinker的micopython 的小爱同学的代码 
========
支持 电灯 和温度计的控制


![Image text](https://github.com/xinruoyusixian/Bxm/blob/master/E700CB39694B28FB598D20E738A8F7FA.jpg?raw=true)
##交互流程

### 1.小爱请求状态 关键字
{"get":"state"}
###### 完整数据：
{"deviceType":"DiyArduino","data":{"get":"state"},"fromDevice":"MIOT","toDevice":"448D910CAQAQ5CWMT6PW41K7"}
### 2.回复设备 当前状态 
"data":  {"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"}
**如果是设备是温度则发送回应就可以了 {"temp":"20","humi":"20","pm25":"20","co2":"20"} **
###### 完整数据：
{"data":{"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
### 3.小爱下发指令：
"data":    {"set":{"pState":true}}
###### 完整数据 :
{"deviceType":"DiyArduino","data":{"set":{"pState":true}},"fromDevice":"MIOT","toDevice":"448D910CAQAQ5CWMT6PW41K7"}
### 4.回复指令完成状态：
"data":  {"pState":"True"}
###### 完整数据：
{"data":{"pState":"True"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}

至此一个指令完整的交互完成
延申：
当设备需要更改颜色，亮度，色温的时候

小爱会在第三步 和第四步 下发的data: 数据有变化
下发颜色设置
{"set":{"col":255}}
回复： {"col":255,"clr":255}
下发亮度设置
{"set":{"bright":21}}
回复： {"bright":"21"}

以下是日志 可以研究一下 
#####小请求获得状态
[992546] Got: {"deviceType":"DiyArduino","data":{"get":"state"},"fromDevice":"MIOT","toDevice":"448D910CAQAQ5CWMT6PW41K7"}
[992547] data: {"get":"state"}
[992549] fromDevice: MIOT
[992551] form MIOT
[992573] MIOT parse data: {"get":"state"}
[992574] MIOT Query codes: 0
[992574] MIOT Query All
[992575] response to MIOT: {"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"}
[992580] isJson: {"data":{"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[992596] MQTT MIOT Publish...
[992598] Freeheap: 5808
[992664] {"data":{"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[992669] ...OK!
[992670] Freeheap: 5808
##### 回复小爱电灯状态
[992672] Send: {"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"}
##### 小爱下发设置开关指令  "pState" 为true   是开  ,false 是关
[992956] Got: {"deviceType":"DiyArduino","data":{"set":{"pState":true}},"fromDevice":"MIOT","toDevice":"448D910CAQAQ5CWMT6PW41K7"}
[992957] data: {"set":{"pState":true}}
[992960] fromDevice: MIOT
[992962] form MIOT
[992985] MIOT parse data: {"set":{"pState":true}}
##### 设置完毕后回复给小爱
[992985] need set power state: on
[992986] response to MIOT: {"pState":"True"}
[992986] isJson: {"data":{"pState":"True"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[992997] MQTT MIOT Publish...
[992999] Freeheap: 4808
[993026] {"data":{"pState":"True"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[993027] ...OK!
[993027] Freeheap: 4808
[993030] Send: {"pState":"True"}
[999301] Got: {"deviceType":"DiyArduino","data":{"get":"state"},"fromDevice":"MIOT","toDevice":"448D910CAQAQ5CWMT6PW41K7"}
[999302] data: {"get":"state"}
[999303] fromDevice: MIOT
[999306] form MIOT
[999328] MIOT parse data: {"get":"state"}
[999328] MIOT Query codes: 0
[999328] MIOT Query All
[999330] response to MIOT: {"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"}
[999334] isJson: {"data":{"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[999351] MQTT MIOT Publish...
[999353] Freeheap: 5808
[999380] {"data":{"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[999385] ...OK!
[999386] Freeheap: 5808
[999388] Send: {"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"}
[1010779] Got: {"deviceType":"DiyArduino","data":{"set":{"pState":false}},"fromDevice":"MIOT","toDevice":"448D910CAQAQ5CWMT6PW41K7"}
[1010781] data: {"set":{"pState":false}}
[1010783] fromDevice: MIOT
[1010786] form MIOT
##### 关灯指令下发
[1010808] MIOT parse data: {"set":{"pState":false}}
[1010809] need set power state: off
[1010809] response to MIOT: {"pState":"False"}
[1010810] isJson: {"data":{"pState":"False"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1010821] MQTT MIOT Publish...
[1010823] Freeheap: 4784
[1010849] {"data":{"pState":"False"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1010850] ...OK!
[1010851] Freeheap: 4784
##### 回复关灯指令
[1010853] Send: {"pState":"False"}
[1029815] Got: {"deviceType":"DiyArduino","data":{"get":"state"},"fromDevice":"MIOT","toDevice":"448D910CAQAQ5CWMT6PW41K7"}
[1029816] data: {"get":"state"}
[1029818] fromDevice: MIOT
[1029820] form MIOT
[1029843] MIOT parse data: {"get":"state"}
[1029843] MIOT Query codes: 0
[1029843] MIOT Query All
[1029845] response to MIOT: {"pState":"False","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"}
[1029850] isJson: {"data":{"pState":"False","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1029866] MQTT MIOT Publish...
[1029869] Freeheap: 5808
[1029895] {"data":{"pState":"False","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1029899] ...OK!
[1029901] Freeheap: 5808
[1029903] Send: {"pState":"False","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"}
[1041261] Got: {"deviceType":"DiyArduino","data":{"set":{"pState":true}},"fromDevice":"MIOT","toDevice":"448D910CAQAQ5CWMT6PW41K7"}
[1041262] data: {"set":{"pState":true}}
[1041265] fromDevice: MIOT
[1041268] form MIOT
[1041290] MIOT parse data: {"set":{"pState":true}}
[1041291] need set power state: on
[1041291] response to MIOT: {"pState":"True"}
[1041292] isJson: {"data":{"pState":"True"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1041303] MQTT MIOT Publish...
[1041305] Freeheap: 4744
[1041333] {"data":{"pState":"True"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1041334] ...OK!
[1041335] Freeheap: 4744
[1041337] Send: {"pState":"True"}
[1069242] Got: {"deviceType":"DiyArduino","data":{"get":"state"},"fromDevice":"MIOT","toDevice":"448D910CAQAQ5CWMT6PW41K7"}
[1069243] data: {"get":"state"}
[1069245] fromDevice: MIOT
[1069247] form MIOT
[1069270] MIOT parse data: {"get":"state"}
[1069270] MIOT Query codes: 0
[1069270] MIOT Query All
[1069272] response to MIOT: {"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"}
[1069276] isJson: {"data":{"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1069293] MQTT MIOT Publish...
[1069295] Freeheap: 5744
[1069323] {"data":{"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1069327] ...OK!
[1069329] Freeheap: 5744
[1069331] Send: {"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"}
[1076057] Got: {"deviceType":"DiyArduino","data":{"get":"state"},"fromDevice":"MIOT","toDevice":"448D910CAQAQ5CWMT6PW41K7"}
[1076058] data: {"get":"state"}
[1076059] fromDevice: MIOT
[1076062] form MIOT
[1076084] MIOT parse data: {"get":"state"}
[1076085] MIOT Query codes: 0
[1076085] MIOT Query All
[1076086] response to MIOT: {"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"}
[1076091] isJson: {"data":{"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1076107] MQTT MIOT Publish...
[1076110] Freeheap: 5744
[1076139] {"data":{"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1076143] ...OK!
[1076145] Freeheap: 5744
[1076147] Send: {"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"}
[1096793] Got: {"deviceType":"DiyArduino","data":{"set":{"bright":21}},"fromDevice":"MIOT","toDevice":"448D910CAQAQ5CWMT6PW41K7"}
##### 设置亮度
[1096794] data: {"set":{"bright":21}}
[1096796] fromDevice: MIOT
[1096799] form MIOT
[1096821] MIOT parse data: {"set":{"bright":21}}
[1096822] need set brightness: 21
[1096822] now set brightness: 21
[1096824] response to MIOT: {"bright":"21"}
[1096825] isJson: {"data":{"bright":"21"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1096836] MQTT MIOT Publish...
[1096838] Freeheap: 4840
[1096868] {"data":{"bright":"21"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1096869] ...OK!
[1096870] Freeheap: 4840
[1096872] Send: {"bright":"21"}
[1113068] Got: {"deviceType":"DiyArduino","data":{"get":"state"},"fromDevice":"MIOT","toDevice":"448D910CAQAQ5CWMT6PW41K7"}
[1113069] data: {"get":"state"}
[1113071] fromDevice: MIOT
[1113073] form MIOT
[1113096] MIOT parse data: {"get":"state"}
[1113096] MIOT Query codes: 0
[1113096] MIOT Query All
[1113098] response to MIOT: {"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"}
[1113102] isJson: {"data":{"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1113119] MQTT MIOT Publish...
[1113121] Freeheap: 5808
[1113150] {"data":{"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1113154] ...OK!
[1113156] Freeheap: 5808
[1113158] Send: {"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"}
[1136454] Got: {"deviceType":"DiyArduino","data":{"get":"state"},"fromDevice":"MIOT","toDevice":"448D910CAQAQ5CWMT6PW41K7"}
[1136455] data: {"get":"state"}
[1136457] fromDevice: MIOT
[1136459] form MIOT
[1136481] MIOT parse data: {"get":"state"}
[1136482] MIOT Query codes: 0
[1136482] MIOT Query All
[1136483] response to MIOT: {"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"}
[1136488] isJson: {"data":{"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1136504] MQTT MIOT Publish...
[1136507] Freeheap: 5808
[1136536] {"data":{"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1136540] ...OK!
[1136542] Freeheap: 5808
[1136544] Send: {"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"}
[1136561] Got: {"deviceType":"DiyArduino","data":{"set":{"col":255}},"fromDevice":"MIOT","toDevice":"448D910CAQAQ5CWMT6PW41K7"}
##### 设置颜色
[1136564] data: {"set":{"col":255}}
[1136566] fromDevice: MIOT
[1136569] form MIOT
[1136591] MIOT parse data: {"set":{"col":255}}
[1136592] need set color: 255
[1136592] colorR: 0, colorG: 0, colorB: 255
[1136593] response to MIOT: {"col":255,"clr":255}
[1136596] isJson: {"data":{"col":255,"clr":255},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1136607] MQTT MIOT Publish...
[1136610] Freeheap: 4808
[1136676] {"data":{"col":255,"clr":255},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1136677] ...OK!
[1136678] Freeheap: 4808
##### 回复颜色
[1136680] Send: {"col":255,"clr":255}
[1143586] Got: {"deviceType":"DiyArduino","data":{"set":{"col":16777215}},"fromDevice":"MIOT","toDevice":"448D910CAQAQ5CWMT6PW41K7"}
[1143588] data: {"set":{"col":16777215}}
[1143591] fromDevice: MIOT
[1143593] form MIOT
[1143616] MIOT parse data: {"set":{"col":16777215}}
[1143616] need set color: 16777215
[1143617] colorR: 255, colorG: 255, colorB: 255
[1143618] response to MIOT: {"col":16777215,"clr":16777215}
[1143622] isJson: {"data":{"col":16777215,"clr":16777215},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1143635] MQTT MIOT Publish...
[1143637] Freeheap: 4784
[1143665] {"data":{"col":16777215,"clr":16777215},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1143666] ...OK!
[1143668] Freeheap: 4784
[1143670] Send: {"col":16777215,"clr":16777215}
[1168469] Got: {"deviceType":"DiyArduino","data":{"get":"state"},"fromDevice":"MIOT","toDevice":"448D910CAQAQ5CWMT6PW41K7"}
[1168470] data: {"get":"state"}
[1168471] fromDevice: MIOT
[1168474] form MIOT
[1168496] MIOT parse data: {"get":"state"}
[1168496] MIOT Query codes: 0
[1168497] MIOT Query All
[1168498] response to MIOT: {"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"}
[1168503] isJson: {"data":{"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1168519] MQTT MIOT Publish...
[1168522] Freeheap: 5808
[1168549] {"data":{"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"},"fromDevice":"448D910CAQAQ5CWMT6PW41K7","toDevice":"MIOT_r","deviceType":"vAssistant"}
[1168554] ...OK!
[1168555] Freeheap: 5808
[1168558] Send: {"pState":"True","col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"}

