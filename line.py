import os
import random
import re

from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

from bot.main import process_message
from bot.sessions import Session
from bot.constants import RESPONSES, Context


app = Flask(__name__)
session = Session()

line_bot_api = LineBotApi(os.environ.get('LINE_ACCESS_TOKEN', None))
handler = WebhookHandler(os.environ.get('LINE_SECRET', None))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('404.html'), 500


@app.route("/", methods=['GET'])
def hello():
    return render_template('hello.html'), 200


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    chat_id = event.source.user_id or event.source.group_id or event.source.room_id
    user_message = event.message.text

    data = {
        'chat_id': chat_id,
        'message': user_message
    }

    bot_response, delay, image = process_message(session, data)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=bot_response))

    while (delay):
        data['message'] = ''
        bot_response, delay, image = process_message(session, data)
        bot_response = re.sub(r'\<.*?\>', '', bot_response)
        line_bot_api.push_message(chat_id, TextSendMessage(text=bot_response))
        line_bot_api.push_message(
            chat_id,
            ImageSendMessage(original_content_url=image, preview_image_url=image)
        ) if image else None

        response = RESPONSES[Context.EXPIRED]

        line_bot_api.push_message(
            chat_id,
            TextSendMessage(text=response[random.randint(0, len(response) - 1)])
        ) if not delay else None


if __name__ == "__main__":
    app.run(
        host=os.environ.get('HOST', None),
        port=int(os.environ.get('PORT', None))
    )
