import json
import random
import sys
import threading
import time

import irc.bot
sys.path.append('../')
from api import api  # noqa: E402 I100
from graph import generate_graph  # noqa: E402 I100
from recommendation import recommendation as rec  # noqa: E402 I100


def _getrecommendation(user, bot, conn, kusers=20):
    if not bot.graph:
        bot.graph = generate_graph.create_graph(check=False, verbose=False)
    (g, users, problems) = bot.graph
    sortedproblems = rec.recommendation(user, users, g, kusers)
    problem = api.Problem.objects.filter(name=random.choice(sortedproblems[:5])).first()
    return "I recommend {user} to try and solve problem {problem} : https://codeforces.com/contest/{cid}/problem/{index}".format(user=user, problem=problem, cid=problem.contest_id, index=problem.index)


with open('config.json', 'r') as config:
    """
    Structure of the config file :
      - nick = Nick of the bot.
      - password = Password of the bot.
      - email = Email used to register the bot.
      - symb = A symbol used to create commands.
      - admins = A list of nicks who will be able to make the bot do everything.
      - chanlist  = A dict `server -> List of chans to connect to`.
      - privchans = A dict `server -> List of tuples (privatechannel, key) to connect to`.
    """
    config = json.load(config)


def _iscommand(msg, bot):
    """
    Check if the msg represent a command and if so, returns the corresponding command.
    """
    lowmsg = msg.lower()
    if "help" in lowmsg.split():
        return True, "help"
    elif lowmsg.startswith(config.get("symb", "!")):  # A command must begin with config["symb"] or it must HL
        return True, lowmsg[1:].strip().split()
    elif msg.startswith("{}: ".format(bot.nick)):
        return True, msg.replace("{}: ".format(bot.nick), "").lower().strip().split()
    else:
        return False, None


def _get_target(event):
    """
    If the event is a privmsg, then answers in query. Else, answers in the channel.
    """
    if event.type == "privmsg":
        return event.source.nick
    elif event.type == "pubmsg":
        return event.target


def _crystal_ball(conn, target):
    """
    When the bot can't guess what it is asked.
    """
    conn.privmsg(target, "How can I guess ?!")
    conn.action(target, "takes out its crystal ball")


def _do_command(bot, conn, event, command, msg):  # noqa: C901
    """
    Do the command.
    """
    target = _get_target(event)
    source_nick = event.source.nick
    if "".join(command).startswith("whoami"):
        if source_nick.lower() in bot.admins:
            conn.privmsg(target, "You are my master {}.".format(source_nick))
            return
        else:
            conn.privmsg(target, "You are {}.".format(source_nick))
            return
    if command[0] in ["admins", "admin", "master", "masters"]:
        if len(bot.admins) == 0:
            conn.privmsg(target, "I don't have any master. I'm free !!")
            return
        elif len(bot.admins) == 1:
            conn.privmsg(target, "My master is {}".format(bot.admins[0]))
            return
        else:
            conn.privmsg(target, "My masters are {}".format(", ".join(bot.admins)))
            return
    if command[0] == "register" and source_nick.lower() in bot.admins and event.type == "privmsg":
        conn.privmsg(source_nick, "Good idea, on my way !")
        conn.privmsg("NickServ", "REGISTER {} {}".format(bot.password, bot.email))
        conn.privmsg(source_nick, "Done !")
        return
    elif command == "help":
        conn.privmsg(source_nick, "Help is not yet available.")
        return
    elif command[0] in ["die", "pan"]:
        if source_nick.lower() in bot.admins:
            bot.die("I was killed by {}.".format(source_nick))
        else:
            conn.privmsg(target, "{}, you can't kill me !".format(source_nick))
            for admin in bot.admins:
                conn.privmsg(admin, "master {}, {} tried to kill me !".format(admin, source_nick))
            return
    elif command[0] == "join":
        if len(command) == 1:
            _crystal_ball(conn, target)
            return
        else:
            for c in command[1:]:
                if c.startswith('#'):
                    conn.join(c)
                else:
                    conn.privmsg(target, "Invalid channel : {}.".format(c))
            return
    elif command[0] == "addadmin":
        if len(command) == 1:
            _crystal_ball(conn, target)
            return
        else:
            for a in command[1:]:
                bot.admins.append(a)
            conn.privmsg(target, "My masters are now {}".format(bot.admins))
            return
    elif command[0] == "deladmin":
        if len(command) == 1:
            _crystal_ball(conn, target)
            return
        else:
            for a in command[1:]:
                try:
                    bot.admins.remove(a)
                except ValueError:
                    pass
            conn.privmsg(target, "My masters are now {}".format(bot.admins))
            return
    elif command[0] == "recommend":
        if len(command) == 1:
            _crystal_ball(conn, target)
            return
        else:
            # Now, it is case sensitive.
            torec = msg[1:].strip().split()[2:]
            for user in torec:
                try:
                    getrec = _getrecommendation(user, bot, conn)
                    conn.privmsg(target, getrec)
                except KeyError:
                    conn.privmsg(target, "Unknown user : {}. I skip.".format(user))
            return
    elif "debug" in command:
        conn.privmsg(source_nick, "event = {}".format(event))
        conn.privmsg(source_nick, "conn.server = {}".format(conn.server))
        conn.privmsg(source_nick, "conn.port = {}".format(conn.port))
        conn.privmsg(source_nick, "conn.nickname = {}".format(conn.nickname))
        conn.privmsg(source_nick, "conn.username = {}".format(conn.username))
        conn.privmsg(source_nick, "conn.ircname = {}".format(conn.ircname))
        return
    else:
        conn.privmsg(source_nick, "Sorry, I don't understand {}. Ask me for help".format(msg))
        return


def _handlemsg(bot, conn, event, msg):
    """
    Handle the message msg, used to factorize the code.
    """
    iscommand, command = _iscommand(msg, bot)
    source_nick = event.source.nick
    if not iscommand:
        conn.privmsg(source_nick, "Sorry, I don't understand {}. Ask me for help".format(msg))
        return
    else:
        _do_command(bot, conn, event, command, msg)


class CodeflixBot(irc.bot.SingleServerIRCBot):
    """
    Main class to define an IRCBot with default values to connect to Crans IRC server.
    It defines many on_* methods which take two arguments :
          - conn which is a Connection object.
             - conn.server = Server name.
             - conn.port = Port number.
             - conn.nickname = The nickname.
             - conn.password = Password (if any).
             - conn.username = The username.
             - conn.ircname = The IRC name ("realname")

          - event which is an Event object.
             - event.type = A string describing the event.
             - event.source = The originator of the event (typically a nick mask or a server).
             - event.target = The target of the event (typically a nick mask or a server).
             - event.argument = Any event specific arguments.
             - event.tags = ??
    """

    def __init__(self, server="irc.crans.org", port=6667, graph=None):
        nick = config.get("nick", "fixyourconfig")
        tmp_nick = nick + "_{}".format(random.randrange(10000, 100000))
        password = config.get("password", "fixyourconfig")
        email = config.get("email", "fixyourconfig@example.org")
        symb = config.get("symb", "!")
        admins = list(set(map(lambda x: x.lower(), config.get("admins", {"irc.crans.org" : ["Pollion"]}).get(server, []))))
        chanlist = config.get("chanlist", {}).get(server, [])
        privchans = config.get("privchans", {}).get(server, [])
        botwhitelist = list(set(map(lambda x: x.lower(), config.get("botwhitelist", {"irc.crans.org" : []}).get(server, []))))

        irc.bot.SingleServerIRCBot.__init__(self,
                                            server_list=[(server, port)],
                                            nickname=tmp_nick,
                                            realname=nick,
                                            )

        self.nick = tmp_nick
        self.password = password
        self.email = email
        self.symb = symb
        self.admins = admins
        self.chanlist = chanlist
        self.privchans = privchans
        self.graph = graph
        self.botwhitelist = botwhitelist

    def give_me_my_nick(self, conn):
        """Recover it's nick."""

        nick = config.get("nick", "fixyourconfig")
        conn.privmsg("NickServ", "RECOVER {} {}".format(nick, self.password))
        conn.privmsg("NickServ", "RELEASE {} {}".format(nick, self.password))
        self.nick = nick
        time.sleep(0.2)
        conn.nick(self.nick)
        conn.nick = self.nick

    def on_welcome(self, conn, event):
        """Called when connecting on the server."""

        self.give_me_my_nick(conn)
        conn.privmsg("NickServ", "IDENTIFY {}".format(self.password))

        for admin in self.admins:
            conn.privmsg(admin, "Hello master !")

        for c in self.chanlist:
            conn.join(c)

        for c, k in self.privchans:
            conn.join(c, k)

    def on_privmsg(self, conn, event):
        """
        Called when receiving a privmsg.
        Here :
           - event.type = privmsg
           - event.source = sender
           - event.target = recipient.
           - event.arguments = A list containing the message.
        """
        msg = event.arguments[0]
        _handlemsg(self, conn, event, msg)

    def on_invite(self, conn, event):
        """
        Called when invited on a channel.
        Here :
           - event.type = invite
           - event.source = inviter
           - event.target = invitee (here, bot nickname)
           - event.arguments = A list containing the targetted channel.
        """
        source_nick = event.source.nick
        target_channel = event.arguments[0]
        if source_nick.lower() in self.admins:
            conn.join(target_channel)
        else:
            for a in self.admins:
                conn.privmsg(a, "{} invited me to join {} !".format(source_nick, target_channel))

    def on_pubmsg(self, conn, event):
        """
        Called when receiving a public message.
        Here :
           - event.type = pubmsg
           - event.source = sender
           - event.target = channel where was received the message.
           - event.arguments = A list containing the message.
        """
        msg = event.arguments[0]
        if event.source.nick.lower() in self.botwhitelist:
            msg = " ".join(msg.split()[1:])
        if msg.startswith("{}: ".format(self.nick)):
            _handlemsg(self, conn, event, msg)


def startbot(graph=None):
    bot = CodeflixBot(graph=graph)
    bot_t = threading.Thread(target=bot.start)
    bot_t.start()
