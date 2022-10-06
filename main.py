from asyncore import write
from random import randint
from aiogram import executor,Bot,Dispatcher,types
import json

from numpy import mat
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


def compare_match(question, match):
    similiarity = 0
    match_array = match.split(' ')
    for n in question.split(' '):
        if n in match_array:
            similiarity += 10
    if question == match:
        similiarity+=500
    return similiarity
def filter_questions(questions,exclude_array):
    l = questions
    for n in exclude_array:
        l = l.remove(n)
    return l


def find_best_match(question,exclude_array,message):
    filtered_QUESTIONS = filter_questions(QUESTIONS,exclude_array)
    best_match = ''
    best_match_score = 0
    for n in filtered_QUESTIONS.keys():
        comparision_score = compare_match(question,n)
        if(comparision_score > best_match_score):
            best_match = n
            best_match_score = comparision_score
    if(best_match == ''):
        write_down_unresponed_question(question,message.from_user.id)
        return 'К сожалению, нам не удалось ответить на ваш вопрос. Он будет отправлен напрямую нашему начальству и вам на него обязательно ответят.'
    return f'{best_match} : {filtered_QUESTIONS[best_match]}'
    

@dp.message_handler()
async def echo(message : types.Message):
    await bot.send_message(chat_id=message.from_user.id,text=find_best_match(message.text.lower(),[],message=message))

def main():
    compare_match('абобус', "сусус абобус")
    executor.start_polling(dp)

if __name__ == '__main__':
    main()
