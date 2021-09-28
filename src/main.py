import requests
import threading
import os
import json
import time
import logging as log


# Config
scoresUrl = "https://discord.com/api/webhooks/890472004002664448/T58YyTYxJMijUOyNTdxUxVh4i5fX8a0h9SUvmnyotJPWXxnEuDZGVwtndEUjacL5KTNg"
log.basicConfig(level=log.INFO)
url = "http://127.0.0.1:24050/json"

# Check for updates
releaseURL = "https://api.github.com/repos/Tiller431/score-notifier/actions/artifacts"

resp = requests.get(releaseURL).json()
latestVersion = resp["artifacts"][0]
print("Download for the newest release of this program:", latestVersion["archive_download_url"])


def sendMSG(msg):
    data = {
        "content": msg,
    }
    requests.post(scoresUrl, json=data)


def startGosu():
    # Change this to the path of your exe if this isnt in the same directory example: C:\\GosuMemory\\gosumemory.exe
    os.system("gosumemory.exe")


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

    if playerData["menu"]["state"] == 2:
        oldState = 2
        log.info("Player is playing a map")

    if playerData["menu"]["state"] == 7 and oldState == 2:
        oldState = 7
        log.info("Player just set a score. Sending to discord!")
        msg = "New play from {}!\n".format(playerData["resultsScreen"]["name"])
        
        msg += "▸ {} ▸ {}PP ({}PP for {}% FC) ▸ {}%\n".format(playerData["gameplay"]["hits"]["grade"]["current"], playerData["gameplay"]["pp"]["current"], playerData["gameplay"]["pp"]["fc"], playerData["gameplay"]["accuracy"], playerData["gameplay"]["accuracy"])
        msg += "▸ {} ▸ x{}/{} ▸ [{}/{}/{}/{}]\n".format(playerData["gameplay"]["score"], playerData["gameplay"]["combo"]["current"], playerData["gameplay"]["combo"]["max"], playerData["gameplay"]["hits"]["300"], playerData["gameplay"]["hits"]["100"], playerData["gameplay"]["hits"]["50"], playerData["gameplay"]["hits"]["0"])

        sendMSG(msg)
    elif playerData["menu"]["state"] == 7 and oldState != 2:
        oldState = 7
        log.info("Player is looking at a score")

