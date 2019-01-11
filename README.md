# botski
A simple Python IRC bot, written as a learning exercise

Botski reads the config file to know which server, port, nick, etc to use when connecting to IRC.

Botski reads the channels file to know which channels to join after it connects. 
Channels are line-separated, and should contain a leading poundsign (#channel).
If channels require a key, specify that by using, #channel:key

# A Note
This project is a learning exercise. For that reason, botski does it's own file ops and parasing, rather than using Python built-ins.

# What's Next
The script is in dire need of error handling and sanity checking, especially where users are expected to provide input. Additionally, the main while loop that reads the socket likely needs to be put into a try/except pattern.
