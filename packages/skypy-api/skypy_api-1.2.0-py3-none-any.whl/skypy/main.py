# skypy(skypy-api) by FuchsCrafter - https://github.com/FuchsCrafter/skypy
# Also check out skypy-webui - https://github.com/FuchsCrafter/skypy-webui

import requests
import json

class skypy:
  """ The skypy class for the module. Uses a api key that you can find by running /api on mc.hypixel.net """
  def __init__(self, key="NO_KEY", no_api_key=False):
    global apikey
    if not no_api_key or key == "NO_KEY":
      returns = False
    else:
      apikey = str(key)
      r = requests.get("https://api.hypixel.net/key?key="+ key)
      returns = json.loads(r.text)
      returns = returns["success"]

    if not returns and not no_api_key and key != "NO_KEY":
      print("Invalid API Key! Please note that you cant use some modules now!")

  def getNews(self):
    """ Gets the latest SkyBlock news"""
    r = requests.get("https://api.hypixel.net/skyblock/news?key=" + apikey)
    returns = json.loads(r.text)
    if not returns["success"]:
      print("Failed! Make sure that you api key is correct!")
    else:
      return returns["items"]

  class bazaar:
    """ The bazaar class was made to get bazaar values from certain items. """
    def __init__(self):
      pass

    def fetchAllProducts(self):
      """ Fetches all products and returns them as a JSON string. """
      r = requests.get("https://api.hypixel.net/skyblock/bazaar")
      r = json.loads(r.text)
      return r["products"]

    def fetchProduct(self, itemname, quickmode=False):
      """ Fetches a specific product and returns his data as a JSON string. Use Quick Mode for shortet but cleaner returns. Returns False if the product is not found. """
      r = requests.get("https://api.hypixel.net/skyblock/bazaar")
      bazaarProducts = json.loads(r.text)
      bazaarProducts = bazaarProducts["products"]
      try:
        if not quickmode:
          return bazaarProducts[itemname]
        else:
          _ = bazaarProducts[itemname]
          return _["quick_status"]
      except:
        return False
  class auction:
    """ The auction class is there to get auction informations. It requires the Hypixel api key (log into mc.hypixel.net and type /api in chat)."""
    def __init__(self):
      pass

    def getAuctionByPlayer(self, uuid):
      """ Gets the auction by a player uuid. """
      r = requests.get("https://api.hypixel.net/skyblock/auction?key=" + apikey + "&player=" + uuid)
      returns = json.loads(r.text)
      if not returns["success"]:
        print("Failed! Make sure, that you api key and the uuid is correct!")
      else:
        return json.loads(returns["auctions"])

    def getAuctionByPlayerName(self, player):
      """ Uses the Mojang API to get the uuid of a player. """
      r = requests.get("https://api.mojang.com/users/profiles/minecraft/" + player)
      returns = json.loads(r.text)
      try:
        playeruuid = returns["id"]
        return self.getAuctionByPlayer(playeruuid)
      except:
        print("Invalid Playername!")

    def getAuction(self, auctionid):
      """ Gets an auction by its ID. """
      r = requests.get("https://api.hypixel.net/skyblock/auction?key=" + apikey + "&uuid=" + auctionid)
      returns = json.loads(r.text)
      if not returns["success"]:
        print("Failed! Make sure, that you api key and the auction-id is correct!")
      else:
        return json.loads(returns["auctions"])
   
    def getAuctions(self):
      """ Gets all active auctions. You dont need an API key for this. """
      r = requests.get("https://api.hypixel.net/skyblock/auctions")
      returns = json.loads(r.text)
      return json.loads(returns["auctions"])

    def getEndedAuctions(self):
      """ Gets the latest ended auctions. It works also without any authorization."""
      r = requests.get("https://api.hypixel.net/skyblock/auctions_ended")
      returns = json.loads(r.text)
      return json.loads(returns["auctions"])
  class politics:
    """ The politics class is there to get the current election results or the current mayor. """
    def __init__(self):
      pass
    def getCurrentMayor(self, quickmode=False):
      """ Gets the current mayor an his perks. """
      r = requests.get("https://api.hypixel.net/resources/skyblock/election")
      returns = json.loads(r.text)

      if quickmode:
        returns = returns["mayor"]
        name = returns["name"]
        mkey = returns["key"]
        _ = {"name": name,"key": mkey}
        return _
      else:
        return returns["mayor"]

    def getCurrentElection(self, quickmode=False, full=True):
      """ Gets the current election results. Using Quickmode only gets the canidates list with all the child data."""
      r = requests.get("https://api.hypixel.net/resources/skyblock/election")
      returns = json.loads(r.text)
      if not quickmode:
        return returns["current"]
      else:
        _ = returns["current"]["candidates"]
        returns = {}
        for element in _:
          if full:
            returns[element["name"]] = {"name": element["name"],"key": element["key"], "votes": element["votes"], "perks": element["perks"]}
          else:
            returns[element["name"]] = {"name": element["name"],"key": element["key"], "votes": element["votes"]}
        return returns

    def getElectionResults(self):
      """ Gets only the election votes. """
      r = requests.get("https://api.hypixel.net/resources/skyblock/election")
      returns = json.loads(r.text)
      _ = returns["current"]["candidates"]
      returns = {}
      for element in _:
        returns[element["name"]] = element["votes"]
      return returns

