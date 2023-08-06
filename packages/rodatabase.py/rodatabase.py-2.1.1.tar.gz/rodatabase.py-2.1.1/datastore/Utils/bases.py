from typing import Optional
from ..datastorereq import Requests
import base64, hashlib, json


class BaseDataStore:
    def __repr__(self) -> str:
        return f"<BaseDataStore {self.datastore}>"
    def __init__(self, json, datastore, token, apitoken, id):
        self._json = json
        self.datastore = datastore 
        self.requests: Requests = Requests()
        self.token = apitoken
        self.id = id
        self.set_token(token)
    def set_token(self, token: str):
        """
        Sets the token for the datastore.
        Arguments:
            token: The token to set.
        """
        self.requests.session.cookies[".ROBLOSECURITY"] = token
    async def get_keys(self, limit: Optional[int] = 100):
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
            params={'datastoreName': self.datastore, 'prefix': '', 'limit': limit}
        )
        return response.json()
    async def set_data(self, key: str, data):
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
            params={'datastoreName': self.datastore, 'entryKey': key}
        )
        return response.json()
    async def increment_data(self, key: str, incrementby: int):
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
            params={'datastoreName': self.datastore, 'entryKey': key}
        )
        return response.json()
    async def delete_data(self, key: str):
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
            params={'datastoreName': self.datastore, 'entryKey': key}
        )
        return response.json()
    async def get_data(self, key: str):
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
            params={'datastoreName': self.datastore, 'entryKey': key}
        )
        return response.json()
