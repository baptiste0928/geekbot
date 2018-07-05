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

import discord
import asyncio
import assets.logs as logs
import assets.temp as temp

async def ping(message, client):
    await client.send_message(message.channel, "Pong ! :ping_pong:")



async def clear(message, client):
    params = message.content.lower().split()
    perm = message.author.server_permissions.manage_messages
    try :
        clear = int(params[1]) + 1
    except (IndexError, ValueError):
        await client.delete_message(message)
        error_message = await client.send_message(message.channel, ":warning: Vous n'avez pas donné le nombre de messages à supprimer!")
        await asyncio.sleep(2)
        await client.delete_message(error_message)
    else:
        if perm == True:
            await client.purge_from(message.channel, limit = clear)
        else :
            await client.delete_message(message)
            error_message = await client.send_message(message.channel, ":x: Vous n'avez pas la permission d'effectuer cette commande.")
            await asyncio.sleep(2)
            await client.delete_message(error_message)



async def report(message, client):
    if not message.raw_mentions: #Si aucun utilisateur n'est mentionné
        await client.delete_message(message)
        error_message = await client.send_message(message.channel, ":warning: Veuillez donner un utilisateur à signaler (sous forme de mention).")
        await asyncio.sleep(2)
        await client.delete_message(error_message)
    else:
        params = message.content.split()
        await client.delete_message(message)
        report_user = await client.get_user_info(message.raw_mentions[0]) #Récuperer l'utilisateur report
        reason = " ".join(params[2:]) #Récupérer la raison
        if not reason: #Si aucune raison n'est spécifiée
            reason = "Aucune raison."
        last_message = None  #Récupérer le dernier message de l'utilisateur report
        async for msg in client.logs_from(message.channel, limit=20):
            if msg.author == report_user:
                last_message = msg.clean_content
                break
        if not last_message:
            last_message = "Aucun message trouvé."
        info_message = await client.send_message(message.channel, "<@" + str(message.author.id) + ">" + " Utilisateur signalé avec succès!")
        await logs.report(message, report_user, reason, last_message, client)
        await asyncio.sleep(2.0)
        await client.delete_message(info_message)

async def warn(message, client):
    perm = message.author.server_permissions.manage_messages
    if perm == True:
        if not message.raw_mentions: #Si aucun utilisateur n'est mentionné
            await client.delete_message(message)
            error_message = await client.send_message(message.channel, ":warning: Veuillez donner un utilisateur à avertir !")
            await asyncio.sleep(2)
            await client.delete_message(error_message)
        else:
            params = message.content.split()
            await client.delete_message(message)
            warned_user = await client.get_user_info(message.raw_mentions[0]) #Récuperer l'utilisateur report
            reason = " ".join(params[2:]) #Récupérer la raison
            if not reason: #Si aucune raison n'est spécifiée
                reason = "Aucune raison."
            info_message = await client.send_message(message.channel, "<@" + str(message.author.id) + ">" + " Utilisateur avertit avec succès!")
            await logs.warn(message, warned_user, reason, client)
            embed=discord.Embed(title="Avertissement (" + message.server.name + ")", description="""
Vous venez de recevoir un avertissement pour la raison suivante:
**""" + reason + """**
""", color=0xff0000)
            await client.send_message(warned_user, embed=embed)
            await asyncio.sleep(2.0)
            await client.delete_message(info_message)
    else:
        await client.delete_message(message)
        error_message = await client.send_message(message.channel, ":x: Vous n'avez pas la permission d'effectuer cette commande.")
        await asyncio.sleep(2)
        await client.delete_message(error_message)

async def mute(message, client):
    params = message.content.split()
    perm = message.author.server_permissions.manage_messages
    if not message.raw_mentions: #Si aucun utilisateur n'est mentionné
        await client.delete_message(message)
        error_message = await client.send_message(message.channel, ":warning: Veuillez donner un utilisateur à mute (sous forme de mention).")
        await asyncio.sleep(2)
        await client.delete_message(error_message)
    else:
        if perm == True:
            muted_user = await client.get_user_info(message.raw_mentions[0]) #Récuperer l'utilisateur mute
            temp.mute(muted_user.id, message.server.id)
            try:
                time = int(params[2])*60
            except:
                await client.delete_message(message)
                error_message = await client.send_message(message.channel, ":warning: Veuillez spécifier la durée du mute (en minutes).")
                await asyncio.sleep(2)
                await client.delete_message(error_message)
            else:
                reason = " ".join(params[3:]) #Récupérer la raison
                if not reason: #Si aucune raison n'est spécifiée
                    reason = "Aucune raison."
                await client.delete_message(message)
                info_message = await client.send_message(message.channel, muted_user.mention + " à été mute !" )
                await client.send_message(muted_user, ":warning: Vous avez été mute pendant **" + str(int(time/60)) + "min** sur **" + message.server.name + "** ! " )
                await logs.mute(message, client, time, muted_user, reason)
                await asyncio.sleep(2.0)
                await client.delete_message(info_message)
                await asyncio.sleep(time)
                temp.unmute(muted_user.id, message.server.id)
        else:
            await client.delete_message(message)
            error_message = await client.send_message(message.channel, ":x: Vous n'avez pas la permission d'effectuer cette commande.")
            await asyncio.sleep(2)
            await client.delete_message(error_message)


async def unmute(message, client):
    perm = message.author.server_permissions.manage_messages
    if not message.raw_mentions: #Si aucun utilisateur n'est mentionné
        await client.delete_message(message)
        error_message = await client.send_message(message.channel, ":warning: Veuillez donner un utilisateur à mute (sous forme de mention).")
        await asyncio.sleep(2)
        await client.delete_message(error_message)
    else:
        if perm == True:
            muted_user = await client.get_user_info(message.raw_mentions[0]) #Récuperer l'utilisateur mute
            temp.unmute(muted_user.id, message.server.id)
            await client.delete_message(message)
            info_message = await client.send_message(message.channel, muted_user.mention + " à été unmute !" )
            await asyncio.sleep(2.0)
            await client.delete_message(info_message)
        else:
            await client.delete_message(message)
            error_message = await client.send_message(message.channel, ":x: Vous n'avez pas la permission d'effectuer cette commande.")
            await asyncio.sleep(2)
            await client.delete_message(error_message)


async def changelog(message, client, changelog, ver):
    embed = discord.Embed(title="Changelog", description= """
**Version """ + ver + """**
```Markdown
""" + changelog + """
```
""", color=0x006400)
    embed.set_footer(text="Le changelog complet est dans le salon #changelog du discord du bot.")
    if message.channel.is_private: #Empêcher le bot de répondre aux messges privés.
        await client.send_message(message.author, embed=embed)
    else:
        await client.delete_message(message)
        info_message = await client.send_message(message.channel, message.author.mention + " Le changelog vous à été envoyé en message privé." )
        await client.send_message(message.author, embed=embed)
        await asyncio.sleep(2.0)
        await client.delete_message(info_message)


async def sendchangelog(message, client, changelog, ver):
    servers = client.servers
    embed = discord.Embed(title="Changelog", description= """
    **Version """ + ver + """**
    ```Markdown
    """ + changelog + """
    ```
    """, color=0x006400)
    embed.set_footer(text="Vous avez une suggestion pour la prochaine mise à jour ? Rejoignez le discord officiel en faisant $invite !")
    for i in servers:
        logs_chan = discord.utils.get(client.get_all_channels(), server__name = str(i), name = "logs")
        if logs_chan == None:
            logs_chan = discord.utils.get(client.get_all_channels(), server__name = str(i), name = "logs-geekbot")
            if logs_chan == None:
                logs_chan = await client.create_channel(i, "logs")
        await client.send_message(logs_chan, embed=embed)


async def help(message, client, ver):
    servers_num = str(len(client.servers))
    embed = discord.Embed(title="Aide", description= """
**Commandes**
`$report [@utilisateur] [raison]`: Permet de signaler un utilisateur.
`$warn [@utilisateur] [raison]`: Permet d'avertir un utilisateur.
`$mute [@utilisateur à mute] [durée en min] [raison]`: Permet de mute (rendre muet) un utilisateur.
`$unmute [@utilisateur]`: Permet d'unmute (permettre de parler) un utilisateur.

`$clear [nombre de messages à supprimer]`: Permet de supprimer un grand nombre de messages rapidement.

`$changelog`: Affiche les modification apportées lors de la dernière mise à jour.
`$invite`: Affiche les liens relatif à GeekBot (site et discord).


**Liens**
[Serveur Discord](https://discord.gg/Dgdurw9) | [Inviter GeekBot sur votre serveur](https://baptiste0928.net/geekbot/)
""", color=0x006400)
    embed.set_footer(text="Bot par baptiste0928 | Version " + ver + " - " + servers_num + " serveurs")
    embed2 =  discord.Embed(title="Kyoshi (Partenaire)", description= """
Un bot Discord qui à pour but d'être fun à utiliser et sans prise de tête !
Kyoshi est mis à jour le plus régulièrement possible afin de vous offrir les meilleures performances et la meilleure qualité possible !
[Inviter Kyoshi](https://discordapp.com/oauth2/authorize?client_id=402203386596032512&scope=bot&permissions=2146958591) | [Serveur discord de Kyoshi](https://discordapp.com/oauth2/authorize?client_id=402203386596032512&scope=bot&permissions=2146958591)
""", color=0xFFC300)
    embed2.set_thumbnail(url="https://image.noelshack.com/fichiers/2018/27/3/1530710705-7c3da55251ad4733ffcf9e6ec6d9601c.png")
    if message.channel.is_private: #Empêcher le bot de répondre aux messges privés.
        await client.send_message(message.author, embed=embed)
        await client.send_message(message.author, embed=embed2)
    else:
        await client.delete_message(message)
        info_message = await client.send_message(message.channel, message.author.mention + " L'aide vous à été envoyé en message privé." )
        await client.send_message(message.author, embed=embed)
        await client.send_message(message.author, embed=embed2)
        await asyncio.sleep(2.0)
        await client.delete_message(info_message)

async def invite(message, client):
    servers_num = str(len(client.servers))
    embed = discord.Embed(title="Liens", description= """
[Serveur Discord](https://discord.gg/Dgdurw9)
[Site web](https://baptiste0928.net/geekbot/)
""", color=0x006400)
    if message.channel.is_private: #Empêcher le bot de répondre aux messges privés.
        await client.send_message(message.author, embed=embed)
    else:
        await client.delete_message(message)
        info_message = await client.send_message(message.channel, message.author.mention + " Les liens vous ont été envoyés en message privé." )
        await client.send_message(message.author, embed=embed)
        await asyncio.sleep(2.0)
        await client.delete_message(info_message)
