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
import datetime

async def insult(message, client):
    logs_chan = discord.utils.get(client.get_all_channels(), server__name = str(message.server), name = "logs")
    if logs_chan == None:
        logs_chan = await client.create_channel(message.server, "logs")
    embed = discord.Embed(title="Insulte supprimée", description="""
**Utilisateur:** <@""" + message.author.id + """>
**Salon:** <#""" + str(message.channel.id) + """>
**Message:**
""" + message.clean_content + """
""",color=0xC60800)
    await client.send_message(logs_chan,embed=embed)

async def spam(message, client):
    logs_chan = discord.utils.get(client.get_all_channels(), server__name = str(message.server), name = "logs")
    if logs_chan == None:
        logs_chan = discord.utils.get(client.get_all_channels(), server__name = str(message.server), name = "logs-geekbot")
        if logs_chan == None:
            logs_chan = await client.create_channel(message.server, "logs")
    embed = discord.Embed(title="Tentative de spam bloquée", description="""
**Utilisateur:** <@""" + message.author.id + """>
**Salon:** <#""" + str(message.channel.id) + """>
""",color=0xC60800)
    await client.send_message(logs_chan,embed=embed)

async def report(message, report_user, reason, last_message, client):
    logs_chan = discord.utils.get(client.get_all_channels(), server__name = str(message.server), name = "logs")
    if logs_chan == None:
        logs_chan = discord.utils.get(client.get_all_channels(), server__name = str(message.server), name = "logs-geekbot")
        if logs_chan == None:
            logs_chan = await client.create_channel(message.server, "logs")
    embed = discord.Embed(description= """
:warning: **<@""" + str(report_user.id) + """> à été signalé par <@""" + str(message.author.id) + """> dans <#""" + str(message.channel.id) + """>.**

**Dernier message de """ + str(report_user.name) + """:**
""" + str(last_message) + """

**Raison:**
""" + reason + """
""", color=0xFFA500)
    await client.send_message(logs_chan,embed=embed)

async def warn(message, warned_user, reason, client):
    logs_chan = discord.utils.get(client.get_all_channels(), server__name = str(message.server), name = "logs")
    if logs_chan == None:
        logs_chan = discord.utils.get(client.get_all_channels(), server__name = str(message.server), name = "logs-geekbot")
        if logs_chan == None:
            logs_chan = await client.create_channel(message.server, "logs")
    embed = discord.Embed(description= """
:warning: **<@""" + str(warned_user.id) + """> à reçu un avertissement de la part de <@""" + str(message.author.id) + """> !**

**Raison:**
""" + reason + """
""", color=0xff0000)
    await client.send_message(logs_chan,embed=embed)

async def auto_mute(message, client):
    logs_chan = discord.utils.get(client.get_all_channels(), server__name = str(message.server), name = "logs")
    if logs_chan == None:
        logs_chan = discord.utils.get(client.get_all_channels(), server__name = str(message.server), name = "logs-geekbot")
        if logs_chan == None:
            logs_chan = await client.create_channel(message.server, "logs")
    embed = discord.Embed(description= """
:warning: **<@""" + str(message.author.id) + """> à été mute pendant 30min (à la suite de 3 infractions) !**
""", color=0xFFA500)
    await client.send_message(logs_chan,embed=embed)
    await client.send_message(message.author, ":warning: Vous avez été mute pendant **30min** sur **" + message.server.name + "** à la suite de 3 infractions. " )

async def mute(message, client, time, muted_user, reason):
    logs_chan = discord.utils.get(client.get_all_channels(), server__name = str(message.server), name = "logs")
    if logs_chan == None:
        logs_chan = discord.utils.get(client.get_all_channels(), server__name = str(message.server), name = "logs-geekbot")
        if logs_chan == None:
            logs_chan = await client.create_channel(message.server, "logs")
    if time != False:
        duration = " pendant " + str(int(time/60)) + "min "
    else:
        duration = ""
    embed = discord.Embed(description= """
:warning: **<@""" + str(muted_user.id) + """> à été mute par <@""" + str(message.author.id) + """>""" + duration + """ !**
**Raison:** """ + reason + """
""", color=0xFFA500)
    await client.send_message(logs_chan,embed=embed)
