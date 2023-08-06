"""REST API Light"""

import json
import asyncio

from aiohttp import (
    ClientConnectionError,
    ClientResponse,
    ClientSession,
    ClientTimeout,
    ServerDisconnectedError,
)

from .exceptions import (
    InvalidEffect,
    Unavailable
)

from .typing import (InfoData, Pixel)

class RestLight:
    """REST API Light."""

    _REQUEST_TIMEOUT = ClientTimeout(total=5, sock_connect=3)

    def __init__(
        self,
        session: ClientSession,
        device_id: int,
        host: str,
        port: int = 25741,
    ) -> None:
        """Initialise the client."""
        self._session: ClientSession = session
        self._device_id: int = device_id
        self._host:str = host
        self._port:int = port

        self._name: str
        self._model: str
        self._is_on: bool
        self._brightness: int
        self._hue: int
        self._saturation: int
        self._pixel_count: int
        self._pixels: list[Pixel]
        self._effects_values: list[str]
        self._effect: str

    @property
    def host(self) -> str:
        """Return the host."""
        return self._host

    @property
    def port(self) -> int:
        """Return the port."""
        return self._port

    @property
    def _api_url(self) -> str:
        return f"http://{self.host}:{self.port}/api/v3"
        
    # Device Info Properties

    @property
    def name(self) -> str:
        """Return the name."""
        return self._name

    @property
    def is_on(self) -> bool:
        """Return if the light is on."""
        return self._is_on

    @property
    def brightness(self) -> int:
        """Return the brightness."""
        return self._brightness

    @property
    def hue(self) -> int:
        """Return the hue."""
        return self._hue

    @property
    def saturation(self) -> int:
        """Return the saturation."""
        return self._saturation

    @property
    def effects_values(self) -> list[str]:
        """Return the list of supported effects."""
        return self._effects_values

    @property
    def effect(self) -> str:
        """Return the selected effect."""
        return self._effect

    @property
    def pixel_count(self) -> int:
        """Return the pixel count."""
        return self._pixel_count

    @property
    def pixels(self) -> list[Pixel]:
        """Return the pixels."""
        return self._pixels

    async def _request(
        self, method: str, path: str, data: dict | None = None, headers: dict | None = None
    ) -> ClientResponse:
        url = f"{self._api_url}/{self._device_id}/{path}"
        json_data = json.dumps(data)
        try:
            try:
                response = await self._session.request(
                    method, url, data=json_data, timeout=self._REQUEST_TIMEOUT, headers=headers)
            except ServerDisconnectedError:
                response = await self._session.request(
                    method, url, data=json_data, timeout=self._REQUEST_TIMEOUT, headers=headers)
        except ClientConnectionError as err:
            raise Unavailable from err
        except asyncio.TimeoutError as err:
            raise Unavailable from err
        response.raise_for_status()
        return response

    async def get_info(self) -> None:
        """Get all device into."""
        response = await self._request("get", "")
        data: InfoData = await response.json()
        self._name = data["name"]
        self._model = data["model"]
        self._is_on = data["state"]["on"]
        self._brightness = data["state"]["brightness"]
        self._hue = data["state"]["hue"]
        self._saturation = data["state"]["saturation"]
        self._pixel_count = data["state"]["pixels"]["count"]
        self._pixels = data["state"]["pixels"]["values"]
        self._effects_values = data["effects"]["values"]
        self._effect = data["effects"]["select"]

    async def set_state(
        self,
        on: bool | None = None,
        brightness: int | None = None,
        brightness_relative: bool = False,
        brightness_transition: int | None = None,
        hue: int | None = None,
        hue_relative: bool = False,
        saturation: int | None = None,
        saturation_relative: bool = False
    ) -> None:
        """Set a new state."""
        data = {}

        async def _add_topic_to_data(
            topic: str, value: int | bool | None, relative: bool = False
        ) -> None:
            if value is not None:
                if relative:
                    data[topic] = {"increment": value}
                else:
                    data[topic] = {"value": value}
            
            await _add_topic_to_data("on", on)
            await _add_topic_to_data("brightness", brightness, brightness_relative)
            if brightness_transition is not None:
                if "brightness" in data:
                    data["brightness"]["duration"] = brightness_transition
            await _add_topic_to_data("hue", hue, hue_relative)
            await _add_topic_to_data("saturation", saturation, saturation_relative)
            if data:
                await self._request("put", "state", data, {'Content-Type': 'application/json'})

    async def _set_state(
        self,
        topic: str,
        value: int | bool,
        relative: bool = False,
        transition: int | None = None
    ) -> None:
        """Set the state of a specific characteristic."""
        data: dict
        if relative:
            data = {topic: {"increment": value}}
        else:
            data = {topic: {"value": value}}
        if transition is not None:
            data[topic]["duration"] = transition
        await self._request("put", "state", data, {'Content-Type': 'application/json'})

    async def turn_on(self) -> None:
        """Turn on the light."""
        await self._set_state("on", True)

    async def turn_off(self) -> None:
        """Turn on the light."""
        await self._set_state("on", False)

    async def set_brightness(self, brightness: int, relative: bool = False, transition: int | None = None) -> None:
        """Set the brightness."""
        await self._set_state("brightness", brightness, relative, transition)

    async def set_hue(self, hue: int, relative: bool = False) -> None:
        """Set the hue."""
        await self._set_state("hue", hue, relative)

    async def set_saturation(self, saturation: int, relative: bool = False) -> None:
        """Set the saturation."""
        await self._set_state("saturation", saturation, relative)

    async def identify(self) -> None:
        """Identify the light."""
        await self._request("put", "identify")

    async def set_effect(self, effect: str) -> None:
        """Set the effect."""
        if effect not in self._effects_values:
            raise InvalidEffect
        await self._request("put", "effects", {"select": effect}, {'Content-Type': 'application/json'})