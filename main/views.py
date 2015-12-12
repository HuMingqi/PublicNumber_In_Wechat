from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from xml.etree import ElementTree as et
from django.utils.encoding import smart_str
import hashlib
from urllib import request,parse
import time
import json

#global veriable
textMsg="""<xml>                                                        
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    </xml>"""
    
ptMsg='''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[news]]></MsgType>
<ArticleCount>1</ArticleCount>
<Articles>
<item>
<Title><![CDATA[%s]]></Title> 
<Description><![CDATA[%s]]></Description>
<PicUrl><![CDATA[%s]]></PicUrl>
<Url><![CDATA[%s]]></Url>
</item>
</Articles>
</xml>'''    

@csrf_exempt
def test(request):
    return HttpResponse("test succeed!")

@csrf_exempt                                                    #disabling the django security request for this view 不验证django token
def index(request):
    if request.method=='GET':                                   #微信接入认证
        response=HttpResponse(checkSignature(request))
        return response
    else:
        #print('post method')
        xml_str = smart_str(request.read())
        request_xml = et.fromstring(xml_str)
        #request_xml=et.iterparse(request)
        msgType = request_xml.find('MsgType').text  
        #print(msgType) 
        if(msgType=='event'):
            return HttpResponse(replyEvent(request_xml))
        elif(msgType=='text'):                
            return HttpResponse(replyTextMsg(request_xml))    
        else:
            return HttpResponse("暂时不支持的请求！")    
        
  
def replyEvent(reqxml): 
    #print('method replyEvent')    
    if(reqxml.find('Event').text=='subscribe'):
        me = reqxml.find('ToUserName').text
        user = reqxml.find('FromUserName').text
        content='''感谢订阅xiaoQ的微信公众号！这里有互联网资讯，兴趣分享，个人编码分享，有趣的内置应用...
                        回复数字0 查看菜单
        xiaoQ会不断努力完善这个公众号，谢谢大家支持 ~
        xiaoQ新浪微博：http://weibo.com/u/5143027608 
                       欢迎交流！
        written by 2015/11/02                       
        '''     
        replyXml=textMsg%(user,me,int(time.time()),content)
        return replyXml              
                     
def replyTextMsg(reqxml):
    #print('method replyText')
    me = reqxml.find('ToUserName').text
    user = reqxml.find('FromUserName').text    
    content = reqxml.find('Content').text
    
    if(content=='0'):
        menu='''菜单：
        1.互联网资讯
        2.编程之旅
        3.兴趣分享
        4.内置应用       
        5.联系xiaoQ 
        '''
        replyXml =textMsg%(user,me,int(time.time()),menu)      #(int)time.time() error        
    elif(content=='1'):
        title='云计算让WinTel体系不攻自破'
        desc='热词“云计算”，你真的了解吗？'
        picurl='https://mmbiz.qlogo.cn/mmbiz/lf9kTl84CDRNL7kaicl0XmxD98W8fME1GfmeHGe5ZJibKph3HDkBSBzjAicpzBgvYeX7y31tMEFn9Gf5jBjLejXWQ/0?wx_fmt=jpeg'
        pturl='http://mp.weixin.qq.com/s?__biz=MzAxNTcwOTUwNQ==&mid=210981950&idx=1&sn=a481f7fc0b5d542812720a9778675be1&scene=18#rd'
        replyXml=ptMsg%(user,me,int(time.time()),title,desc,picurl,pturl)
    elif(content=='2'):
        replyXml=textMsg%(user,me,int(time.time()),"暂时还没有内容")
    elif(content=='3'):
        replyXml=textMsg%(user,me,int(time.time()),"暂时还没有内容")
    elif(content=='4'):
        submenu='''内置应用子菜单：
        41.你发我译
        42.clothes助手 (编码中coding!)       
        '''     
        replyXml=textMsg%(user,me,int(time.time()),submenu)  
    elif(content=='5'):
        myself='''xiaoQ新浪微博：
        http://weibo.com/u/5143027608        
                        邮箱：
        xiaoq_focus_net@sina.com        
                        欢迎与各位交流!
        '''
        replyXml=textMsg%(user,me,int(time.time()),myself)        
    elif(content=='41'):
        replyXml=textMsg%(user,me,int(time.time()),'请发送你要翻译的单词或句子(中英不限）,以%开头,例如 :%hi,my friend! \n ps:由于网络延时回复可能较慢')
    elif(content=='42'):
        replyXml=textMsg%(user,me,int(time.time()),'请发送一张你喜欢的服饰图片，clothes助手将帮你匹配到最相似服饰并发送给你购买链接^_^')
    elif(content[0]=='%'):
        trans=youdaotrans(content[1:])           
        replyXml=textMsg%(user,me,int(time.time()),trans)
    else:
        menu='''菜单：
        1.互联网资讯
        2.编程之旅
        3.兴趣分享
        4.内置应用        
        5.联系xiaoQ
        '''
        replyXml =textMsg%(user,me,int(time.time()),menu) 
    return replyXml


def youdaotrans(qtext):
    #print('method ydtrans')
    qqtext=parse.quote(qtext,encoding='utf-8')                       #编码非ascii字符
    url='http://fanyi.youdao.com/openapi.do?keyfrom=xiaoQ-winxin&key=2108254436&type=data&doctype=json&version=1.1&q='+qqtext
    resp=request.urlopen(url,timeout=2)
    rs=json.loads(resp.read().decode())             #bytes -> str
    if('errorCode' not in rs):
        return '网络超时，请稍后再试！'
    if(rs['errorCode']==0):
            trans=''            
            if('basic' in rs):
                trans=rs['basic']['explains']
                trans='基础翻译：\n'+'\n'.join(trans)        
            trans=trans+'\n'+'网络翻译：\n'+'\n'.join(rs['translation'])
    elif(rs['errorCode'] == 20):
        trans='对不起，要翻译的文本过长'
    elif(rs['errorCode'] == 30):
        trans='对不起，无法进行有效的翻译'
    elif(rs['errorCode'] == 40):
        trans='对不起，不支持的语言类型'
    else:
        trans='对不起，您输入的文本  %s 暂时无法翻译,请稍后再试'%qtext           
    return trans
    
        
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