MainAPILink: str = 'https://api.hypixel.net/'
ResourcesLink: str = f'{MainAPILink}resources/'
ResourcesVanity: str = f'{ResourcesLink}vanity/'
ResourcesSkyblock: str = f'{ResourcesLink}skyblock/'
MainSkyblock: str = f'{MainAPILink}skyblock/'

APIKeyInfo: str = f'{MainAPILink}key'
Player: str = f'{MainAPILink}player'
Friends: str = f'{MainAPILink}friends'
RecentGames: str = f'{MainAPILink}recentgames'
Status: str = f'{MainAPILink}status'
Guild: str = f'{MainAPILink}guild'
RankedSkywars: str = f'{Player}/ranked/skywars'
ResourcesGames: str = f'{ResourcesLink}games'
ResourcesAchievements: str = f'{ResourcesLink}achievements'
ResourcesChallenges: str = f'{ResourcesLink}challenges'
ResourcesQuests: str = f'{ResourcesLink}quests'
ResourcesGuildsAchievements: str = f'{ResourcesLink}guilds/achievements'
ResourcesVanityPets: str = f'{ResourcesVanity}pets'
ResourcesVanityCompanions: str = f'{ResourcesVanity}companions'
ResourcesSkyblockCollections: str = f'{ResourcesSkyblock}collections'
ResourcesSkyblockSkills: str = f'{ResourcesSkyblock}skills'
ResourcesSkyblockItems: str = f'{ResourcesSkyblock}items'
ResourcesSkyblockElection: str = f'{ResourcesSkyblock}election'
ResourcesSkyblockBingo: str = f'{ResourcesSkyblock}bingo'
SkyblockNews: str = f'{MainSkyblock}news'
SkyblockAuction: str = f'{MainSkyblock}auction'
SkyblockAuctions: str = f'{MainSkyblock}auctions'
SkyblockAuctionsEnded: str = f'{MainSkyblock}auctions_ended'
SkyblockBazaar: str = f'{MainSkyblock}bazaar'
SkyblockProfile: str = f'{MainSkyblock}profile'
SkyblockProfiles: str = f'{MainSkyblock}profiles'
SkyblockBingo: str = f'{MainSkyblock}bingo'
Boosters: str = f'{MainAPILink}boosters'
Counts: str = f'{MainAPILink}counts'
Leaderboards: str = f'{MainAPILink}leaderboards'
PunishmentStats: str = f'{MainAPILink}punishmentstats'

ErrorMessages = ["Some data is missing, this is usually a field.",
                 "Access is forbidden, usually due to an invalid API key being used.",
                 "No data could be found for the requested player.",
                 "Some data provided is invalid.",
                 "A request limit has been reached, usually this is due to the limit on the key being reached but can also be triggered by a global throttle.",
                 "The data is not yet populated and should be available shortly.",
                 "Wrong type of API key. API key should be 'str' type.",
                 "No data could be found for the provided player uuid.",
                 "Undefined error."]