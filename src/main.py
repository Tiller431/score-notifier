import requests
import threading
import os
import json
import time
import logging as log


# Config
lbwh = "https://discord.com/api/webhooks/890431880124563527/nJPDD0Si0qhstTN_vx1Oq36qI0d4PPqFtXUvl-s9o9n80dIpfj1uDsKEvXSWif35C76Y"
ppwh = "https://discord.com/api/webhooks/890472004002664448/T58YyTYxJMijUOyNTdxUxVh4i5fX8a0h9SUvmnyotJPWXxnEuDZGVwtndEUjacL5KTNg"
log.basicConfig(level=log.INFO)
url = "http://127.0.0.1:24050/json"


def sendMSG(msg, url):
    data = {
        "content": msg,
    }
    requests.post(url, json=data)


def startGosu():
    # Change this to the path of your exe if this isnt in the same directory
    os.system("gosumemory.exe")


#def checkUpdates():
    # https://api.github.com/repos/octocat/hello-world/releases/latest


try:
    requests.get(url)
except requests.exceptions.ConnectionError:
    gosuThread = threading.Thread(target=startGosu)
    gosuThread.start()
    time.sleep(2)
oldState = 0
while True:
    time.sleep(0.5)
    playerData = requests.get(url).json()

    if playerData["menu"]["state"] == oldState:
        continue

    if playerData["menu"]["state"] == 7:
        oldState = 7
        log.info("Player is on score screen")

    if playerData["menu"]["state"] == 5:
        oldState = 5
        log.info("Player is selecting a map")
