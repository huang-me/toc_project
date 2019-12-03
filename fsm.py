from transitions.extensions import GraphMachine
from utils import send_text_message
from linebot import LineBotApi, WebhookParser
from linebot.models import *
from oauth2client.service_account import ServiceAccountCredentials
import random
import os
import gspread

def auth_gss_client(path, scopes):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scopes)
    return gspread.authorize(credentials)

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

# all of is_going_to 

    def is_going_to_helper(self, event):
        return True

    def is_going_to_ncku(self, event):
        text = event.message.text
        return text.lower() == "成大"

    def is_going_to_drink(self, event):
        text = event.message.text
        return text.lower() == "飲料"

    def is_going_to_add(self, event):
        text = event.message.text
        return text.lower() == "新增"

    def is_going_to_food(self, event):
        text = event.message.text
        return text.lower() == "午餐/晚餐"

    def is_going_to_savefood(self, event):
        text = event.message.text
        return text.lower() == "正餐"

    def is_going_to_savedrink(self, event):
        text = event.message.text
        return text.lower() == "飲料"

    def is_going_to_savencku(self, event):
        text = event.message.text
        return text.lower() == "成大"

    def is_going_to_repeat(self, event):
        return True

# in all states
    #helper
    def on_enter_helper(self, event):
        channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
        line_bot_api = LineBotApi(channel_access_token)
        buttons_template = ButtonsTemplate(
            title='想吃什麼呢？', text='以下選擇', actions=[
                PostbackAction(label='午餐/晚餐', data='food',text = '午餐/晚餐'),
                PostbackAction(label='飲料', data='drink',text = '飲料'),
                PostbackAction(label='推薦店家給\"吃吃\"', data='add',text = '新增'),
                PostbackAction(label='成大', data='ncku',text = '成大')
            ])
        template_message = TemplateSendMessage(
            alt_text='請用手機看此訊息！', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
        print("I'm entering helper")

    def on_exit_helper(self,event):
        print("leaving helper")

    # food 
    def on_enter_food(self, event):
        print("I'm entering food")
        auth_json_path = 'TocProject.json'
        gss_scopes = ['https://spreadsheets.google.com/feeds']
        gss_client = auth_gss_client(auth_json_path, gss_scopes) 
        spreadsheet_key_path = '1cCzx4bFzaG_PODChyKfWqrc11EN3D6RdvGrdNk2VrrI'
        sheet = gss_client.open_by_key(spreadsheet_key_path).sheet1
        index = sheet.get_all_values()
        rand = random.randint(0,len(index)-1)
        # print('===\n',index[rand],'\n===')
        msg = str(index[rand])
        msg = msg.split('\'',1)[1]
        msg = msg.split('\'',1)[0]
        send_text_message(event.reply_token,text = msg)
        self.go_back()

    def on_exit_food(self):
        print("Leaving food")

    # ncku
    def on_enter_ncku(self, event):
        auth_json_path = 'TocProject.json'
        gss_scopes = ['https://spreadsheets.google.com/feeds']
        gss_client = auth_gss_client(auth_json_path, gss_scopes) 
        spreadsheet_key_path = '1klbJDqlRv6F75UsVZT563O0fAIDylnHSErKo4vH_3bc'
        sheet = gss_client.open_by_key(spreadsheet_key_path).sheet1
        index = sheet.get_all_values()
        rand = random.randint(0,len(index)-1)
        # print('===\n',index[rand],'\n===')
        msg = str(index[rand])
        msg = msg.split('\'',1)[1]
        msg = msg.split('\'',1)[0]
        send_text_message(event.reply_token,text = msg)
        print("I'm entering ncku")
        self.go_back()

    def on_exit_ncku(self):
        print("Leaving ncku")

    # drink
    def on_enter_drink(self, event):
        auth_json_path = 'TocProject.json'
        gss_scopes = ['https://spreadsheets.google.com/feeds']
        gss_client = auth_gss_client(auth_json_path, gss_scopes) 
        spreadsheet_key_path = '1zSD4ggZbj6IHusOWiU6IyVnHR6vzuxVLMVulYh2iyiQ'
        sheet = gss_client.open_by_key(spreadsheet_key_path).sheet1
        index = sheet.get_all_values()
        rand = random.randint(0,len(index)-1)
        # print('===\n',index[rand],'\n===')
        msg = str(index[rand])
        msg = msg.split('\'',1)[1]
        msg = msg.split('\'',1)[0]
        send_text_message(event.reply_token,text = msg)
        print("I'm entering drink")
        self.go_back()

    def on_exit_drink(self):
        print("Leaving drink")

    # add
    def on_enter_add(self, event):
        channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
        line_bot_api = LineBotApi(channel_access_token)
        buttons_template = ButtonsTemplate(
            title='想加入店家到什麼分類呢？', text='以下選擇', actions=[
                PostbackAction(label='正餐', data='food',text = '正餐'),
                PostbackAction(label='飲料', data='drink',text = '飲料'),
                PostbackAction(label='成大', data='ncku',text = '成大')
            ])
        template_message = TemplateSendMessage(
            alt_text='請用手機看此訊息！', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
        print("I'm entering add")
        
    def on_exit_add(self,event):
        print("Leaving add")

    # savefood
    def on_enter_savefood(self,event):
        print("I'm entering savefood")

    def on_exit_savefood(self,event):
        print("I'm entering food")
        auth_json_path = 'TocProject.json'
        gss_scopes = ['https://spreadsheets.google.com/feeds']
        gss_client = auth_gss_client(auth_json_path, gss_scopes) 
        spreadsheet_key_path = '1cCzx4bFzaG_PODChyKfWqrc11EN3D6RdvGrdNk2VrrI'
        sheet = gss_client.open_by_key(spreadsheet_key_path).sheet1
        sheet.insert_row([event.message.text],1)
        send_text_message(event.reply_token,text = f"將{event.message.text}加入\"午餐/晚餐\"成功！")
        print("leaving savefood")

    # savedrink
    def on_enter_savedrink(self,event):
        print("I'm entering savedrink")

    def on_exit_savedrink(self,event):
        auth_json_path = 'TocProject.json'
        gss_scopes = ['https://spreadsheets.google.com/feeds']
        gss_client = auth_gss_client(auth_json_path, gss_scopes) 
        spreadsheet_key_path = '1zSD4ggZbj6IHusOWiU6IyVnHR6vzuxVLMVulYh2iyiQ'
        sheet = gss_client.open_by_key(spreadsheet_key_path).sheet1
        sheet.insert_row([event.message.text],1)
        send_text_message(event.reply_token,text = f"將{event.message.text}加入\"飲料\"成功！")
        print("leaving savedrink")

    # savencku 
    def on_enter_savencku(self,event):
        print("I'm entering savencku")

    def on_exit_savencku(self,event):
        auth_json_path = 'TocProject.json'
        gss_scopes = ['https://spreadsheets.google.com/feeds']
        gss_client = auth_gss_client(auth_json_path, gss_scopes) 
        spreadsheet_key_path = '1klbJDqlRv6F75UsVZT563O0fAIDylnHSErKo4vH_3bc'
        sheet = gss_client.open_by_key(spreadsheet_key_path).sheet1
        sheet.insert_row([event.message.text],1)
        send_text_message(event.reply_token,text = f"將{event.message.text}加入\"成大\"成功！")
        print("leaving savencku")

    # repeat
    def on_enter_repeat(self,event):
        send_text_message(event.reply_token,text = event.message.text)
        self.go_back()

    def on_exit_repeat(self):
        print("leaving repeat")