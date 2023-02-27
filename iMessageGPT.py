from chatgpt_wrapper import ChatGPT
from imessage_tools import read_messages, print_messages, send_message
import time
bot = ChatGPT()

def user_inputs():
    #ask the user for what phone number they want to send/read messages from
    phone_number = input("What phone number would you like to send/read messages from? (format: +12223334444): ")
    #ask the user for the path of their iMessage database
    chat_db = input("What is the path to your iMessage database? (/Users/userName/Messages/chatDB): ")
    #ask the user for the name of the person they are texting
    person = input("What is the name of the person you are texting? (format: FIRSTNAME): ")

    #default values for testing, uncomment the below 3 lines and comment out the above 3 lines to use the default values``
    
    chat_db = "/Users/kellygold/Library/Messages/chat.db"
    phone_number = "+13034768549"
    person = "Jeff"
    
    return [phone_number, chat_db, person]
dynamicData = user_inputs()
def check_last_sender(messages):
    last_sender = messages[0]['sender']
    print ("The last sender was: " + last_sender)
    return last_sender

while True:
    def get_recent_messages(phone_number, chat_db, person):
        # Phone number or label for "you"
        self_number = "Me"
        # Number of messages to return
        n = 15
        # Read the messages
        messages = read_messages(chat_db, n=n, self_number=self_number, human_readable_date=True)
        # Filter messages where phone_number is phone_number
        messages = [message for message in messages if message['phone_number'] == phone_number]

        #if is_from_me is true, then set messages.sender to "ME: " and if is_from_me is false, then set messages.sender to "THEM: "
        for message in messages:
            if message['is_from_me'] == True:
                message['sender'] = " KELLY: "
            else:
                message['sender'] = person + ": "
        return messages

    def build_prompt(messages, person):
        prompt = ""
        promptPrefix = "Write a reply for me to the following text message message conversation. The reply must be less than 280 characters so be very concise. Do not use quotations in your resposne. Do not use a greeting. The conversation is between me (KELLY) and a friend (" + person + "). Do not use words KELLY or "+person+". Messages from KELLY begin 'KELLY: ' and messages from "+person+" begin with '"+person+"': .The oldest messages are last. The most recent messages are first. The tone in the reply should be friendly, supportive, and encouraging. The style should be casual and informal. You may ask 1 or 2 follow up quetsions if needed. The message should continue from the most recent messages and be imformal. The most recent messages contain relevant topics. Choose relevant topics. Write a reply to the following conversation....."
        promptSuffix = ""
        for message in messages:
            promptSuffix += message['sender'] + message['body']
        prompt = promptPrefix + promptSuffix
        #print(prompt)
        return prompt

    def ask_chatGPT(prompt):
        response = bot.ask(prompt)
        print(response)
        return response

    def sender(phone_number, response):
        send_message(response, phone_number, False)

    #loop logic
    recent_messages_for_number = get_recent_messages(dynamicData[0], dynamicData[1], dynamicData[2])
    if check_last_sender(recent_messages_for_number[1:]) == " KELLY: ":
        print("I am the last sender, so I will not respond to myself.")
        time.sleep(25)
        continue
    else:
        chatGPT_Prompt = build_prompt(recent_messages_for_number, dynamicData[2])
        chatGPT_response = ask_chatGPT(chatGPT_Prompt)
        sender(dynamicData[0], chatGPT_response)
        time.sleep(25)
