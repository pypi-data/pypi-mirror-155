from typing import Any, Dict, Optional, Union

from aiohttp import ClientSession

from wottle.exception import CityError, TokenError


class Wottle:
    def __init__(
        self, token: Optional[str] = None, language: str = "ru"
    ) -> None:

        if not token:
            raise TokenError(
                "Invalid Token! You can get it here: "
                "https://openweathermap.org/api."
            )

        self.token = token
        self.language = language
        self.url = "http://api.openweathermap.org/data/2.5/weather"

        self.session = ClientSession(
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    async def get_weather(self, city: Optional[str] = None) -> Dict[str, Any]:

        if not city:
            raise CityError("Invalid city! In an empty city.")

        response = await self.session.get(self.url, params=self.in_json(city))

        json = await response.json()
        await self.session.close()

        if not json:
            raise CityError(
                "Invalid city! The city you specified was not found."
            )

        return json

    def in_json(self, city: Union[str]) -> Dict[str, str]:

        return {"q": city, "lang": self.language, "appid": self.token}
