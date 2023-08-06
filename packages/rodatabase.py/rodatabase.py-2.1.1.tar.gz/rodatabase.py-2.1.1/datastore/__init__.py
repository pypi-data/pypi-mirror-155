from typing import Optional
from .datastorereq import Requests
import base64, hashlib, json
from .Utils.bases import BaseDataStore

class DatabaseClient:
    def __init__(self, universeId: int, token: str, ROBLOSECURITY: str, responsetype: Optional[str] = 'class'):
        """
        universeId: The ID of the universe to connect to.
        token: The API token to use for requests.
        roblosecurity: The .ROBLOSECURITY token to use for authentication.
        responsetype: The type of response to return. NOTE: Class is slower then json. 'class' | 'json'

        Functions: 
            get_datastores: Returns a list of all datastores in the universe.
            get_datastore: Returns a class or json object of the datastore with the specified name.
        """
        if not responsetype == 'class' or responsetype == 'json':
            raise TypeError("Invalid response type.")
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
    @classmethod
    async def get_datastore(self, datastore: str):
        """
        Gets the datastore with the specified name.
        Arguments:
            datastore: The name of the datastore to get.
        Returns: JSON Object or Class.
        """
        response = await self.requests.get(
            url=f"https://apis.roblox.com/datastores/v1/universes/{self.id}/standard-datastores",
            headers={'x-api-key': self.token},
        )
        if self.response == 'class':
            for i in response.json()["datastores"]:
                try:
                    data = BaseDataStore(i, datastore, self.token, self.token, self.id)
                    return data
                    
                except:
                    pass
        elif self.response == 'json':
            return response.json()[f"{datastore}"]
        else:
            raise TypeError("Invalid response type.")




