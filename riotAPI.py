import os
import pprint
from typing import Optional, TypedDict

import requests
from dotenv import load_dotenv
from requests.models import Response


def main():
    # pprint.pprint(getMatch("GW toucouille"), width=1)
    getMatch("GW toucouille")


def getMatch(summonerName):

    load_dotenv()
    RIOT_TOKEN = os.getenv("RIOT_TOKEN")

    """
        Response status:
            0: Summoner not found
            1: Summoner not in game
            2: Summoner in game
    """
    response_status: int = 0
    encryptedId: str = getSummonerId(summonerName, RIOT_TOKEN)
    if encryptedId:
        matchData: dict = getMatchEncryptedId(encryptedId, RIOT_TOKEN)
        if matchData:
            response_status = 2
            parsedMatch: tuple[int, list[dict]] = parseMatch(matchData)
            for i in range(len(parsedMatch[1])):
                parsedMatch[1][i].update(
                    getPlayerRatio(
                        parsedMatch[1][i]["summonerId"],
                        RIOT_TOKEN))
            pprint.pprint(parsedMatch)
            return (response_status, parsedMatch)
        response_status = 1
    return (response_status, {})


def parseMatch(matchData: dict) -> tuple[int, list[dict]]:
    parsedMatchData: tuple[int, list[dict]]
    queue: int = matchData["gameQueueConfigId"]
    keysToRemove: list[str] = [
        "perks",
        "profileIconId",
        "bot",
        "spell1Id",
        "spell2Id",
        "gameCustomizationObjects"]
    players: list[dict] = [matchData["participants"][i]
                           for i in range(len(matchData["participants"]))]
    for i in range(len(players)):
        for key in keysToRemove:
            players[i].pop(key, None)
    parsedMatchData = (queue, players)
    return parsedMatchData


def getPlayerRatio(encryptedSummonerId: str, token: Optional[str]) -> dict:
    url: str = "https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/"
    payload: dict = {"api_key": token}
    try:
        r: Response = requests.get(url + encryptedSummonerId, params=payload)
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Can't retrieve summoner data")
        return {}
    else:
        playerRatio: dict = r.json()[0]
        keysToRemove: list[str] = [
            "leagueId",
            "summonerId",
            "summonerName",
            "queueType",
            "hotStreak",
            "veteran",
            "freshBlood",
            "inactive",
            "miniSeries"
        ]
        for key in keysToRemove:
            playerRatio.pop(key, None)
        playerRatio["winRate"] = int(
            playerRatio["wins"] / (playerRatio["wins"] + playerRatio["losses"]) * 100)
        return playerRatio


def getSummonerId(summonerName: str, token: Optional[str]) -> str:
    url: str = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
    payload: dict = {"api_key": token}
    try:
        r: Response = requests.get(url + summonerName, params=payload)
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Summoner not found")
        return ""
    else:
        return r.json()['id']


def getMatchEncryptedId(
        encryptedSummonerId: str,
        token: Optional[str]) -> dict:
    url: str = "https://euw1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/"
    payload: dict = {"api_key": token}
    try:
        r: Response = requests.get(url + encryptedSummonerId, params=payload)
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Summoner not in game")
        return {}
    else:
        print(r.json())
        return r.json()


queues: dict = {
    0: {
        "map": "Game custom",
        "description": None
    },
    430: {
        "map": "Summoner's Rift",
        "description": "5v5 Blind Pick"
    },
    420: {
        "map": "Summoner's Rift",
        "description": "5v5 Ranked Solo"
    },
    76: {
        "map": "Summoner's Rift",
        "description": "Ultra Rapide Fire"
    },
    83: {
        "map": "Summoner's Rift",
        "description": "Co-op vs AI Ultra Rapide Fire"
    },
    400: {
        "map": "Summoner's Rift",
        "description": "5v5 Draft Pick"
    },
    440: {
        "map": "Summoner's Rift",
        "description": "5v5 Ranked Flex"
    },
    450: {
        "map": "Howling Abyss",
        "description": "5v5 ARAM"
    },
    700: {
        "map": "Summoner's Rift",
        "description": "Clash"
    },
    900: {
        "map": "Summoner's Rift",
        "description": "Ultra Rapid Fire"
    },
    1020: {
        "map": "Suommoner's Rift",
        "description": "One For All"
    },
    1300: {
        "map": "Nexus Blitz",
        "description": "Nexus Blitz"
    },
    1400: {
        "map": "Summoner's Rift",
        "description": "Ultimate Spellbook"
    },
}

if __name__ == "__main__":
    main()
