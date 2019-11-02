#!/usr/bin/python

import socket
import os.path

class Botski( object ):
    def __init__( self, debug=0 ):
        self.debug = debug

    def load_config( self, config ):
        self.config = config 
        conf_values = {}
        config_file = open( self.config, 'r' )

        for line in config_file.readlines():
            values                   = line.split( '=' )
            conf_values[ values[0] ] = values[1]

        self.user   = conf_values[ 'user' ].rstrip()
        self.server = conf_values[ 'server' ].rstrip()
        self.nick   = conf_values[ 'nick' ].rstrip()
        self.port   = conf_values[ 'port' ].rstrip()
        self.port   = int( self.port ) # We have to do this for socket not to complain
        self.log_file = conf_values[ 'log_file' ].rstrip()

        if self.debug:
            print "[DEBUG] Nick: "   + self.nick
            print "[DEBUG] User: "   + self.user
            print "[DEBUG] Server: " + self.server
            print "[DEBUG] Port: "   + str( self.port )

    def setup_sock( self ):
        self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.sock.connect( ( self.server, self.port ) )
        self.sock.send( bytes("USER "+ self.nick +" "+ self.nick +" "+ self.nick + " " + self.nick + "\n") )
        self.sock.send( bytes( "NICK " + self.nick + "\n" ) )


    def join_channel( self, channel, *key ):
        if key:
            self.sock.send( bytes( "JOIN " + channel + " " + key + "\n" ) )
        else:
            self.sock.send( bytes( "JOIN %s\n" % channel ) )

    def version( self ):
        # Returns server version
        self.sock.send( bytes( "VERSION\n" ) )

    def info( self ):
        # Returns server info 
        self.sock.send( bytes( "INFO\n" ) )

    def admin( self ):
        # Instructs the server to return information about the administrators 
        self.sock.send( bytes( "ADMIN\n" ) )

    def stats( self ):
        # Returns statistics about the current server
        self.sock.send( bytes( "STATS\n" ) )
 
    def motd( self ):
        # Returns the MOTD
        self.sock.send( bytes( "MOTD\n" ) )

    def names( self, *channel ):
        # Returns a list of who is on
        if channel:
            self.sock.send( bytes( "NAMES %s\n" % channel ) )
        else:
            self.sock.send( bytes( "NAMES\n") )

    def whois( self, nick ):
        # Returns whois information a nick
        self.sock.send( bytes( "WHOIS "+ nick + "\n") )

    def lusers( self ):
        # Returns statistics about the size of the network.
        self.sock.send( bytes( "LUSERS\n" ) )

    def servlist( self ) :
        # Lists the services currently on the network.
        self.sock.send( bytes( "SERVLIST\n" ) )
  
    def list( self ):
        # Lists all channels on the server.
        self.sock.send( bytes( "LIST\n" ) )

    def time( self ):
        # Returns the local time on the current server.
        self.sock.send( bytes( "TIME\n" ) )

    def uhnames( self ):
        # Instructs the server to send names in an RPL_NAMES reply in the long format:
        # This command is not formally defined in an RFC, but is recognized by most major IRC daemons.
        self.sock.send( bytes( "UHNAMES\n" ) )

    def userip( self ):
        # Requests the direct IP address of the user with the specified nickname.
        # This command is not formally defined in an RFC, but is recognized by most major IRC daemons.
        self.sock.send( bytes( "USERIP\n" ) )

    def userhost( self ):
        # Returns a list of information about the nicknames specified.
        # This command is not formally defined in an RFC, but is recognized by most major IRC daemons.
        self.sock.send( bytes( "USERHOST\n" ) )

    def rules( self ):
        # Requests the server rules. 
        # This command is not formally defined in an RFC, but is recognized by most major IRC daemons.
        self.sock.send( bytes( "RULES\n" ) )
    
    #def ison( self, nicknames ):
        # Queries for a space-separated list <nicknames> to see if they are on server
        #self.sock.send( bytes( "ISON " + " ".join(nicknames) )

    def do_config_joins( self, f_channels='./channels' ):
        channels = {}

        if os.path.isfile( f_channels ) and os.stat( f_channels ).st_size > 0: # These checks could probably be better...
            channel_fh = open( f_channels, 'r' ) 

            for line in channel_fh.readlines():
                line = line.rstrip()
                values = line.split( ':' )

                try:
                    channels[ values[0] ] = values[1]
                except:
                    channels[ values[0] ] = ''

        else:
            print "No file or file is empty: " + f_channels
            die 

        for key, value in channels.iteritems():
            if self.debug == 1:
                print "JOIN " + key + " " + value
            self.sock.send( bytes( "JOIN " + key + " " + value + "\n" ) ) # This should call the sub above

    def read_sock( self ):
        while 1:
            data = self.sock.recv( 1024 )
            data = data.strip( '\n\r' )

            if self.debug == 1:
                print data

            msg = str.split( str( data ) )
            if msg[0] == "PING":
                self.sock.send( bytes( "PONG: %s" % msg[1] + "\n" ) )

bot = Botski( debug = 1 ) 
bot.load_config('./config' ) # Probably auto define this later or allow optional specification of a new config with assumed value of ./config 
bot.setup_sock()
# We should do recon before we do our joins
# list users online and do a whois on them
bot.join_channel("#TheName")
bot.join_channel("#TheGame")
#bot.info()
#bot.admin()
#bot.lusers()
#bot.version()
#bot.stats()
bot.names()
bot.names("#TheGame")
#bot.uhnames()
#bot.time()
#bot.list()
#bot.whois("nito")
#bot.rules()
# list channels, we might want to join them

# This is a command that joins channels from a config file.
#bot.do_config_joins()

#Join channels not already in your config

# listen to the channels and record conversations

bot.read_sock()
