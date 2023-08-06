from typing import Optional
from .datastorereq import Requests
import base64, hashlib, json

class DatabaseClient:
    def __init__(self, universeId: int, token: str, ROBLOSECURITY: Optional[str] = None):
        """
        universeId: The ID of the universe to connect to.
        token: The API token to use for requests.
        roblosecurity: The .ROBLOSECURITY token to use for authentication.

        Functions: 
            get_datastores: Returns a list of all datastores in the universe.
            get_keys: Returns a list of all keys in the specified datastore.
            set_data: Sets the data in the specified datastore.
            increment_data: Increments the data in the specified datastore.
        """
        self.token = token
        self.requests: Requests = Requests()
        self.id = universeId
        self.set_token(token=ROBLOSECURITY)
    def set_token(self, token: str):
        """
        Authenticates the client with the passed .ROBLOSECURITY token.
        This method does not send any requests and will not throw if the token is invalid.
        Arguments:
            token: A .ROBLOSECURITY token to authenticate the client with.
        """
        self.requests.session.cookies[".ROBLOSECURITY"] = token
    async def get_datastores(self):
        """
        Gets the datastores associated with the game.
        Returns: JSON Object.
        """
        response = await self.requests.get(
            url=f"https://apis.roblox.com/datastores/v1/{self.id}/standard-datastores",
            headers={'x-api-key': self.token}
        )
        return response.json()
    async def get_keys(self, datastore: str, limit: Optional[int] = 100):
        """
        Gets the keys of the given datastore.
        Arguments:
            datastore: The name of the datastore to get the keys of.
            limit: The maximum number of keys to return.
        Returns: JSON Object.
        """
        if limit > 100:
            raise TypeError("Limit must be less than or equal to 100.")
        response = await self.requests.get(
            url=f"https://apis.roblox.com/datastores/v1/universes/{self.id}/standard-datastores/datastore/entries",
            headers={'x-api-key': self.token},
            params={'datastoreName': datastore, 'prefix': '', 'limit': limit}
        )
        return response.json()
    async def set_data(self, datastore: str, key: str, data):
        """
        Sets the data in the specified datastore.
        Arguments:
            datastore: The name of the datastore to set the data in.
            key: The key to set the data under.
            data: The data to set.
        Retuns: JSON Object.
        """
        sdata = json.dumps(data)
        sdata = str(base64.b64encode(hashlib.md5(bytes(sdata, encoding='utf8')).digest()), encoding='utf8')
        response = await self.requests.post(
            url=f"https://apis.roblox.com/datastores/v1/universes/{self.id}/standard-datastores/datastore/entries/entry",
            headers={'x-api-key': self.token, 'content-md5': sdata},
            json=data,
            params={'datastoreName': datastore, 'entryKey': key}
        )
        return response.json()
    async def increment_data(self, datastore: str, key: str, incrementby: int):
        """
        Increments the data in the specified datastore.
        Arguments:
            datastore: The name of the datastore to increment the data in.
            key: The key to increment the data under.
            incrementby: The amount to increment the data by.
        Retuns: JSON Object.
        """
        response = await self.requests.post(
            url=f"https://apis.roblox.com/datastores/v1/universes/{self.id}/standard-datastores/datastore/entries/entry/increment",
            headers={'x-api-key': self.token},
            json={"incrementBy": incrementby},
            params={'datastoreName': datastore, 'entryKey': key}
        )
        return response.json()
    async def delete_data(self, datastore: str, key: str):
        """
        Deletes the data in the specified datastore entry.
        Arguments:
            datastore: The name of the datastore to delete the data in.
            key: The key to delete the data under.
        Retuns: JSON Object.
        """
        response = await self.requests.delete(
            url=f"https://apis.roblox.com/datastores/v1/universes/{self.id}/standard-datastores/datastore/entries/entry",
            headers={'x-api-key': self.token},
            params={'datastoreName': datastore, 'entryKey': key}
        )
        return response.json()
    async def get_data(self, datastore: str, key: str):
        """
        Gets the data in the specified datastore entry.
        Arguments:
            datastore: The name of the datastore to get the data in.
            key: The key to get the data under.
        Retuns: JSON Object.
        """
        response = await self.requests.get(
            url=f"https://apis.roblox.com/datastores/v1/universes/{self.id}/standard-datastores/datastore/entries/entry",
            headers={'x-api-key': self.token},
            params={'datastoreName': datastore, 'entryKey': key}
        )
        return response.json()

import asyncio
ban_data = {'reason': 'sleep', 'BannedBy': 'xKen_t (1356185892)', 'PlayerName': 'xKen_t'}

