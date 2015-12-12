from urllib import request
from urllib import parse
import json

def testxml():
    print('method testxml')
              
    xmlData= '''<xml>
     <ToUserName><![CDATA[hmqi]]></ToUserName>
     <FromUserName><![CDATA[user]]></FromUserName> 
     <CreateTime>1348831860</CreateTime>
     <MsgType><![CDATA[text]]></MsgType>
     <Content><![CDATA[1]]></Content>
     <MsgId>1234567890123456</MsgId>
     </xml>'''                        
    url='http://localhost:8000/main/'
    #headers = {'User-Agent':'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)','Content-Type':'text/xml'}    
    req=request.Request(url,headers = {"User-Agent": "Mozilla/5.0 Firefox/35.0",'Content-Type':'text/xml'},data=xmlData.encode())          #str encoded to bytes         
    try:
        resp=request.urlopen(req)                           #500 , keyError(key is not found) when debugging
    except Exception as ex:
        print(ex)    
    print(resp.read())          #bytes
    
    
def youdaotrans(qtext):
    print('method ydtrans') 
    qtext=parse.quote(qtext,encoding='utf-8')   
    url='http://fanyi.youdao.com/openapi.do?keyfrom=xiaoQ-winxin&key=2108254436&type=data&doctype=json&version=1.1&q='+qtext
    resp=request.urlopen(url,timeout=1)
    #print(resp.read())
    tran=resp.read()                            #read 不可反复读取！！
    rs=json.loads(tran.decode())
    if(rs['errorCode']==0):
            trans=''            
            if('basic' in rs):
                trans=rs['basic']['explains']
                trans='基础翻译：'+'\n'.join(trans)        
            trans=trans+'\n'+'网络翻译：\n'+'\n'.join(rs['translation'])
            print(trans)
    
    