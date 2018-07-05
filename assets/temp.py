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
import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

def init():
    cursor.execute("""
CREATE TABLE IF NOT EXISTS warns(
    server_id VARCHAR NOT NULL,
    user_id VARCHAR NOT NULL,
    count INT
);
""")
    cursor.execute("""
CREATE TABLE IF NOT EXISTS mute(
    server_id VARCHAR NOT NULL,
    user_id VARCHAR NOT NULL,
    muted BOOLEAN
);
""")
    conn.commit()
    return conn



def getwarn(user_id, server_id):
    cursor.execute("""SELECT count FROM warns WHERE server_id=? AND user_id=?""", (server_id, user_id))
    try:
        count = cursor.fetchone()[0]
    except TypeError:
        count = 0
    return count

def setwarn(user_id, server_id, count=0):
    if getwarn(user_id,server_id) > 0:
        cursor.execute("""UPDATE warns SET count=? WHERE server_id=? AND user_id=?""", (count, server_id, user_id))
    else:
        cursor.execute("""INSERT INTO warns(server_id, user_id, count) VALUES(?, ?, ?)""", (server_id, user_id, count))

def addwarn(user_id, server_id):
    count = getwarn(user_id,server_id)+1

    if getwarn(user_id,server_id) > 0:
        cursor.execute("""UPDATE warns SET count=? WHERE server_id=? AND user_id=?""", (count, server_id, user_id))
    else:
        cursor.execute("""INSERT INTO warns(server_id, user_id, count) VALUES(?, ?, ?)""", (server_id, user_id, count))



def mute(user_id, server_id):
    cursor.execute("""SELECT muted FROM mute WHERE server_id=? AND user_id=?""", (server_id, user_id))
    if cursor.fetchone():
        cursor.execute("""UPDATE mute SET muted=1 WHERE server_id=? AND user_id=?""", (server_id, user_id))
    else:
        cursor.execute("""INSERT INTO mute(server_id, user_id, muted) VALUES(?, ?, 1)""", (server_id, user_id))


def unmute(user_id, server_id):
    cursor.execute("""SELECT muted FROM mute WHERE server_id=? AND user_id=?""", (server_id, user_id))
    if cursor.fetchone():
        cursor.execute("""UPDATE mute SET muted=0 WHERE server_id=? AND user_id=?""", (server_id, user_id))
    else:
        cursor.execute("""INSERT INTO mute(server_id, user_id, muted) VALUES(?, ?, 0)""", (server_id, user_id))

def ismute(user_id, server_id):
    cursor.execute("""SELECT muted FROM mute WHERE server_id=? AND user_id=?""", (server_id, user_id))
    try:
        if cursor.fetchone()[0] == 1:
            muted = True
        else:
            muted = False
    except TypeError:
        muted = False
    return muted
