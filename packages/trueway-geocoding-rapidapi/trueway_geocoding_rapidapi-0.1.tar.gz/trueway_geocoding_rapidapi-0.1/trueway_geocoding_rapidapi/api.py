from __future__ import annotations

from typing import AnyStr
from typing import Dict
from typing import List
from typing import Optional
from urllib.parse import urlencode

import aiohttp
from purl import URL

from trueway_geocoding_rapidapi.schemas.schema import ReverseGeocodeItem
from trueway_geocoding_rapidapi.schemas.schema import ReverseGeocodeModel


class TrueWayGeocodeRapidAPI(object):
    def __init__(self, rapidapi_host: AnyStr, rapidapi_key: AnyStr):
        """
        Buy a plan here: https://rapidapi.com/trueway/api/trueway-geocoding/
        :param rapidapi_host: X-RapidAPI-Host header & Base URL (i.e. trueway-geocoding.p.rapidapi.com)
        :param rapidapi_key: X-RapidAPI-Key header (i.e. 930193396dkk30df818ae0b85e1afp195723jsn7f904ccbeae9)
        """
        self.headers = {
            "X-RapidAPI-Host": rapidapi_host,
            "X-Rapidapi-Key": rapidapi_key,
        }
        self.rapidapi_host = rapidapi_host

    async def __get_request(self, path: AnyStr, params: Optional[Dict] = None) -> Dict | List:
        """
        :param path: Request path
        :param params: Request query parameters
        :return: JSON Response Dict
        """

        if params:
            query_string = urlencode(params)
        else:
            query_string = ""

        url = URL(
            host=self.rapidapi_host,
            path=path,
            query=query_string,
            scheme="https"
        ).as_string()

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url=url) as response:
                json_response = await response.json()

        results = json_response.get("results")

        return results

    async def reverse_geocode(self, lat: int, lon: int, language: str = "en") -> ReverseGeocodeModel:
        """
        Obtain address for location
        Method: /ReverseGeocode

        :param lat: The location for which you wish to obtain the human-readable address
        :param lon: The location for which you wish to obtain the human-readable address
        :param language: The language in which to return results
        :return: ReverseGeocodeModel object
        """
        path = "/ReverseGeocode"

        response_data = await self.__get_request(
            path=path, params=dict(
                location=f"{lat},{lon}",
                language=language
            )
        )
        data = ReverseGeocodeModel().parse_obj([ReverseGeocodeItem.parse_obj(el) for el in response_data])

        return data
