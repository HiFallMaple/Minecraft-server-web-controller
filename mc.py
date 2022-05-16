from mcstatus import MinecraftServer
from config import Mcrcon, Command, Url
from mcrcon import MCRcon
import os
import requests
import subprocess
import time
import logging


mcrcon = MCRcon(host=Mcrcon.HOST, port=Mcrcon.PORT, password=Mcrcon.PASSWD)
server = MinecraftServer.lookup("localhost:25565")


def is_online() -> bool:
    try:
        mcrcon.connect()
        return True
    except ConnectionRefusedError:
        return False


def stop() -> bool:
    if is_online():
        mcrcon.connect()
        mcrcon.command("/stop")
        while tmux_exist():
            time.sleep(0.5)
        return True
    return False


def start() -> bool:
    if not is_online():
        os.system(Command.START)
        while not is_online():
            time.sleep(0.5)
        logging.info('start')
        return True
    return False


def status():
    if is_online():
        return server.status().players


def online_account() -> dict:
    if is_online():
        account_list = list()
        for name in server.query().players.names:
            resp = requests.get(Url.MOJANG_API+name)
            account = {
                'id': resp.json()['id'],
                'name': name
            }
            account_list.append(account)
        return account_list
    return dict()

def op(username: str):
    if is_online():
        mcrcon.connect()
        return mcrcon.command(f"/op {username}")


def tmux_exist() -> bool:
    result = subprocess.run(['tmux', 'ls'], stdout=subprocess.PIPE)
    return 'mcserver' in result.stdout.decode('utf-8')