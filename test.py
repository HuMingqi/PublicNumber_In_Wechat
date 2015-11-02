from urllib import request
from urllib import parse

def testxml():
    print('method testxml')
              
    xmlData= '''<xml>
     <ToUserName><![CDATA[hmqi]]></ToUserName>
     <FromUserName><![CDATA[user]]></FromUserName> 
     <CreateTime>1348831860</CreateTime>
     <MsgType><![CDATA[text]]></MsgType>
     <Content><![CDATA[test]]></Content>
     <MsgId>1234567890123456</MsgId>
     </xml>'''                        
    url='http://localhost:8000/main/'
    #headers = {'User-Agent':'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)','Content-Type':'text/xml'}    
    req=request.Request(url,headers = {"User-Agent": "Mozilla/5.0 Firefox/35.0",'Content-Type':'text/xml'},data=xmlData.encode())          #str encoded to bytes         
    try:
        resp=request.urlopen(req)                           #500 , keyError(key is not found) when debugging
    except Exception as ex:
        print(ex)    
    print(resp.read()) 
    