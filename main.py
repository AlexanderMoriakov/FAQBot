from random import randint
import re
from aiogram import executor,Bot,Dispatcher,types
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
import json
import difflib

from numpy import mat
from soupsieve import match
with open('questions.json',encoding='utf-8') as json_file:
    questions = json.load(json_file)
json_file.close()
QUESTIONS = questions
DICTIONARY = {}
MARKUP = types.InlineKeyboardMarkup()
with open('config.json',encoding='utf-8') as json_file:
    cfg = json.load(json_file)
json_file.close()


    

bot = Bot(cfg['token'])
dp = Dispatcher(bot=bot)

def write_down_unresponed_question(question,name):
    with open('unresponded.json',encoding='utf-8') as f:
        unresponded = json.load(f)
        unresponded[question]=name
    f.close()
 
    with open('unresponded.json','w',encoding='utf-8') as f:
        json.dump(unresponded, f, ensure_ascii=False, indent=4)
    f.close()

def get_answer(question):
    return f'{question} : {QUESTIONS[question]}'

async def find_best_match(question,id,n=0):
    
    matches = difflib.get_close_matches(question,QUESTIONS.keys() , n=3, cutoff=0.4)
    if(len(matches)<=n):
        await bot.send_message(chat_id=id,text="Нам не удалось найти ответ на ваш вопрос, он будет рассмотрен вручную и вам на него ответят")
        write_down_unresponed_question(question,id)
        return 
    keyboard = [
            [
                InlineKeyboardButton("Спасибо", callback_data=f"Да${question}${n}"),
                
            ],
            [InlineKeyboardButton("Мне не подходит такой ответ", callback_data=f"Нет${question}${n}")]
        ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await bot.send_message(chat_id=id,text=get_answer(matches[n]),reply_markup=markup)
    
    
@dp.message_handler()
async def echo(message : types.Message):
    print(message)
    await find_best_match(message.text,message.from_user.id)
    await bot.answer_callback_query('')

@dp.callback_query_handler(lambda callback_query: True)
async def some_callback_handler(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    if(callback_query.data.split('$')[0]=='Да'):
        await bot.send_message(chat_id=chat_id,text='Пожалуйста :3')
    elif(callback_query.data.split('$')[0]=='Нет'):
        await find_best_match(question=callback_query.data.split('$')[1],id=chat_id,n=int(callback_query.data.split('$')[2])+1)
    await bot.edit_message_reply_markup(chat_id=chat_id,message_id=callback_query.message.message_id,reply_markup=InlineKeyboardMarkup(inline_keyboard=[[],[]]))



def main():
    executor.start_polling(dp)

if __name__ == '__main__':
    main()
