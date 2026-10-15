import logging
from urllib.parse import urlencode

from django.core.cache import cache
from decouple import config

import requests

logger = logging.getLogger(__name__)

API_BASE = "https://us1.locationiq.com/v1"
MAP_BASE = "https://maps.locationiq.com/v3/staticmap"
REQUEST_TIMEOUT = 10

FACILITY_TAGS = {
    'hospital': 'amenity:hospital',
    'clinic': 'amenity:clinic',
    'pharmacy': 'amenity:pharmacy',
}

FACILITY_LABELS = {
    'hospital': 'Hospital',
    'clinic': 'Clinic',
    'pharmacy': 'Pharmacy',
}

_FACILITY_BADGE = {
    'hospital': 'danger',
    'clinic': 'info',
    'pharmacy': 'success',
}

_MAP_COLOR = {
    'hospital': 'red',
    'clinic': 'blue',
    'pharmacy': 'green',
}


def get_api_key():
    return config('LOCATIONIQ_API_KEY', default='').strip()


def is_configured():
    return bool(get_api_key())


def geocode_address(address):
    """Convert an address string to lat/lon using LocationIQ forward geocoding."""
    if not address:
        return None

    cache_key = 'locationiq_geocode:' + address.lower().strip()
    cached = cache.get(cache_key)
    if cached:
        return cached

    api_key = get_api_key()
    if not api_key:
        return None

    try:
        response = requests.get(
            API_BASE + '/search',
            params={
                'key': api_key,
                'q': address,
                'format': 'json',
                'addressdetails': 1,
                'limit': 1,
            },
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        if data and isinstance(data, list) and len(data) > 0:
            result = data[0]
            location = {
                'lat': float(result['lat']),
                'lon': float(result['lon']),
                'display_name': result.get('display_name', address),
            }
            cache.set(cache_key, location, timeout=86400)
            return location
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else None
        if status == 429:
            logger.warning('LocationIQ rate limit exceeded (geocode)')
        else:
            logger.warning('LocationIQ geocode HTTP error: %s', e)
    except Exception as e:
        logger.warning('LocationIQ geocode error: %s', e)

    return None


def search_nearby_places(lat, lon, tag, radius=5000):
    """Search for nearby places using LocationIQ Nearby API."""
    api_key = get_api_key()
    if not api_key:
        return []

    try:
        response = requests.get(
            API_BASE + '/nearby',
            params={
                'key': api_key,
                'lat': lat,
                'lon': lon,
                'tag': tag,
                'radius': radius,
                'format': 'json',
            },
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, list):
            return []

        results = []
        for item in data:
            facility_type = item.get('type', '')
            results.append({
                'place_id': item.get('place_id'),
                'name': item.get('name') or item.get('display_name', 'Unknown'),
                'display_name': item.get('display_name', ''),
                'lat': float(item.get('lat', 0)),
                'lon': float(item.get('lon', 0)),
                'address': item.get('address', {}) or {},
                'distance': float(item.get('distance', 0)),
                'distance_km': round(float(item.get('distance', 0)) / 1000, 2),
                'class': item.get('class', ''),
                'type': facility_type,
                'type_label': FACILITY_LABELS.get(facility_type, (facility_type or 'unknown').title()),
                'badge_class': _FACILITY_BADGE.get(facility_type, 'secondary'),
            })
        return results
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else None
        if status == 429:
            logger.warning('LocationIQ rate limit exceeded (nearby)')
        else:
            logger.warning('LocationIQ nearby HTTP error: %s', e)
    except Exception as e:
        logger.warning('LocationIQ nearby search error: %s', e)

    return []


def get_nearby_facilities(lat, lon, facility_type='all', radius=5000):
    """Search for nearby medical facilities. Returns results sorted by distance."""
    if facility_type == 'all':
        tags = list(FACILITY_TAGS.values())
    else:
        tags = [FACILITY_TAGS.get(facility_type, FACILITY_TAGS['hospital'])]

    all_results = []
    for tag in tags:
        all_results.extend(search_nearby_places(lat, lon, tag, radius))

    all_results.sort(key=lambda x: x['distance'])
    return all_results


def build_map_url(center_lat, center_lon, facilities, max_markers=10):
    """Build a LocationIQ static map URL with markers for the center and facilities."""
    api_key = get_api_key()
    if not api_key:
        return None

    params = [
        ('key', api_key),
        ('center', '{},{}'.format(center_lat, center_lon)),
        ('zoom', 13),
        ('size', '800x400'),
        ('format', 'png'),
        ('maptype', 'streets'),
    ]

    params.append(('markers', 'icon:large-blue-dot|{},{}'.format(center_lat, center_lon)))

    for facility in facilities[:max_markers]:
        color = _MAP_COLOR.get(facility['type'], 'red')
        params.append((
            'markers',
            'icon:large-{}-dot|{},{}'.format(color, facility['lat'], facility['lon']),
        ))

    return MAP_BASE + '?' + urlencode(params)
