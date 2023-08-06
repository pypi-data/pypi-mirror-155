from contextlib import contextmanager
import os
from typing import Any, Dict
from aiohttp import ClientSession, ClientResponse
from async_rundeck.exceptions import RundeckError
from copy import deepcopy


class RundeckClient:
    _default_options = {
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    }

    def __init__(
        self,
        url: str = None,
        token: str = None,
        username: str = None,
        password: str = None,
        api_version: int = None,
    ) -> None:
        self.url = url or os.getenv("RUNDECK_URL", "http://localhost:4440")
        self.url = self.url.rstrip("/")
        self.token = token or os.getenv("RUNDECK_TOKEN")
        self.username = username or os.getenv("RUNDECK_USERNAME")
        self.password = password or os.getenv("RUNDECK_PASSWORD")
        self.api_version = api_version or int(os.getenv("RUNDECK_API_VERSION", "32"))
        if self.token is None and (self.password is None or self.password is None):
            raise ValueError("Cannot authenticate without a token or username/password")
        self.session_id: str = None
        self._session: ClientSession = None
        self._context_options: Dict[str, Any] = deepcopy(self._default_options)

    @contextmanager
    def context_options(self, options: Dict[str, Any]) -> Any:
        self._context_options = options
        yield
        self._context_options = deepcopy(self._default_options)

    @property
    def version(self) -> str:
        """Alias of api_version"""
        return self.api_version

    @property
    def options(self) -> Dict[str, Dict[str, Any]]:
        options = self._context_options
        if self.session_id is not None:
            options["cookies"] = {"JSESSIONID": self.session_id}

        return options

    def format_url(self, path: str, **kwargs) -> str:
        """format url with path and query parameters

        Parameters
        ----------
        path : str
            accesing url

        Returns
        -------
        str
            formatted url
        """
        return (self.url + path).format(**kwargs)

    async def __aenter__(self) -> "RundeckClient":
        if self._session is None:
            self._session = ClientSession()
            self._session = await self._session.__aenter__()
            if self.token is None and self.session_id is None:
                self.session_id = await self.auth(self._session)
        return self

    async def __aexit__(self, *args) -> "RundeckClient":
        if self._session is not None:
            await self._session.__aexit__(*args)
        self._session = None

    def request(self, method: str, url: str, **kwargs) -> ClientResponse:
        """Requesting a resource

        Parameters
        ----------
        method : str
            Requesting method
        url : str
            url to request

        Returns
        -------
        ClientResponse
            response object. see aiohttp.ClientResponse for more details
        """
        options = self.options
        for k, v in kwargs.items():
            if isinstance(v, dict):
                options.setdefault(k, {}).update(v)
            else:
                options[k] = v
        if self.token:
            options["headers"]["X-Rundeck-Auth-Token"] = self.token

        return self._session.request(method, url, **options)

    async def auth(self, session: ClientSession) -> str:
        """username/password authentication

        Parameters
        ----------
        session : ClientSession
            session to use for authentication

        Returns
        -------
        str
            session id

        Raises
        ------
        RundeckError
            if authentication fails
        """
        url = self.url + "/j_security_check"
        p = {"j_username": self.username, "j_password": self.password}
        async with session.post(
            url,
            data=p,
        ) as response:
            if len(response.history) > 1:
                async with response.history[0] as r:
                    session_id = r.cookies.get("JSESSIONID")
            else:
                session_id = response.cookies.get("JSESSIONID")
        if session_id is None:
            raise RundeckError("Authrorization failed")
        return session_id.value
