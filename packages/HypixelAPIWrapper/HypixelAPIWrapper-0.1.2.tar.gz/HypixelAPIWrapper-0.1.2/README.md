# Hypixel API wrapper
A small  library for using Hypixel API methods.

### Installation
```
pip install HypixelAPIWrapper
```

### Get started
How to get progile information with this lib:

```Python
from HypixelAPIWrapper import APIWrapper

# Instantiate a wrapper object
APIKey = 'xxxxxxxx-xxxx-xxxx-xxxxx-xxxxxxxxxxxx'
wrapper = APIWrapper(APIkey)

# Get owner uuid
owner = wrapper.getOwner()

# Get player data
profile = wrapper.getPlayerData(owner)
```