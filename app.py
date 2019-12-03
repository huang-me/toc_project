# coding=utf-8
import os
import sys
import gspread

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage
from oauth2client.service_account import ServiceAccountCredentials

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", "helper", "food","drink","add","ncku","savefood","savedrink","savencku","repeat"],
    transitions=[
        {
            "trigger": "helper",
            "source": "user",
            "dest": "helper",
            "conditions": "is_going_to_helper",
        },
        {
            "trigger": "advance",
            "source": "helper",
            "dest": "food",
            "conditions": "is_going_to_food",
        },
        {
            "trigger": "advance",
            "source": "helper",
            "dest": "drink",
            "conditions": "is_going_to_drink",
        },
        {
            "trigger": "advance",
            "source": "helper",
            "dest": "add",
            "conditions": "is_going_to_add",
        },
        {
            "trigger": "advance",
            "source": "helper",
            "dest": "ncku",
            "conditions": "is_going_to_ncku",
        },
        {
            "trigger": "trig_save",
            "source": "add",
            "dest": "savefood",
            "conditions": "is_going_to_savefood",
        },
        {
            "trigger": "trig_save",
            "source": "add",
            "dest": "savedrink",
            "conditions": "is_going_to_savedrink",
        },
        {
            "trigger": "trig_save",
            "source": "add",
            "dest": "savencku",
            "conditions": "is_going_to_savencku",
        },
        {
            "trigger": "go",
            "source": "user",
            "dest": "repeat",
            "conditions": "is_going_to_repeat",
        },
        {"trigger": "back", "source": ["savefood","savencku","savedrink"], "dest": "user"},
        {"trigger": "go_back", "source": [ "food","drink","ncku","repeat"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)



@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")
    print('\n===\n')

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue

        if event.message.text == "小幫手" :
            machine.helper(event)
        else :
            if machine.state == "savefood" or machine.state == "savedrink" or machine.state == "savencku" :
                machine.back(event)
                continue
            if machine.state == "add" :
                send_text_message(event.reply_token,text = "你想推薦的店家叫什麼名字呢？")
                machine.trig_save(event)
                continue
            if machine.state == "helper" :
                machine.advance(event)
                continue
            else :
                machine.go(event)
        print(machine.state)


    # if not machine.state == "user" :
    #     machine.go_back()
    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)