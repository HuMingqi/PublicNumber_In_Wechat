from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from xml.etree import ElementTree as et
from django.utils.encoding import smart_str
import hashlib

@csrf_exempt
def test(request):
    return HttpResponse("test succeed!")

def index(request):
    if request.method=='GET':                                   #微信接入认证
        response=HttpResponse(checkSignature(request))
        return response
    else:
        xml_str = smart_str(request.body)
        request_xml = et.fromstring(xml_str)
        msgType = request_xml.find('MsgType').text
        
        if(msgType=='text'):                
            return HttpResponse(replyTextMsg(request_xml))   
        
             

def replyTextMsg(reqxml):
    server = reqxml.find('ToUserName').text
    user = reqxml.find('FromUserName').text
    CreateTime = reqxml.find('CreateTime').text
    #MsgType = reqxml.find('MsgType').text
    Content = reqxml.find('Content').text
    MsgId = reqxml.find('MsgId').text
    replyXml ="""<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    </xml>"""%(user,server,CreateTime,"鹦鹉学舌:"+Content+"\n by xiaoQ")              
    return replyXml
        
def checkSignature(request):
    signature=request.GET.get('signature',None)
    timestamp=request.GET.get('timestamp',None)
    nonce=request.GET.get('nonce',None)
    echostr=request.GET.get('echostr',None)    
    
    token='hmqi'
    tmplist=[token,timestamp,nonce]
    tmplist.sort()
    tmpstr="%s%s%s"%tuple(tmplist)                                                 
    tmpstr=hashlib.sha1(tmpstr.encode('utf-8')).hexdigest()                           #默认utf-8，先编码在hashing
    if tmpstr==signature:
        return echostr
    else:
        return 'Verify fail'