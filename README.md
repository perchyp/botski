# botski
A simple Python IRC bot, written as a learning exercise

Botski reads the config file to know which server, port, nick, etc to use when connecting to IRC.

Botski reads the channels file to know which channels to join after it connects. 
Channels are line-separated, and should contain the leading poundsign (#).
If the channel(s) require a key, specify that like using, #channel:key
