from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    PostbackEvent,
    PostbackTemplateAction
)
from .scraper import IFoodie

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
 
@csrf_exempt
def callback(request):
    city=['台北市','新北市','桃園市','台中市','台南市','高雄市','基隆市','新竹市','嘉義市',
          '宜蘭縣','新竹縣','苗栗縣','彰化縣','南投縣','雲林縣','嘉義縣','屏東縣','花蓮縣','臺東縣','澎湖縣']

    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
 
                if event.message.text == "嗨":
 
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='Menu',
                                text='請選擇地區',
                                actions=[
                                    PostbackTemplateAction(
                                        label='台北市',
                                        text='台北市',
                                        data='A&台北市'
                                    ),
                                    PostbackTemplateAction(
                                        label='台中市',
                                        text='台中市',
                                        data='A&台中市'
                                    ),
                                    PostbackTemplateAction(
                                        label='高雄市',
                                        text='高雄市',
                                        data='A&高雄市'
                                    )
                                ]
                            )
                        )
                    )
            elif isinstance(event, PostbackEvent):  # 如果有回傳值事件
 
                if event.postback.data[0:1] == "A":  # 如果回傳值為「選擇地區」
 
                    area = event.postback.data[2:]  # 透過切割字串取得地區文字
 
                    line_bot_api.reply_message(   # 回復「選擇美食類別」按鈕樣板訊息
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='您有新訊息',
                            template=ButtonsTemplate(
                                title='Menu',
                                text='請選擇美食類別',
                                actions=[
                                    PostbackTemplateAction(  # 將第一步驟選擇的地區，包含在第二步驟的資料中
                                        label='火鍋',
                                        text='火鍋',
                                        data='B&' + area + '&火鍋'
                                    ),
                                    PostbackTemplateAction(
                                        label='早午餐',
                                        text='早午餐',
                                        data='B&' + area + '&早午餐'
                                    ),
                                    PostbackTemplateAction(
                                        label='約會餐廳',
                                        text='約會餐廳',
                                        data='B&' + area + '&約會餐廳'
                                        
                                    ),
                                    PostbackTemplateAction(
                                        label='新開幕',
                                        text='新開幕',
                                        data='B&' + area + '&新開幕'
                                        
                                    ),

                                    # PostbackTemplateAction(
                                    #     label='燒烤',
                                    #     text='燒烤',
                                    #     data='B&' + area + '&燒烤'
                                        
                                    # ),
                                    # PostbackTemplateAction(
                                    #     label='餐酒館',
                                    #     text='餐酒館',
                                    #     data='B&' + area + '&餐酒館'
                                        
                                    # ),                                                                                                        
                                    # PostbackTemplateAction(
                                    #     label='居酒屋',
                                    #     text='居酒屋',
                                    #     data='B&' + area + '&居酒屋'
                                        
                                    # )                                    
                                ]
                            )
                        )
                    )
 
                elif event.postback.data[0:1] == "B":  # 如果回傳值為「選擇美食類別」
 
                    result = event.postback.data[2:].split('&')  # 回傳值的字串切割
 
                    food = IFoodie(
                        result[0],  # 地區
                        result[1]  # 美食類別
                    )
 
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        # 爬取該地區正在營業，且符合所選擇的美食類別的前五大最高人氣餐廳
                        TextSendMessage(text=food.scrape())
                    )
 
        return HttpResponse()
    else:
        return HttpResponseBadRequest()