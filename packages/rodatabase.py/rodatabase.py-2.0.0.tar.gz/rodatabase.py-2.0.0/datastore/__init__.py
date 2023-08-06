from typing import Optional
from .datastorereq import Requests
import base64, hashlib, json
from .Utils.bases import BaseDataStore

class DatabaseClient:
    def __init__(self, universeId: int, token: str, ROBLOSECURITY: Optional[str] = None, responsetype: Optional[str] = 'class'):
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
        self.response = responsetype
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
    async def get_datastore(self, datastore: str):
        """
        Gets the datastore with the specified name.
        Arguments:
            datastore: The name of the datastore to get.
        Returns: JSON Object or Class.
        """
        response = await self.requests.get(
            url=f"https://apis.roblox.com/datastores/v1/{self.id}/standard-datastores/datastore/entries",
            headers={'x-api-key': self.token},
            params={'datastoreName': datastore, 'prefix': '', 'limit': 100}
        )
        if self.response == 'class':
            return BaseDataStore(response.json()[f"{datastore}"], datastore, self.token, self.token)
        else:
            return response.json()


