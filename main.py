import discord
from random import randint
import os

client = discord.Client()

github_link = ''
help_message_add = 'To use: \n\t#add {Character Name} {Weapon Speed and/or Initiative Modifier} - Add to the initiative\n\t#reset - Reset the initiative tracker\n\t#edit {Character Name} {Weapon Speed and/or Initiative Modifier} - Edit an existing characters roll'
help_message_git = 'Command and Explanations at: ' + github_link

current_initiative_list = []  # To hold all the players


# Default Initiative in ADD is a D10 +- Weapon Speed and/or Dex Modifier
def initiative_d10(user_modifier):
	return randint(1, 11) + user_modifier


def repeat():
	print(repeat)


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

	if user_message.content.startswith('#add'):
		# Fix a few of the edge cases that need to be handled.
		# Need to take in multi-word names
		# If last token is not a digit, default to 0, otherwise the last token will be the modifier.
		# Check extremely large and small edge cases
		# Double check for NULL inputs.
		tokens = user_message.content.split(' ')
		print(len(tokens))
		print(tokens)
		try:
			if len(tokens) == 1:
				raise Exception('You Fool! Are you not a person? Give your character a name!')
			elif len(tokens) > 3:
				raise Exception('You Fool! You gave too Many Arguments!')
			elif len(tokens) == 3:
				if not tokens[2].isdigit():
					raise TypeError('You Fool! You must put a modifier as an whole number!')
				initiative_roll = initiative_d10(int(tokens[2]))
			else:
				initiative_roll = initiative_d10(0)

			current_initiative_list.append(tokens[1])
			current_initiative_list.append(initiative_roll)

			await user_message.channel.send('{} rolled a {}'.format(tokens[1], initiative_roll))
		except:
			pass
		finally:
			print('Complete #add')

	if user_message.content.startswith('#edit'):  # Might move to a class function
		print('Editing')

	if user_message.content.startswith('#reset'):
		current_initiative_list.clear()
		print('Completed #reset')
		await user_message.channel.send('*Initiative Wiped*')

	if user_message.content.startswith('#order'):  # Works just finish formatting the output correctly
		try:
			if len(current_initiative_list) == 0:
				raise IndexError('You silly goose, there isn\'t anyone in the initiative right now')
			else:

				''' 
				Message format should be: 	Initiative order is:
											Counter:	Character_Name Roll
				'''
				initiative_order = 1
				await user_message.channel.send('Initiative order is: ')
				character_order = '```'
				for i in range(0, len(current_initiative_list), 2):
					character_order += ('{}:\t{}\t{}\n'.format(initiative_order, current_initiative_list[i], current_initiative_list[i+1]))
					initiative_order += 1
				character_order += '```'
				await user_message.channel.send(character_order)
		except IndexError as EmptyList:
			await user_message.channel.send(EmptyList)
			pass
		finally:
			print('Completed #order')

client.run(os.environ['TOKEN'])
