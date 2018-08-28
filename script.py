#Copyright (C) 2018 Girardeau Baptiste
#
#This program is free software; you can redistribute it and/or modify  
#it under the terms of the GNU General Public License as published by  
#the Free Software Foundation; either version 2 of the License, or  
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,  
#but WITHOUT ANY WARRANTY; without even the implied warranty of  
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the  
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along  
#with this program; if not, write to the Free Software Foundation, Inc.,  
#51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import asyncio, discord, re, time
import assets.commands as commands
import assets.logs as logs
import assets.temp as temp
from difflib import SequenceMatcher #Pour la ressemblance entre deux string

client = discord.Client()
token = str(open("token.txt", "r", encoding="utf-8").readline().replace('\n','')) #Token du Bot (stocké dans le fichier token.txt)
ver = "1.1.0"
changelog = """
- Ajout de la commande $changelog
- Ajout de la commande $invite
- Ajout de la commande $warn
- Ajout de la raison lors d'un mute
- Il est possible de renommer le salon #logs en #logs-geekbot.
- Le changelog est désormais posté dans le salon #logs à chaque mise à jour.
- Amélioration de l'aide et ajout du partenaire Kyoshi
- Modification du message lorsque le bot rejoint un serveur
"""

with open("insultes.txt", "r", encoding="utf-8") as insultes:
	string=insultes.read().replace('\n',' ')
list_insultes = []
for word in string.split(' '):
	list_insultes.append(word)

temp.init() #Création de la base de données temporaire

print("GeekBot " + ver )


@client.event
async def on_ready():
	print("Ready !")
	servers_num = str(len(client.servers))
	await client.change_presence(game=discord.Game(name="$help | " + servers_num + " serveurs"),status=discord.Status.online)

@client.event
async def on_server_join(server):
	if server.me.server_permissions.administrator:
		print("GeekBot vient de rejoindre le serveur " + server.name + " !")
		chan = await client.get_channel("452126872994578434")
		await client.send_message(chan, "GeekBot vient de rejoindre le serveur " + server.name + " ! :tada::tada:")
		role = await client.create_role(server, name="GeekBot Logs")
		everyone_perms = discord.PermissionOverwrite(read_messages=False)
		role_perms = discord.PermissionOverwrite(read_messages=True)
		logs_chan = await client.create_channel(server, "logs", (server.default_role, everyone_perms), (role, role_perms))
		embed = discord.Embed(title="Merci d'avoir ajouté GeekBot !", description= """
Dans ce channel seront postés les **logs relatifs à GeekBot**.
Il est pour le moment **accessible uniquement au rôle GeekBot Logs**, mais rien ne vous empêche de le modifier.
Si vous le souhaitez, vous pouvez renommer ce salon en #logs-geekbot.

**POUR AFFICHER L'AIDE, FAITES $HELP**
N'oubliez pas d'informer vos membres de l'existence de la commande `$report`.

**[Rejoindre le discord officiel de GeekBot](https://discord.gg/Dgdurw9)**
""", color=0x006400)
		embed.set_footer(text="Bot créé par baptiste0928")
		await client.send_message(logs_chan, embed=embed)
	else:
		embed = discord.Embed(title="Permissions manquantes !!", description="""
**Merci d'avoir ajoouté Geekbot à votre serveur !**
*Malheureusement, vous ne lui avez pas donné les permissions nécessaires à son bon fonctionnement ...*

GeekBot ne demande qu'une seule permission, celle d'administrateur.
Cela lui permet notamment d'acceder à tous les channels afin de les modérer immédiatement. De plus, si une nouvelle fonctionalité demande une nouvelle permission, vous n'aurez pas besoin de réinviter le bot.

Afin que tout fonctionne normalement, réinvitez GeekBet en lui donnant bien la permissions "Administrateur".
**[Réinviter GeekBot](https://discordapp.com/oauth2/authorize?client_id=438384691251511307&scope=bot&permissions=8)**
""", color=0xDB0F0F)
	embed.set_footer(text="Bot créé par baptiste0928")
	await client.send_message(server.owner, embed=embed)
	await client.leave_server(server)


@client.event
async def on_message(message):
	if message.author == client.user: #Empêcher le bot de se répondre à lui même.
		return
	if message.author.bot == True: #Empêcher le bot de répondre à des bots
		return

	#Commandes en mp
	if message.content.startswith('$help'): #Commande Aide
		await commands.help(message, client, ver)
		return

	if message.content.startswith('$invite'): #Commande Aide
		await commands.invite(message, client)
		return

	if message.content.startswith('$changelog'): #Commande Ping
		await commands.changelog(message, client, changelog, ver)
		return

	if message.content.startswith('$send-changelog'): #Commande Ping
		if message.author.id == '207852811596201985':
			await commands.sendchangelog(message, client, changelog, ver)
		return


	if message.channel.is_private: #Empêcher le bot de répondre aux messges privés.
		await client.send_message(message.channel, "Désolé, je ne peut pas vous répondre par message privé.")
		return

	#Commandes
	if message.content.startswith('$ping'): #Commande Ping
		await commands.ping(message, client)
		return

	if message.content.startswith('$clear'): #Commande Clear
		await commands.clear(message, client)
		return

	if message.content.startswith('$report'): #Commande report
		await commands.report(message, client)
		return

	if message.content.startswith('$warn'): #Commande Ping
		await commands.warn(message, client)
		return

	if message.content.startswith('$mute'): #Commande Ping
		await commands.mute(message, client)
		return

	if message.content.startswith('$unmute'): #Commande Ping
		await commands.unmute(message, client)
		return


	if message.author.server_permissions.manage_messages:
		return

	if temp.ismute(message.author.id, message.server.id):
		await client.delete_message(message)
		return

	#Anti-insultes
	msg = message.content.lower()
	message_clean = re.sub('[*_~!?\-$§\.]', '', msg)
	for i in list_insultes:
		if i.lower() in message_clean.split(): #Si le message contient un mot dans la liste des insultes
				await client.delete_message(message) #Supprimer le message
				temp.addwarn(message.author.id, message.server.id)
				alert_message = await client.send_message(message.channel,"<@" + str(int(message.author.id)) + ">" + " Surveillez votre language!")
				await logs.insult(message, client)

				if temp.getwarn(message.author.id, message.server.id) >= 3:
					temp.mute(message.author.id, message.server.id)
					await logs.auto_mute(message, client)
					temp.setwarn(message.author.id, message.server.id)
					await asyncio.sleep(1800.0)
					temp.unmute(message.author.id, message.server.id)

				await asyncio.sleep(3.0)
				await client.delete_message(alert_message)
				return

	if message.server.id == "464727714566242305":
		return
	
	#Anti-spam
	async for msg in client.logs_from(message.channel, limit=5):
		if msg.author == message.author and msg.id != message.id:
			if SequenceMatcher(None, msg.clean_content, message.clean_content).ratio() >= 0.9 or time.mktime(message.timestamp.timetuple())-1 < time.mktime(msg.timestamp.timetuple()):
				await client.delete_message(message)
				temp.addwarn(message.author.id, message.server.id)
				alert_message = await client.send_message(message.channel,"<@" + str(int(message.author.id)) + ">" + " Pas de spam (flood)!")
				await logs.spam(message, client)

				if temp.getwarn(message.author.id, message.server.id) >= 3:
					temp.mute(message.author.id, message.server.id)
					await logs.auto_mute(message, client)
					temp.setwarn(message.author.id, message.server.id)
					await asyncio.sleep(1800.0)
					temp.unmute(message.author.id, message.server.id)

				await asyncio.sleep(3.0)
				await client.delete_message(alert_message)
				return
			else:
				break

@client.event
async def on_message_edit(before, message):
	if message.author == client.user: #Empêcher le bot de se répondre à lui même.
		return
	if message.channel.is_private: #Empêcher le bot de répondre aux messges privés.
		await client.send_message(message.channel, "Désolé, je ne peut pas vous répondre par message privé.")
		return
	if message.author.server_permissions.manage_messages:
		return


	msg = message.content.lower()
	message_clean = re.sub('[*_~!?]', '', msg)
	for i in list_insultes:
		if i.lower() in message_clean.split(): #Si le message contient un mot dans la liste des insultes
			await client.delete_message(message) #Supprimer le message
			temp.addwarn(message.author.id, message.server.id)
			alert_message = await client.send_message(message.channel,"<@" + str(int(message.author.id)) + ">" + " Surveillez votre language!")
			await logs.insult(message, client)

			if temp.getwarn(message.author.id, message.server.id) >= 3:
				temp.mute(message.author.id, message.server.id)
				await logs.auto_mute(message, client)
				await asyncio.sleep(1800.0)
				temp.unmute(message.author.id, message.server.id)

			await asyncio.sleep(3.0)
			await client.delete_message(alert_message)
			return

@client.event
async def on_error(event):
	return

client.run(token)
