import pytz

TIMEZONE = pytz.timezone('Asia/Taipei')
LOGFILENAME = 'web.log'
USERS = {'baha': {'password': 'minecraft'}}

class Web:
    PORT = 5000
    HOST = 'localhost'

class Mcrcon:
    HOST = "localhost"
    PORT = 25575
    PASSWD = "bahaminecraft"

class Command:
    START = "tmux new-session -ds mcserver \"source $HOME/.bashrc;source $HOME/.profile;bash -c 'cd /home/bahaminecraft87/minecraft; ./run.sh'\""
    STOP = "/stop"

class Url:
    MOJANG_API = 'https://api.mojang.com/users/profiles/minecraft/'
    HEAD_IMG = 'https://mc-heads.net/avatar/'
