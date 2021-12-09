#載入LineBot所需要的模組
from flask import Flask, request, abort
 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)
 
# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('mA6l5z4uRrlABWY4yuLxpp9xYApQIhNr3hp3xqdQ+GFHW+0Sd6WF1VQzc5PITgpuUbS4HyW+kN8NP0yOMkDGHgzBWplfBcFH2VhRlkbChQSoNlD1rTL1DzD5PdxuF3wpJ7r8qXT5qEzyuvWjblPWIgdB04t89/1O/w1cDnyilFU=')
 
# 必須放上自己的Channel Secret
handler = WebhookHandler('f7d4a81d9a0421c462d51c9c4899af7a')

#line_bot_api.push_message('U367eab69b0c66a0f5f40b659fb3b47a1', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
 
  
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
 
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
 
    return 'OK'

#判斷輸入是否為數字
# By : https://www.itread01.com/content/1549772101.html
def is_number(str):
    try:
        # 因為使用float有一個例外是'NaN'
        if str=='NaN':
            return False
        float(str)
        return True
    except ValueError:
        return False

#股價List
startValue = 1000
valueList = []

while startValue < 100000:
    #valueArray.append(round(startValue/100,2))
    valueList.append(startValue/100)
    if startValue < 5000:
        startValue += 5
    elif startValue < 10000:
        startValue += 10
    elif startValue < 50000:
        startValue += 50
    else:
        startValue += 100

def parsingStr(pStr):
    splitStrArray = pStr.split(' ')
    
    if len(splitStrArray) == 1:
        if is_number(pStr):
            return '計算價格為:'+pStr+'\n往上1.5%為'+str(round(float(pStr)*1.015,2))+'\n往下1.5%為'+str(round(float(pStr)*0.985,2))+'\n'
        elif pStr == 'Help' or pStr == 'help' or pStr == '幫助':
            outStr = ''
            outStr += '指令清單:\n'
            outStr += 'A) 空/多 價格 (折扣)\n'
            outStr += '簡易計算進出場的賺賠\n折扣為選填，格式為0.25，預設2.5折\n'
            outStr += 'ex: 多 120.5 / 空 115 / 空 50.5 0.28\n'
            outStr += 'B) 價格\n'
            outStr += '簡易計算上下1.5%大概為多少'
            outStr += 'ex: 90 / 215.5\n'
            outStr += 'C) count/Count/結算 總成交金額 應收付金額 (折扣)\n'
            outStr += '幫助月退的計算損益\n折扣為選填，格式為2.5，預設2.5折\n'
            outStr += 'ex: Count 123000 365 0.25 / 結算 323000 -1255\n'
            return outStr
        else:
            return 'Error'
            
    elif len(splitStrArray) == 2:
        if splitStrArray[0] == '空' or splitStrArray[0] == '多':
            if is_number(splitStrArray[1]):
                exists = float(splitStrArray[1]) in valueList
                targetValue = float(splitStrArray[1])
                if exists:
                    targetIndex = valueList.index( targetValue )
                    outStr = ''
                    if splitStrArray[0] == '空':
                        for k in range(targetIndex-5,targetIndex+5):
                            fee = (targetValue + valueList[k]) * 1.425 * 0.25
                            fee = round(fee,2)
                            tax = targetValue * 1.5
                            tax = round(tax,2)
                            endPrice = (targetValue - valueList[k]) * 1000 - fee - tax
                            endPrice = round(endPrice)
                            outStr += repr(valueList[k]) + "  " + repr(endPrice) + "\n"
                        return outStr
                    else:
                        for k in range(targetIndex-5,targetIndex+5):
                            fee = (targetValue + valueList[k]) * 1.425 * 0.25
                            fee = round(fee,2)
                            tax = valueList[k] * 1.5
                            tax = round(tax,2)
                            endPrice = (valueList[k] - targetValue) * 1000 - fee - tax
                            endPrice = round(endPrice)
                            outStr += repr(valueList[k]) + "  " + repr(endPrice) + "\n"
                        return outStr
                else:
                    return 'Error'
            else:
                return 'Error'
        else:
            return 'Error'
    elif len(splitStrArray) == 3:
        if splitStrArray[0] == 'count' or splitStrArray[0] == 'Count' or splitStrArray[0] == '結算':
            if is_number(splitStrArray[1]) and is_number(splitStrArray[2]):
                outStr = ''
                outStr += '總成交金額 : '+splitStrArray[1]+'\n'
                outStr += '應收付金額 : '+splitStrArray[2]+'\n'
                outStr += '折數 : 2.5 折\n'
                saveValue = round(float(splitStrArray[1]) * 0.001425 * 0.75,2)
                outStr += '折讓金額約為 : '+str(saveValue)+'\n'
                finalValue = float(splitStrArray[2]) + saveValue
                outStr += '結算金額約為 : '+str(finalValue)+'\n'
                return outStr
            else:
                return 'Error'
        elif is_number(splitStrArray[2]):
            per = float(splitStrArray[2])
            if splitStrArray[0] == '空' or splitStrArray[0] == '多':
                if is_number(splitStrArray[1]):
                    exists = float(splitStrArray[1]) in valueList
                    targetValue = float(splitStrArray[1])
                    if exists:
                        targetIndex = valueList.index( targetValue )
                        outStr = ''
                        if splitStrArray[0] == '空':
                            for k in range(targetIndex-5,targetIndex+5):
                                fee = (targetValue + valueList[k]) * 1.425 * per
                                fee = round(fee,2)
                                tax = targetValue * 1.5
                                tax = round(tax,2)
                                endPrice = (targetValue - valueList[k]) * 1000 - fee - tax
                                endPrice = round(endPrice)
                                outStr += repr(valueList[k]) + "  " + repr(endPrice) + "\n"
                            return outStr
                        else:
                            for k in range(targetIndex-5,targetIndex+5):
                                fee = (targetValue + valueList[k]) * 1.425 * per
                                fee = round(fee,2)
                                tax = valueList[k] * 1.5
                                tax = round(tax,2)
                                endPrice = (valueList[k] - targetValue) * 1000 - fee - tax
                                endPrice = round(endPrice)
                                outStr += repr(valueList[k]) + "  " + repr(endPrice) + "\n"
                            return outStr
                    else:
                        return 'Error'
                else:
                    return 'Error'
            else:
                return 'Error'
        else:
            return 'Error'
    elif len(splitStrArray) == 4:
        if splitStrArray[0] == 'count' or splitStrArray[0] == 'Count' or splitStrArray[0] == '結算':
            if is_number(splitStrArray[1]) and is_number(splitStrArray[2]) and is_number(splitStrArray[3]):
                outStr = ''
                outStr += '總成交金額 : '+splitStrArray[1]+'\n'
                outStr += '應收付金額 : '+splitStrArray[2]+'\n'
                outStr += '折數 : '+splitStrArray[3]+' 折\n'
                saveValue = round(float(splitStrArray[1]) * 0.001425 * (1 - float(splitStrArray[3])/10),2)
                outStr += '折讓金額約為 : '+str(saveValue)+'\n'
                finalValue = float(splitStrArray[2]) + saveValue
                outStr += '結算金額約為 : '+str(finalValue)+'\n'
                return outStr
            else:
                return 'Error'
        else:
            return 'Error'
    else:
        return 'Error'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
import re
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if parsingStr(message) != 'Error':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(parsingStr(message)))
    #if is_number(message):
    #    inputNum = float(message)
    #    msg = '計算金額為 : ' + str(inputNum) + '\n往上1.5%為 : ' + str(round(inputNum*1.015,2)) + '\n往下1.5%為 : ' + str(round(inputNum*0.985,2)) 
    #    line_bot_api.reply_message(event.reply_token,TextSendMessage(msg))
    #else:
    #    line_bot_api.reply_message(event.reply_token,TextSendMessage('哩公蝦'))

    #if re.match("你是誰",message):
    #    line_bot_api.reply_message(event.reply_token,TextSendMessage("才不告訴你勒~~"))
    #else:
    #    line_bot_api.reply_message(event.reply_token,TextSendMessage(message*1.015))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

