# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import discord
import random
import asyncio
import re
class Bot(discord.Client):
	async def on_ready(self):
		self.chatbot = ChatBot(name='Stella 2.0', read_only=False, logic_adapters=['chatterbot.logic.BestMatch'])
		self.trainer = ChatterBotCorpusTrainer(self.chatbot)
		self.trainer.train('./corpus.json')

	async def on_message(self, message):
		# don't respond to ourselves
		if message.author == self.user:
			return
	
		inpt = str(message.content.encode('utf-8'))
		outpt = self.chatbot.get_response(re.sub('<@[-+]?[1-9]\d*>', '', inpt))
		print('> ' + inpt)
		print(outpt)

		# 25% chance of replying
		if random.randint(0, 100) < 10 or f'<@{self.user.id}>' in inpt:
			inpt.replace(f'<@{self.user.id}>', '')
			await asyncio.sleep(random.randint(3, 5))
			async with message.channel.typing():
				await asyncio.sleep(len(str(outpt)) * 0.10)
				await message.channel.send(f'<@{message.author.id}> ' + str(outpt))
		self.trainer.export_for_training('./corpus.json')
client = Bot()
client.run('NjE2MjM1MDM2MTIzMDcwNDc1.XWZnuQ.hhGDYqGTSkotu4XhOatjLn8V1hk', bot=False)
