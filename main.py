"""
Project: Initiative Tracker for Adventures Dark and Deep
Author: Justin Bull
Purpose: Discord bot that allows for ease of tracking initiative during combat in Adventures Dark and Deep
"""



import discord
from random import randint
import os
import re

client = discord.Client()

github_link = 'https://github.com/Bull-Justin/Initiative-Tracker'
help_message_add = 'To use: \n\t#add {Character Name} {Weapon Speed and/or Initiative Modifier} - Add to the initiative\n\t#reset - Reset the initiative tracker\n\t#order - Prints the current Initiative Order'
help_message_git = 'Command and Explanations at: ' + github_link

# To hold all the players
current_initiative_list = []


class DuplicateName(Exception):
	pass


class NoName(Exception):
	pass


class PlayerCharacter:
	def __init__(self):
		self.character_name = None
		self.initiative_roll = None
		self.attack_modifier = 0

	def __init__(self, character_name, attack_modifier):
		self.character_name = character_name
		self.attack_modifier = attack_modifier
		self.initiative_roll = initiative_d10(attack_modifier)

	def edit(self, new_mod):
		self.attack_modifier = new_mod

	def reroll(self):
		self.initiative_roll = initiative_d10(self.attack_modifier)
		self.__str__()

	def __str__(self):
		return '{} ({})'.format(self.character_name,self.initiative_roll)


# Default Initiative in ADD is a D10 +- Weapon Speed and/or Dex Modifier
def initiative_d10(modifier):
	return randint(1, 10) + modifier


@client.event
async def on_ready():
	print('I am {0.user}, a initiative tracker and die roller for Adventures Dark and Deep!'.format(client))


@client.event
async def on_message(user_message):
	if user_message.author == client.user:
		return

	if user_message.content.startswith('#help'):
		await user_message.channel.send(help_message_add)
		await user_message.channel.send(help_message_git)
		await user_message.edit(suppress=True) # Remove Embedded image pop-up

	if user_message.content.startswith('#add'):
		modifier = 0
		tokens = user_message.content.split(' ')
		print(len(tokens))
		index = len(current_initiative_list)
		try:
			if len(tokens) == 1: 																	# Only calling #add
				raise Exception('You Fool! Are you not a person? Give your character a name!')
			else:
				character_info = user_message.content[4:]  											# Remove the command from the string
				character_info = ' '.join(re.findall(r"[^()0-9-]+", character_info))  				# Get the name from the string
				character_info = character_info.rstrip()											# Remove any extra whitespace

				if any(x.character_name == character_info for x in current_initiative_list):		# Doesn't allow duplicate names
					raise DuplicateName('What are you, a Mimic? A character already has that name. Choose another!')

				if tokens[len(tokens) - 1].lstrip('-').isdigit() or tokens[len(tokens) - 1].lstrip('+').isdigit():
					modifier = int(tokens[len(tokens) - 1])											# Grabs number with +/- at the beginning

			PC = PlayerCharacter(character_info, modifier)
			current_initiative_list.append(PC)
			await user_message.channel.send('{} rolled a {}'.format(current_initiative_list[index].character_name, current_initiative_list[index].initiative_roll))
		except Exception as E:
			await user_message.channel.send(E)
			pass
#		finally:
#			print('Complete #add')

	if user_message.content.startswith('#reset'):
		current_initiative_list.clear()
#		print('Completed #reset')
		await user_message.channel.send('*Initiative Wiped*')

	# Works just finish formatting the output correctly
	if user_message.content.startswith('#order'):
		try:
			if len(current_initiative_list) == 0:
				raise IndexError('You silly goose, there isn\'t anyone in the initiative right now')
			else:

				''' 
				Message format should be: 	Initiative order is:
											Counter:	Character_Name Roll
				'''
				current_initiative_list.sort(key=lambda x: x.initiative_roll, reverse=False)		# Sort the order by initiative, Lower = Better

				initiative_order = 1
				await user_message.channel.send('Initiative order is: ')
				character_order = '```'																# Discord Formatting
				for i in range(len(current_initiative_list)):										# Format the output for Initiative Order
					character_order += ('{}:\t{}\n'.format(initiative_order, current_initiative_list[i]))  # Better looking using __str__
					initiative_order += 1
				character_order += '```'															# Discord Formatting
				await user_message.channel.send(character_order)
		except IndexError as EmptyList:
			await user_message.channel.send(EmptyList)
			pass
#		finally:
#			print('Completed #order')

	if user_message.content.startswith('#reroll'):
		if len(current_initiative_list) == 0:
			raise Exception('There is no one in the initiative right now, add with #add')
		else:
			for i in range(len(current_initiative_list)):
				current_initiative_list[i].reroll()
		await user_message.channel.send('The initiative was rerolled!')
client.run(os.environ['TOKEN'])
