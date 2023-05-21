"""Simple reader that reads weather data from OpenWeatherMap API"""
from typing import Any, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class WeatherReader(BaseReader):
    """Weather Reader.

    Reads the forecast & current weather of any location using OpenWeatherMap's free API.

    Check 'https://openweathermap.org/appid' \
        on how to generate a free OpenWeatherMap API, It's free.

    Args:
        token (str): bearer_token that you get from OWM API.
    """

    def __init__(
        self,
        token: str,
    ) -> None:
        """Initialize with parameters."""
        super().__init__()
        self.token = token

    def load_data(
        self, 
        places: List[str], 
    ) -> List[Document]:
        
        """Load weather data for the given locations. 
        OWM's One Call API provides the following weather data for any geographical coordinate:
        - Current weather
        - Hourly forecast for 48 hours
        - Daily forecast for 7 days

        Args:
            places (List[str]) - places you want the weather data for.
        """

        try:
            import pyowm
        except:
            print('install pyowm using `pip install pyowm`')

        owm = pyowm.OWM(api_key=self.token)
        mgr = owm.weather_manager()

        reg = owm.city_id_registry()

        
        results = []
        for place in places:
            info_dict = {}
            list_of_locations = reg.locations_for(city_name=place)
            city = list_of_locations[0]
            lat = city.lat
            lon = city.lon
    
            res = mgr.one_call(lat=lat,lon=lon)
            
            info_dict['location'] = place
            info_dict['latitude'] = res.lat
            info_dict['longitude'] = res.lon
            info_dict['timezone'] = res.timezone
            info_dict['current weather'] = res.current.to_dict()
            info_dict['daily forecast'] = [i.to_dict() for i in res.forecast_daily]
            info_dict['hourly forecast'] = [i.to_dict() for i in res.forecast_hourly]
            info_dict['minutely forecast'] = [i.to_dict() for i in res.forecast_minutely]
            if res.national_weather_alerts:
                info_dict['national weather alerts'] = [i.to_dict() for i in res.national_weather_alerts]
            
            results.append(Document(info_dict))

        return results