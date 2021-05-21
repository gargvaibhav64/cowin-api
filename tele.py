
import time
# import schedule
import requests


def telegram_bot_sendtext(bot_message):
    
    bot_token = 'N/A'
    bot_chatID = 'N/A'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

# def 
# telegram_bot_sendtext("Hello! Test message!")