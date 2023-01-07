# -*- coding: utf-8 -*-
"""
Chat Room Demo for Miniboa.
"""

import logging
from miniboa import TelnetServer

IDLE_TIMEOUT = 300000
CLIENT_LIST = []
PLAYER_LIST = []
room0_list = []
room1_list = []
SERVER_RUN = True

class Player():

    def __init__(self,truename,desc,speaker,name,clientname,room):
        self.truename = truename
        self.desc = desc
        self.speaker = speaker
        self.name = name
        self.clientname = clientname
        self.linkedto = 'nobody'
        self.room = room

def on_connect(client):
    """pyth
    Sample on_connect function.
    Handles new connections.
    """
    logging.info("Opened connection to {}".format(client.addrport()))
    broadcast("{} joins the conversation.\n".format(client.addrport()))
    CLIENT_LIST.append(client)
    player = Player(client.addrport(),"Amorphous and void...",'silent',client.addrport(),client,"0")
    PLAYER_LIST.append(player)
    room0_list.append(player.clientname)

    for guest in CLIENT_LIST: ### This sends the message to the specific person who just logged in
        if guest == client:
            guest.send("You send your soul into the black mirror...\n")
#           client.send("You wait in the empty void between worlds...") # because why not have alternate dimensions within your own mud?
            guest.send("You go towards the light of another world on the other side of the mirror...\n")
            guest.send("You must (think name ) of the personal (yourname) of the creature who's body you wish to inhabit\n")


def on_disconnect(client):
    """
    Sample on_disconnect function.
    Handles lost connections.
    """
    logging.info("Lost connection to {}".format(client.addrport()))
    CLIENT_LIST.remove(client)
    broadcast("{} leaves the conversation.\n".format(client.addrport()))


def kick_idle():
    """
    Looks for idle clients and disconnects them by setting active to False.
    """
    # Who hasn't been typing?
    for client in CLIENT_LIST:
        if client.idle() > IDLE_TIMEOUT:
            logging.info("Kicking idle lobby client from {}".format(
                client.addrport()))
            client.active = False


def process_clients():
    """
    Check each client, if client.cmd_ready == True then there is a line of
    input available via client.get_command().
    """
    for client in CLIENT_LIST:
        if client.active and client.cmd_ready:
            # If the client sends input echo it to the chat room
            chat(client)


def broadcast(msg):
    """
    Send msg to every client.
    """
    for client in CLIENT_LIST:
        client.send(msg)


def chat(client):
    """
    Echo whatever client types to everyone.
    """
    global SERVER_RUN
    msg = client.get_command()
    logging.info("{} says '{}'".format(client.addrport(), msg))

    for player in PLAYER_LIST: #looks through the list for each individual player
        if client.addrport() in player.truename: # checks each player to see if their truename matches the addr port of the person sending THIS cmd
            player.speaker = 'speaking' # if the above code finds a match, it changes their speaker variable to true, identifying them as the speaker
            global speakername
            speakername = player.name
            global speakerroom #some code for who can hear which says based on what room they're in
            speakerroom = player.room


    cmd = msg.lower()
    # bye = disconnect
    if cmd == 'quit game':
        client.active = False
    # shutdown == stop the server    
    #elif cmd == 'shutdown':   ### blotted these out so so the machine who started the server controls it via their
    #    SERVER_RUN = False    ### console program, no having a random player kill the server because they're a grump

    if cmd[0:4] == ('say '):
        for guest in CLIENT_LIST: # this has to be here otherwise it doesn't read playername
            if speakerroom == "0": 
                if guest != client and guest in room0_list:
                    guest.send("{} says '{}'\n".format(speakername, cmd[4:])) # has your renamed name when you say things
            if speakerroom == "1": 
                if guest != client and guest in room1_list:
                    guest.send("{} says '{}'\n".format(speakername, cmd[4:])) # has your renamed name when you say things            
            if guest == client:
                guest.send("You say '{}'\n".format(cmd[4:]))

    if cmd == ('west'):
        for guest in CLIENT_LIST:
            if speakerroom == "0": 
                if guest != client and guest in room0_list:
                    guest.send("{} travels west.\n".format(speakername))
            if speakerroom == "1": 
                if guest != client and guest in room1_list:
                    guest.send("{} travels west.\n".format(speakername))
            if speakerroom == "0":
                if guest != client and guest in room1_list:
                    guest.send("{} travels in from the east.\n".format(speakername))                                
        for player in PLAYER_LIST:
            if 'speaking' in player.speaker:
                if player.room == "0":
                    player.room = "1"
                    room0_list.remove(player.clientname)
                    room1_list.append(player.clientname)
                    for guest in CLIENT_LIST:
                        if guest == client:
                            guest.send("You travel to the west.\n")
                            guest.send("A sprawling, jungle-choked ruin.\n")
                            guest.send("This land gives off the smell of unspoiled wilderness.  There are of course, many trees\n")
                            guest.send("all around you, but the plant life is not growing solely on natural earthen soil, but\n")
                            guest.send("is also a sprawling ruin with the crumbling and tottering remains of square-cut, towering\n")
                            guest.send("cement structures made by intelligent creatures of some sort.  Birds flock in the trees\n")
                            guest.send("and numerous vermin scurry across the grounds.  Occassionally one can hear distant howls\n")
                            guest.send("and roars...\n")                     
            print((player.name)+(player.room))

    if cmd == ('east'):
        for guest in CLIENT_LIST:
            if speakerroom == "0": 
                if guest != client and guest in room0_list:
                    guest.send("{} travels east.\n".format(speakername))
            if speakerroom == "1": 
                if guest != client and guest in room1_list:
                    guest.send("{} travels east.\n".format(speakername)) 
            if speakerroom == "1":
                if guest != client and guest in room0_list:
                    guest.send("{} travels in from the west.\n".format(speakername))                    
        for player in PLAYER_LIST:
            if 'speaking' in player.speaker:
                if player.room == "1":
                    player.room = "0"
                    room1_list.remove(player.clientname)
                    room0_list.append(player.clientname)
                    for guest in CLIENT_LIST:
                        if guest == client:
                            guest.send("You travel to the east.\n")
                            guest.send("A null, black void. \n") 
                            guest.send("This place is empty, black nothingness, but it does have it's own sort of clarity so that \n")
                            guest.send("sight and senses are not impaired at all.  The ceiling of this place is an endless slab of \n")
                            guest.send("glossy black material showing a shimmering reflection of your real human body, playing on \n")
                            guest.send("your device...\n")                    
            print((player.name)+(player.room))

    if cmd == 'addresses':
        for client in CLIENT_LIST: #looks through the list for specific instances of client
            print(client.addrport()) # prints the addrport of each client

    if cmd == 'players':
        for player in PLAYER_LIST:
            print((player.name)+(player.truename)) 

    if cmd[0:11] == ('think name '):
        for player in PLAYER_LIST:
            if 'speaking' in player.speaker: # checks to find a match of who is speaking
                player.name = (cmd[11:])    # once it finds them it changes THEIR name only? hopefully?
                for guest in CLIENT_LIST: ### does a good job of controlling who gets sent what
                    if guest == client:   
                        guest.send("You must (think description ) of the (yourdescription) of the creature who's body you wish to inhabit...\n")

    if cmd[0:18] == ('think description '):
        for player in PLAYER_LIST:
            if 'speaking' in player.speaker:
                player.desc = (cmd[18:])

    if cmd == ('look'):
        if speakerroom == "1":
                for guest in CLIENT_LIST:
                    if guest == client:
                            guest.send("A sprawling, jungle-choked ruin.\n")
                            guest.send("This land gives off the smell of unspoiled wilderness.  There are of course, many trees\n")
                            guest.send("all around you, but the plant life is not growing solely on natural earthen soil, but\n")
                            guest.send("is also a sprawling ruin with the crumbling and tottering remains of square-cut, towering\n")
                            guest.send("cement structures made by intelligent creatures of some sort.  Birds flock in the trees\n")
                            guest.send("and numerous vermin scurry across the grounds.  Occassionally one can hear distant howls\n")
                            guest.send("and roars...\n")

        if speakerroom == "0":
                for guest in CLIENT_LIST:
                    if guest == client:
                            guest.send("A null, black void. \n") 
                            guest.send("This place is empty, black nothingness, but it does have it's own sort of clarity so that \n")
                            guest.send("sight and senses are not impaired at all.  The ceiling of this place is an endless slab of \n")
                            guest.send("glossy black material showing a shimmering reflection of your real human body, playing on \n")
                            guest.send("your device...\n")            

    if cmd[0:5] == ('look '): 
        if speakerroom == "0":
            for player in PLAYER_LIST: #### untested code for only being able to look at players in the same room as you
                if cmd[5:] == player.name:
                    if player.clientname in room0_list:
                        for guest in CLIENT_LIST:
                            if guest == client:                    
                                guest.send((player.desc)+('\n'))
        if speakerroom == "1":
            for player in PLAYER_LIST: #### untested code for only being able to look at players in the same room as you
                if cmd[5:] == player.name:
                    if player.clientname in room1_list:
                        for guest in CLIENT_LIST:
                            if guest == client:                    
                                guest.send((player.desc)+('\n'))                                 
    
    if cmd[0:10] == ('mind link '):
        for player in PLAYER_LIST:
            if cmd[10:] == player.name:
                global linkee
                linkee = player.clientname
                for player in PLAYER_LIST:                    
                    if 'speaking' in player.speaker:
                        player.linkedto = linkee
                        #print(player.linkedto)
                        linkee = 'nobody'
                        
    if cmd[0:6] == ('telep '):
        for player in PLAYER_LIST:                 
            if 'speaking' in player.speaker:
                global sendee                   
                sendee = player.linkedto
                for guest in CLIENT_LIST:
                    if guest == sendee:                    
                        guest.send((msg)+('\n'))
                    
    for player in PLAYER_LIST: #looks through the list for specific instances of players
        player.speaker = 'silent' # changes each players speaker variable to false

    #while SERVER_RUN == True:
    #    global oneloop
    #    oneloop += .000000000000000000000000000000000000000000000000000000000000000000000001
    #    if oneloop > 99999999999999999999999999999999999999999999999999999999999999999999:
    #        oneloop = 0


if __name__ == '__main__':

    # Simple chat server to demonstrate connection handling via the
    # async and telnet modules.
    logging.basicConfig(level=logging.DEBUG)

    # Create a telnet server with a port, address,
    # a function to call with new connections
    # and one to call with lost connections.
    telnet_server = TelnetServer(
        port=7777,
        address='',
        on_connect=on_connect,
        on_disconnect=on_disconnect,
        timeout=.05)

    logging.info("Listening for connections on"
                 " port {}. CTRL-C to break.".format(telnet_server.port))

    # Server Loop
    while SERVER_RUN:
        telnet_server.poll()    # Send, Recv, and look for new connections
        kick_idle()    # Check for idle clients
        process_clients()    # Check for client input

    logging.info("Server shutdown.")
