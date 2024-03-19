from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import fickling

bot = ChatBot('YouTubeChatBot')
bot.set_trainer(ListTrainer)

f = open('./InstagramComments_.p', 'rb')
comments = fickling.load(f)
f.close()

for convo in comments[:10000]:
	bot.train(convo)

while True:
	request = input("You: ")
	response = bot.get_response(request)
	print('Bot:', response)
