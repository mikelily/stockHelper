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

line_bot_api.push_message('U367eab69b0c66a0f5f40b659fb3b47a1', TextSendMessage(text='你可以開始了'))

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

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
import re
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if is_number(message):
        inputNum = float(message)
        msg = '計算金額為 : ' + str(inputNum) + '\n往上1.5%為 : ' + str(round(inputNum*1.015,2)) + '\n往下1.5%為 : ' + str(round(inputNum*0.985,2)) 
        line_bot_api.reply_message(event.reply_token,TextSendMessage(msg))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage('哩公蝦'))
    #if re.match("你是誰",message):
    #    line_bot_api.reply_message(event.reply_token,TextSendMessage("才不告訴你勒~~"))
    #else:
    #    line_bot_api.reply_message(event.reply_token,TextSendMessage(message*1.015))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

