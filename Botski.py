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
            self.sock.send( bytes( "JOIN " + channel + " " + key ) )
        else:
            self.sock.send( bytes( "JOIN " + channel ) )

    def do_joins( self, f_channels='./channels' ):
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
                self.sock.send( bytes( "PONG: %s" %msg[1] + "\n" ) )

bot = Botski( debug = 1 ) 
bot.load_config('./config' ) # Probably auto define this later or allow optional specification of a new config with assumed value of ./config 
bot.setup_sock()
bot.do_joins()
bot.read_sock()
