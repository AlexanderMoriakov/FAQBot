from tkinter.messagebox import QUESTION
from aiogram import executor,Bot,Dispatcher,types
import json
with open('questions.json',encoding='utf-8') as json_file:
    questions = json.load(json_file)
QUESTIONS = questions

with open('config.json',encoding='utf-8') as json_file:
    cfg = json.load(json_file)


    
class Question:
    def __init__(self) -> None:
        self.question = ''
        self.words = {}

bot = Bot(cfg['token'])
dp = Dispatcher(bot=bot)

def find_best_match(question, exclude):
    matches = {}
    for n in QUESTIONS.keys():
        score = 0
        words_probable_match = n.split(' ')
        words_question = question.split(' ')
        for i in words_question:
            if(i in words_probable_match):
                score += 1
        matches[n] = score
    best_match = ''
    for n in matches.keys():
        if((best_match == '') or (matches[n]>matches[best_match])):
            best_match = n
    return f'{best_match} : {QUESTIONS[best_match]}'            




@dp.message_handler()
async def echo(message : types.Message):
    await bot.send_message(chat_id=message.from_user.id,text=find_best_match(message.text.lower(),[])) 
    print(message)

def main():
    executor.start_polling(dp)

if __name__ == '__main__':
    main()
