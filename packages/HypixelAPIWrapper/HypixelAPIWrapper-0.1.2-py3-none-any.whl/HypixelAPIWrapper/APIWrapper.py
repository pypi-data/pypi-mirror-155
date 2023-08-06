import requests
from HypixelAPIWrapper.exceptions import *
from HypixelAPIWrapper.models import *
from HypixelAPIWrapper.utils import *
import json


class APIWrapper():
    def __init__(self, apiKey: str) -> None:
        self.session: requests.session = requests.session()
        if type(apiKey) == str: self.headers = {'API-Key': apiKey}
        else: raise WrongAPIKey(ErrorMessages[-3])
        response: requests.Response = self.session.get(APIKeyInfo, headers = self.headers)
        checkStatusCode(response.status_code)
        self.owner: str = json.loads(response.content)['record']['owner']
        self.lastResponseHeaders: dict = response.headers
    
    def get(self, url: str) -> requests.Response:
        response: requests.Response = self.session.get(url, headers = self.headers)
        self.lastResponseHeaders = response.headers
        return response
    
    def getOwner(self) -> str: return self.owner
    
    def getLastResponseHeaders(self) -> dict: return self.lastResponseHeaders
    
    def getPlayerData(self, uuid: str) -> dict: return oneParamRequest(Player, 'uuid', uuid, self)
    
    def getFriends(self, uuid: str) -> dict: return oneParamRequest(Friends, 'uuid', uuid, self)
        
    def getRecentGames(self, uuid: str) -> dict: return oneParamRequest(RecentGames, 'uuid', uuid, self)
    
    def getStatus(self, uuid: str) -> dict: return oneParamRequest(Status, 'uuid', uuid, self)
    
    def getGuild(self, id = None, player = None, name = None) -> dict:
        return threeParamsRequest(Guild, 'id', 'player', 'name', id, player, name, self)
    
    def getRankedSkywars(self, uuid: str) -> dict: return oneParamRequest(RankedSkywars, 'uuid', uuid, self)
    
    def getResourcesGames(self) -> dict: return simpleGetRequest(ResourcesGames, self)
        
    def getResourcesAchievements(self) -> dict: return simpleGetRequest(ResourcesAchievements, self)
    
    def getResourcesChallenges(self) -> dict: return simpleGetRequest(ResourcesChallenges, self)
    
    def getResourcesQuests(self) -> dict: return simpleGetRequest(ResourcesQuests, self)
    
    def getResourcesGuildsAchievements(self) -> dict: return simpleGetRequest(ResourcesGuildsAchievements, self)
        
    def getResourcesVanityPets(self) -> dict: return simpleGetRequest(ResourcesVanityPets, self)
    
    def getResourcesVanityCompanions(self) -> dict: return simpleGetRequest(ResourcesVanityCompanions, self)
    
    def getResourcesSkyblockCollections(self) -> dict: return simpleGetRequest(ResourcesSkyblockCollections, self)
        
    def getResourcesSkyblockSkills(self) -> dict: return simpleGetRequest(ResourcesSkyblockSkills, self)
    
    def getResourcesSkyblockItems(self) -> dict: return simpleGetRequest(ResourcesSkyblockItems, self)
    
    def getResourcesSkyblockElection(self) -> dict: return simpleGetRequest(ResourcesSkyblockElection, self)
    
    def getResourcesSkyblockBingo(self) -> dict: return simpleGetRequest(ResourcesSkyblockBingo, self)
    
    def getSkyblockNews(self) -> dict: return simpleGetRequest(SkyblockNews, self)
    
    def getSkyblockAuction(self, uuid = None, player = None, profile = None) -> dict:
        return threeParamsRequest(SkyblockAuction, 'uuid', 'player', 'profile', uuid, player, profile, self)
    
    def getSkyblockAuctions(self, page: int) -> dict: return oneParamRequest(SkyblockAuctions, 'page', page, self)
    
    def getSkyblockAuctionsEnded(self) -> dict: return simpleGetRequest(SkyblockAuctionsEnded, self)
    
    def getSkyblockBazaar(self) -> dict: return simpleGetRequest(SkyblockBazaar, self)
    
    def getSkyblockProfile(self, profile: str) -> dict: return oneParamRequest(SkyblockProfile, 'profile', profile, self)
    
    def getSkyblockProfiles(self, uuid: str) -> dict: return oneParamRequest(SkyblockProfiles, 'uuid', uuid, self)
    
    def getSkyblockBingo(self, uuid: str) -> dict: return oneParamRequest(SkyblockBingo, 'uuid', uuid, self)
        
    def getBoosters(self) -> dict: return simpleGetRequest(Boosters, self)
        
    def getCounts(self) -> dict: return simpleGetRequest(Counts, self)
        
    def getLeaderboards(self) -> dict: return simpleGetRequest(Leaderboards, self)
        
    def getPunishmentStats(self) -> dict: return simpleGetRequest(PunishmentStats, self)
    
    @staticmethod
    def decodeNBT(raw: str) -> dict: return nbt.read_from_nbt_file(BytesIO(b64decode(raw)))