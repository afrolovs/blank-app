import requests

GIS_IMAGE_URL = "https://static.maps.2gis.com/1.0?s=1280x1280@2x&z=17&pt="


def get_coords_by_address(address: str) -> list:
    """
    Получаем координаты по адресу через OpenStreetMap
    """
    base_url = "https://nominatim.openstreetmap.org/search"

    params = {"q": address, "format": "json", "limit": 1, "accept-language": "ru"}

    headers = {"User-Agent": "StreamlitApp/1.0"}  # Требуется Nominatim

    response = requests.get(base_url, params=params, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()

    first_result = data[0]
    lat = float(first_result["lat"])
    lon = float(first_result["lon"])

    return f"{lat},{lon}"
