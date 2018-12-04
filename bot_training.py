from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import pickle

bot = ChatBot('YouTubeChatBot')
bot.set_trainer(ListTrainer)

f = open('./InstagramComments_.p', 'rb')
comments = pickle.load(f)
f.close()

for convo in comments[:10000]:
	bot.train(convo)

while True:
	request = input("You: ")
	response = bot.get_response(request)
	print('Bot:', response)