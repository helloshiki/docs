<span id='TOC'/>

# 目录
- [1. 请求协议](#id_1) 
	- [1.1 协议与uri](#id_1_1) 
	- [1.2 错误代码](#id_1_2) 
	- [1.3 demo](#id_1_3) 
- [2. 接入信息查询 AccessInfoQuery](#id_2) 
	- [2.1 getPONIfPhyStatus](#id_2_1) 
	- [2.2 getPONIfUpTime](#id_2_2) 
	- [2.3 getPONIfRegisterStatus](#id_2_3) 
	- [2.4 getUplinkIfStats](#id_2_4) 
	- [2.5 getWANIfList](#id_2_5) 
	- [2.6 getWANIfStats](#id_2_6) 
	- [2.7 getWANIfInfo](#id_2_7) 
	- [2.8 getWanIfBandwidth ](#id_2_8) 
	- [2.9 getWANIfStatus](#id_2_9) 
	- [2.10 getInternetWANIndex](#id_2_10) 
- [3. XXXX](#id_3) 
	- [3.1 XXX](#id_3_1) 
	- [3.2 XXX](#id_3_2) 
	- [3.3 XXX](#id_3_3) 
	- [3.4 XXX](#id_3_4) 
- [4. XXXX](#id_4) 
	- [4.1 XXX](#id_4_1) 
	- [4.2 XXX](#id_4_2) 
- [5. XXXX](#id_5) 
	- [5.1 XXX](#id_5_1) 
	- [5.2 XXX](#id_5_2) 
- [6. XXXX](#id_6) 
	- [6.1 XXX](#id_6_1) 
- [7. XXXX](#id_7) 
	- [7.1 XXX](#id_7_1) 
	- [7.2 XXX](#id_7_2) 
	- [7.3 XXX](#id_7_3) 
	- [7.4 XXX](#id_7_4) 
- [8. XXXX](#id_8) 
	- [8.1 XXX](#id_8_1) 
	- [8.2 XXX](#id_8_2) 
	- [8.3 XXX](#id_8_3) 
	- [8.4 XXX](#id_8_4) 

<span id='id_1'/>

# 1. 请求协议
<span id='id_1_1'/>

## 1.1 协议与uri 

* 统一使用 [JSON-RPC 2.0](https://www.jsonrpc.org/specification)
* 请求uri为 `/rpc`

<span id='id_1_2'/>

## 1.2 错误代码
code | message | description 
------------ | -------------- | -------------- 
-32700 | Parse error | 语法解析错误             服务端接收到无效的json。该错误发送于服务器尝试解析json文本
-32600 | Invalid Request | 无效请求                    发送的json不是一个有效的请求对象 
-32601 | Method not found  | 找不到方法                该方法不存在或无效 
-32602 | Invalid params | 无效的参数	            无效的方法参数
-32603 | Internal error | 内部错误	                JSON-RPC内部错误 
-32000 to -32099 | | Server error服务端错误, 预留用于自定义的服务器错误

<span id='id_1_3'/>
## 1.3 demo
```shell
curl http://127.0.0.1:8001/rpc -d '{
    "jsonrpc":"2.0",
    "id":1,
    "method":"wireless.deviceinfo",
    "params":{
    }
}'
```
```shell
{
    "id":1,
    "jsonrpc":"2.0",
    "result":{
        "from":"wireless",
        "timestamp":"Wed Jul  1 04:50:01 2020"
    }
}
```
[TOC](#TOC) 

<span id='id_2'/>
# 2. 接入信息查询 AccessInfoQuery
<span id='id_2_1'/>
## 2.1 getPONIfPhyStatus    
<span id='id_2_2'/>
## 2.2 getPONIfUpTime
<span id='id_2_3'/>
## 2.3 getPONIfRegisterStatus
<span id='id_2_4'/>
## 2.4 getUplinkIfStats
* description: `查询上行口报文统计`
* method: `AccessInfoQuery.getUplinkIfStats`
* params: 
* response:

参数名 | 必选 | 类型 | 说明
------------ | ------------- | -------------- | -------------- 
UsStats | Y | int | 上行统计，单位byte
DsStats | Y | int | 下行统计，单位byte

 * demo
```bash
curl http://127.0.0.1:8001/rpc -d '{
    "id":1,
    "method":"AccessInfoQuery.getUplinkIfStats",
    "params":{}
}'
```
```js
{
    "jsonrpc": "2.0",
    "id": "1",
    "result": {
        "UsStats": 506319210, 
        "DsStats": 2992356088
    }
}
```
[TOC](#TOC) 

<span id='id_2_5'/>
## 2.5 getWANIfList 
* description: `获取当前网关的WAN连接序号及名称列表`
* method: `AccessInfoQuery.getWANIfList`
* params: 
* response:

参数名 | 必选 | 类型 | 说明
------------ | ------------- | -------------- | -------------- 
List | Y | array | WAN列表
List[i].Index | Y | int | WAN序号
List[i].Name | Y | string | WAN连接名称，规则：`序号_关键字_桥接或路由方式_VLAN信息` 

 * memo
   * 序号: 1~99
   * VLAN信息
     * Z: 上行WAN采用VLAN信息，具体为：VID_Z中Z为实际VLAN_ID值
   * 桥接或路由方式
     * B: Bridge方式
     * R: Router方式
   * 关键字:
     * TR069: 表示此连接仅用于管理
     * INTERNET: 表示此连接仅用于上网应用，但不支持TR069
     * TR069_INTERNET: 表示此连接同时用于管理和上网应用
     * VOICE: 表示此连接仅用于语音通道
     * TR069_VOICE: 表示此连接仅用于管理和与语音应用
     * VOICE_INTERNET: 表示此连接仅用于上网和语音应用
     * TR069_VOICE _INTERNET: 表示此连接仅用于管理、上网和语音应用
     * OTHER: 其他连接（除以上的应用外，均使用OTHER，如STB和WLAN共享等）
 * demo
```bash
curl http://127.0.0.1:8001/rpc -d '{
    "id":10,
    "method":"AccessInfoQuery.getWANIfList",
    "params":{}
}'
```
```js
{
    "jsonrpc":"2.0",
    "id":10,
    "result":[
        {
            "Index":1,
            "Name":"1_TR069_INTERNET_R_1"
        },
        {
            "Index":2,
            "Name":"2_INTERNET_R_2"
        }
    ]
}
```
[TOC](#TOC) 

<span id='id_2_6'/>
## 2.6 getWANIfStats
* description: `查询WAN口报文统计`
* method: `AccessInfoQuery.getWANIfStats`
* params: 

|  参数名  | 必选 | 类型 | 说明          |
| :------: | ---- | ---- | ------------- |
| WanIndex | Y    | int  | WAN连接的序号 |

* response:

 参数名  | 必选 | 类型 | 说明               
------------ | ------------- | -------------- | -------------- 
 UsStats | Y    | int  | 上行统计，单位byte 
 DsStats | Y    | int  | 下行统计，单位byte 

 * demo
```bash
curl http://127.0.0.1:8001/rpc -d '{
    "id":1,
    "method":"AccessInfoQuery.getWANIfStats",
    "params":{"WanIndex": 1}
}'
```
```js
{
    "jsonrpc": "2.0",
    "id": "1",
    "result": {
        "UsStats": 506319210, 
        "DsStats": 2992356088
    }
}
```
[TOC](#TOC) 
<span id='id_2_7'/>

## 2.7 getWANIfInfo
* description: `查询WAN口详细信息`
* method: `AccessInfoQuery.getWANIfInfo`
* params: 

|  参数名  | 必选 | 类型 | 说明          |
| :------: | ---- | ---- | ------------- |
| WanIndex | Y    | int  | WAN连接的序号 |

* response:

| 参数名                      | 必选 | 类型   | 说明                                                         |
| --------------------------- | ---- | ------ | ------------------------------------------------------------ |
| LanInterface                | N    | string | 和本WAN连接绑定的LAN侧端口列表，包括以太网端口、无线SSID，以逗号分割<br/>格式：LANx,SSIDx |
| VLANMode                    | N    | int    | VLAN启用模式，以下值之一：<br/>0 表示不启用<br/>1 表示保持原来的标志位值<br/>2 表示重写VLAN |
| VLANIDMark                  | N    | int    | WAN连接的VLANID                                              |
| ServiceMode                 | N    | string | 建立连接时所选择的关键字,取值为如下8个之一TR069、VOICE、INTERNET、TR069_INTERNET、TR069_VOICE、VOICE_INTERNET、TR069_VOICE _INTERNET、OTHER |
| 802-1pMark                  | N    | string | WAN连接的802.1p优先级                                        |
| MulticastVlan               | N    | int    | 组播VLAN<br/>-1表示不启用                                    |
| LanInterface-DHCPEnable     | N    | bool   | 是否启用本WAN绑定的LAN侧端口的DHCP分配IP功能。TRUE表示启用DHCP分配IP，FALSE表示DHCP不分配 |
| IPMode                      | N    | int    | 控制IPv4和IPv6协议使能，如下值之一：<br/>1: IPv4<br/>2: IPv6<br/>3: IPv4+IPv6 |
| ConnectionType              | N    | string | WAN连接的类型，如下值之一：IP_Routed/IP_Bridged/PPPoE_Bridged/PPPoE_Routed |
| NATEnabled                  | N    | bool   | 是否启用NAT。TRUE表示启用，FALSE表示禁用。                   |
| Username                    | N    | string | PPPoE鉴权的用户名                                            |
| Password                    | N    | string | PPPoE鉴权的密码                                              |
| AddressingType              | N    | string | IPv4地址分配方式，如下值之一：<br/>DHCP <br/>Static<br/>仅针对ConnectionType为IP_Routed的WAN连接 |
| ExternalIPAddress           | N    | string | WAN连接当前IP地址                                            |
| SubnetMask                  | N    | string | WAN连接子网掩码                                              |
| DefaultGateway              | N    | string | WAN连接默认网关                                              |
| DNSEnabled                  | N    | string | WAN连接是否使能DNS                                           |
| DNSServers                  | N    | string | WAN连接当前DNS列表。<br/>多个以逗号隔开。                    |
| MACAddress                  | N    | string | WAN连接的MAC地址                                             |
| ConnectionTrigger           | N    | string | 连接触发方式，如下值之一：<br/>OnDemand<br/>AlwaysOn<br/>Manual<br/>仅针对ConnectionType为PPPoE_Routed的WAN连接 |
| IPv6IPAddressOrigin         | N    | string | IPv6地址获取机制，如下值之一：<br/>AutoConfigured：通过RA通告自动获取<br/>DHCPv6<br/>Static<br/>None |
| IPv6IPAddress               | N    | string | WAN连接的IPv6地址，仅静态分配地址时可写。                    |
| IPv6DNSServers              | N    | string | WAN连接IPv6地址别名                                          |
| IPv6PrefixDelegationEnabled | N    | bool   | WAN连接是否需要获得Prefix Delegation，当建立只包含TR069或VOIP属性的WAN连接时，该参数应为FALSE。 |
| IPv6PrefixAlias             | N    | string | 前缀地址别名                                                 |
| IPv6PrefixOrigin            | N    | string | 前缀地址获取机制，如下值之一：<br/>PrefixDelegation<br/>Static<br/>PPPoE<br/>None |
| IPv6Prefix                  | N    | string | 前缀地址别名                                                 |
| IPv6PrefixPltime            | N    | int    | 公告前缀的preferred lifetime（单位：秒）                     |
| IPv6PrefixVltime            | N    | int    | 公告前缀的valid lifetime（单位：秒）                         |
| IPv6DefaultGateway          | N    | string | IPv6默认网关                                                 |
| IPv6DomainName              | N    | string | IPv6域名                                                     |
| IPv6DsliteEnable            | N    | bool   | 是否启用DS-lite功能。TRUE表示启用，FALSE表示禁用。           |
| IPv6AftrMode                | N    | int    | AFTR配置模式，如下值之一：<br/>0：为自动获取方式；<br/>1：指定方式 |
| IPv6AftrAddress             | N    | string | AFTR地址，可为域名方式或者IP地址方式。                       |

 * demo
```bash
curl http://127.0.0.1:8001/rpc -d '{
    "id":10,
    "method":"AccessInfoQuery.getWANIfInfo",
    "params":{"WanIndex": 1}
}'
```
```js
{
    "result":{
        "VLANMode":0,
        "ServiceMode":"TR069_INTERNET",
        "SubnetMask":"255.255.0.0",
        "DNSEnabled":true,
        "NATEnabled":true,
        "IPMode":1,
        "AddressingType":"DHCP",
        "Username":"PPPoE_Username",
        "LanInterface-DHCPEnable":true,
        "MACAddress":"E4:67:1E:0C:CF:2E",
        "ConnectionType":"PPPoE_Routed",
        "DefaultGateway":"172.19.1.1",
        "Password":"PPPoE_Password",
        "DNSServers":"8.8.8.8,114.114.114.114",
        "ExternalIPAddress":"172.19.1.51",
        "LanInterface":"LAN1,SSID1"
    },
    "jsonrpc":"2.0",
    "id":10
}
```
[TOC](#TOC) 
<span id='id_2_8'/>
## 2.8 getWanIfBandwidth 
* description: `查询WAN口上下行速率`
* method: `AccessInfoQuery.getWanIfBandwidth`
* params: 

|  参数名  | 必选 | 类型 | 说明          |
| :------: | ---- | ---- | ------------- |
| WanIndex | Y    | int  | WAN连接的序号 |

* response:

 参数名  | 必选 | 类型 | 说明               
------------ | ------------- | -------------- | -------------- 
 UsBandwidth | Y    | int  | 下挂设备上行速率，单位为kbps
 DsBandwidth | Y    | int  | 下挂设备下行速率，单位为kbps

 * demo
```bash
curl http://127.0.0.1:8001/rpc -d '{
    "id":1,
    "method":"AccessInfoQuery.getWanIfBandwidth",
    "params":{"WanIndex": 1}
}'
```
```js
{
    "jsonrpc": "2.0",
    "id": "1",
    "result": {
        "UsBandwidth": 4096, 
        "DsBandwidth": 4096
    }
}
```
[TOC](#TOC) 
<span id='id_2_9'/>
## 2.9 getWANIfStatus
* description: `查询WAN口状态`
* method: `AccessInfoQuery.getWANIfStatus`
* params: 

|  参数名  | 必选 | 类型 | 说明          |
| :------: | ---- | ---- | ------------- |
| WanIndex | Y    | int  | WAN连接的序号 |

* response:

 参数名  | 必选 | 类型 | 说明               
------------ | ------------- | -------------- | -------------- 
 Uptime | Y    | int  | 该连接启动时间（单位：秒）
 ConnectionStatus | N   | string  | IPv4协议的连接状态，如下值之一：<br/>Unconfigured <br/>Connecting <br/>Connected <br/>PendingDisconnect <br/>Disconneting<br/>Disconnecting <br/>Disconnected 
 IPv6ConnStatus | N    | string | IPv6协议的连接状态，如下值之一：<br/>Unconfigured <br/>Connecting<br/>Authenticating <br/>Connected <br/>PendingDisconnect <br/>Disconnecting <br/>Disconnected 
 LastConnectionError | Y    | string  | 上次试图建立连接时的错误原因，针对PPPoE_Routed WAN如下值之一：<br/>ERROR_NONE <br/>ERROR_ISP_TIME_OUT <br/>ERROR_COMMAND_ABORTED <br/>ERROR_NOT_ENABLED_FOR_INTERNET <br/>ERROR_BAD_PHONE_NUMBER <br/>ERROR_USER_DISCONNECT <br/>ERROR_ISP_DISCONNECT <br/>ERROR_IDLE_DISCONNECT <br/>ERROR_FORCED_DISCONNECT <br/>ERROR_SERVER_OUT_OF_RESOURCES <br/>ERROR_RESTRICTED_LOGON_HOURS <br/>ERROR_ACCOUNT_DISABLED <br/>ERROR_ACCOUNT_EXPIRED <br/>ERROR_PASSWORD_EXPIRED <br/>ERROR_AUTHENTICATION_FAILURE <br/>ERROR_NO_DIALTONE <br/>ERROR_NO_CARRIER <br/>ERROR_NO_ANSWER <br/>ERROR_LINE_BUSY <br/>ERROR_UNSUPPORTED_BITSPERSECOND <br/>ERROR_TOO_MANY_LINE_ERRORS <br/>ERROR_IP_CONFIGURATION <br/>ERROR_UNKNOWN<br/>针对IP_Routed WAN如下值之一：<br/>ERROR_NONE <br/>ERROR_COMMAND_ABORTED <br/>ERROR_NOT_ENABLED_FOR_INTERNET <br/>ERROR_USER_DISCONNECT <br/>ERROR_ISP_DISCONNECT <br/>ERROR_IDLE_DISCONNECT <br/>ERROR_FORCED_DISCONNECT <br/>ERROR_NO_CARRIER <br/>ERROR_IP_CONFIGURATION <br/>ERROR_UNKNOWN 


 * demo
```bash
curl http://127.0.0.1:8001/rpc -d '{
    "id":1,
    "method":"AccessInfoQuery.getWANIfStatus",
    "params":{"WanIndex": 1}
}'
```
```js
{
    "id":1,
    "jsonrpc":"2.0",
    "result":{
        "LastConnectionError":"ERROR_NONE",
        "IPv6ConnStatus":"Unconfigured",
        "Uptime":1800,
        "ConnectionStatus":"Connected"
    }
}
```
[TOC](#TOC) 
<span id='id_2_10'/>
## 2.10 getInternetWANIndex
* description: `获取第一个Internet WAN连接的序号`
* method: `AccessInfoQuery.getInternetWANIndex`
* params:  
* response:

 参数名  | 必选 | 类型 | 说明               
------------ | ------------- | -------------- | -------------- 
 index | Y    | int  | >0 获取成功，返回WAN序号<br/>-1 失败 

 * demo
```bash
curl http://127.0.0.1:8001/rpc -d '{
    "id":1,
    "method":"AccessInfoQuery.getInternetWANIndex",
    "params":{}
}'
```
```js
{
    "jsonrpc": "2.0",
    "id": "1",
    "result": {
        "index": 1, 
    }
}
```
[TOC](#TOC) 
<span id='id_3'/>
# 3. WAN口配置
<span id='id_3_1'/>
## 3.1 addWANIf
<span id='id_3_2'/>
## 3.2 setWANIf
<span id='id_3_3'/>
## 3.3 deleteWANIf
<span id='id_3_4'/>
## 3.4 setDevicePassword

<span id='id_4'/>
# 4. Ping诊断
<span id='id_4_1'/>
## 4.1 startIPPingDiagnostics
<span id='id_4_2'/>
## 4.2 getIPPingDiagnosticsResult

<span id='id_5'/>
# 5. Traceroute诊断
<span id='id_5_1'/>
## 5.1 startTraceRouteDiagnostics
<span id='id_5_2'/>
## 5.2 getTraceRouteDiagnosticsResult

<span id='id_6'/>
# 6. DDNS配置
<span id='id_6_1'/>
## 6.1 setDDNScfg

<span id='id_7'/>
# 7. IPSecVPN配置
<span id='id_7_1'/>
## 7.1 addIPSecVPNserver
<span id='id_7_2'/>
## 7.2 setIPSecVPNserver
<span id='id_7_3'/>
## 7.3 delIPSecVPNserver
<span id='id_7_4'/>
## 7.4 getIPSecVPNserver

<span id='id_8'/>
# 8. L2TP VPN配置
<span id='id_8_1'/>
## 8.1 setL2TPVPNMode
<span id='id_8_2'/>
## 8.2 setL2TPVPNServer
<span id='id_8_3'/>
## 8.3 getL2TPVPNserver
<span id='id_8_4'/>
## 8.4 setL2TPVPNClient


