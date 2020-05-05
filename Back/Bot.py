import telebot
dUserState = dict()
dUserProblem = dict()
dUserNumber = dict()
token = '1207357105:AAHlQ1stw2VZd1bEvqQYLIx49nAHlOUaaRU'
bot = telebot.TeleBot(token)
x = 1
@bot.message_handler(content_types=["text"])

def ans(message):

    if message.from_user.id not in dUserState:
        dUserState[message.from_user.id] = 0

    if dUserState[message.from_user.id] == 0 and message.text != "помощь":
        bot.send_message(message.from_user.id, "напишите 'помощь' чтобы оставить заявку")

    if  message.text == "помощь":
        bot.send_message(message.from_user.id, "опишите вашу проблему")
        dUserState[message.from_user.id] = 1

    elif dUserState[message.from_user.id] == 1:
        dUserProblem[message.from_user.id] = message.text
        dUserState[message.from_user.id] = 2
        bot.send_message(message.from_user.id, "отправьте ваш контактный номер")
        
    elif dUserState[message.from_user.id] == 2:
        dUserNumber[message.from_user.id] = message.text
        dUserState[message.from_user.id] = 3
        bot.send_message(message.from_user.id, "отправьте локацию")

    elif dUserState[message.from_user.id] == 3:
         bot.send_message(message.from_user.id, "отправьте локацию")


            
@bot.message_handler(content_types=["location"])
def location(message):
    global x
    if message.location is not None and dUserState[message.from_user.id] == 3:
        #тут закидываем в firebase
        nowPhone = str(dUserNumber[message.from_user.id])
        nowProblem = str(dUserProblem[message.from_user.id])
        latitude = str(message.location.latitude)
        longitude = str(message.location.longitude)
        
        doc_ref = db.collection(u'Problems').document(str(x))
        doc_ref.set({
            u'latitude': latitude,
            u'longitude': longitude,
            u'phone': nowPhone,
            u'problem': nowProblem
        })
        
        x+=1
        
        print(nowPhone, nowProblem, latitude, longitude)
        bot.send_message(message.from_user.id, "мы добавили вашу заявку")
        dUserState[message.from_user.id] = 0

if __name__ == '__main__':
    bot.polling(none_stop=True)