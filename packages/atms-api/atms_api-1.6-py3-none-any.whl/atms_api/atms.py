import abc
import typing
from inspect import currentframe

import requests
from datetime import datetime, timezone
import re
import os

from xml.etree import ElementTree
# noinspection PyUnresolvedReferences
from xml.dom import minidom

__all__ = ['EventPlanned', 'EventUnplanned', 'EventMedia', 'SignInventory', 'SignStatus',
           'RouteInventory', 'RouteStatus', 'RwisInventory', 'RwisStatus']


county_lookup = {
    'ADAMS': {'cntyCode': 1, 'region': 'NC', 'fips': 55001, 'district': 4, 'regionOffice': 'RAP'},
    'ASHLAND': {'cntyCode': 2, 'region': 'NW', 'fips': 55003, 'district': 8, 'regionOffice': 'SUP'},
    'BARRON': {'cntyCode': 3, 'region': 'NW', 'fips': 55005, 'district': 8, 'regionOffice': 'SUP'},
    'BAYFIELD': {'cntyCode': 4, 'region': 'NW', 'fips': 55007, 'district': 8, 'regionOffice': 'SUP'},
    'BROWN': {'cntyCode': 5, 'region': 'NE', 'fips': 55009, 'district': 3, 'regionOffice': 'GRB'},
    'BUFFALO': {'cntyCode': 6, 'region': 'NW', 'fips': 55011, 'district': 5, 'regionOffice': 'EAU'},
    'BURNETT': {'cntyCode': 7, 'region': 'NW', 'fips': 55013, 'district': 8, 'regionOffice': 'SUP'},
    'CALUMET': {'cntyCode': 8, 'region': 'NE', 'fips': 55015, 'district': 3, 'regionOffice': 'GRB'},
    'CHIPPEWA': {'cntyCode': 9, 'region': 'NW', 'fips': 55017, 'district': 6, 'regionOffice': 'EAU'},
    'CLARK': {'cntyCode': 10, 'region': 'NW', 'fips': 55019, 'district': 6, 'regionOffice': 'EAU'},
    'COLUMBIA': {'cntyCode': 11, 'region': 'SW', 'fips': 55021, 'district': 1, 'regionOffice': 'MAD'},
    'CRAWFORD': {'cntyCode': 12, 'region': 'SW', 'fips': 55023, 'district': 5, 'regionOffice': 'LAC'},
    'DANE': {'cntyCode': 13, 'region': 'SW', 'fips': 55025, 'district': 1, 'regionOffice': 'MAD'},
    'DODGE': {'cntyCode': 14, 'region': 'SW', 'fips': 55027, 'district': 1, 'regionOffice': 'MAD'},
    'DOOR': {'cntyCode': 15, 'region': 'NE', 'fips': 55029, 'district': 3, 'regionOffice': 'GRB'},
    'DOUGLAS': {'cntyCode': 16, 'region': 'NW', 'fips': 55031, 'district': 8, 'regionOffice': 'SUP'},
    'DUNN': {'cntyCode': 17, 'region': 'NW', 'fips': 55033, 'district': 6, 'regionOffice': 'EAU'},
    'EAU CLAIRE': {'cntyCode': 18, 'region': 'NW', 'fips': 55035, 'district': 6, 'regionOffice': 'EAU'},
    'FLORENCE': {'cntyCode': 19, 'region': 'NC', 'fips': 55037, 'district': 7, 'regionOffice': 'RHI'},
    'FOND DU LAC': {'cntyCode': 20, 'region': 'NE', 'fips': 55039, 'district': 2, 'regionOffice': 'GRB'},
    'FOREST': {'cntyCode': 21, 'region': 'NC', 'fips': 55041, 'district': 7, 'regionOffice': 'RHI'},
    'GRANT': {'cntyCode': 22, 'region': 'SW', 'fips': 55043, 'district': 1, 'regionOffice': 'LAC'},
    'GREEN': {'cntyCode': 23, 'region': 'SW', 'fips': 55045, 'district': 1, 'regionOffice': 'MAD'},
    'GREEN LAKE': {'cntyCode': 24, 'region': 'NC', 'fips': 55047, 'district': 4, 'regionOffice': 'RAP'},
    'IOWA': {'cntyCode': 25, 'region': 'SW', 'fips': 55049, 'district': 1, 'regionOffice': 'MAD'},
    'IRON': {'cntyCode': 26, 'region': 'NC', 'fips': 55051, 'district': 7, 'regionOffice': 'RHI'},
    'JACKSON': {'cntyCode': 27, 'region': 'NW', 'fips': 55053, 'district': 5, 'regionOffice': 'EAU'},
    'JEFFERSON': {'cntyCode': 28, 'region': 'SW', 'fips': 55055, 'district': 1, 'regionOffice': 'MAD'},
    'JUNEAU': {'cntyCode': 29, 'region': 'SW', 'fips': 55057, 'district': 4, 'regionOffice': 'LAC'},
    'KENOSHA': {'cntyCode': 30, 'region': 'SE', 'fips': 55059, 'district': 2, 'regionOffice': 'WKE'},
    'KEWAUNEE': {'cntyCode': 31, 'region': 'NE', 'fips': 55061, 'district': 3, 'regionOffice': 'GRB'},
    'LA CROSSE': {'cntyCode': 32, 'region': 'SW', 'fips': 55063, 'district': 5, 'regionOffice': 'LAC'},
    'LAFAYETTE': {'cntyCode': 33, 'region': 'SW', 'fips': 55065, 'district': 1, 'regionOffice': 'MAD'},
    'LANGLADE': {'cntyCode': 34, 'region': 'NC', 'fips': 55067, 'district': 7, 'regionOffice': 'RHI'},
    'LINCOLN': {'cntyCode': 35, 'region': 'NC', 'fips': 55069, 'district': 7, 'regionOffice': 'RHI'},
    'MANITOWOC': {'cntyCode': 36, 'region': 'NE', 'fips': 55071, 'district': 3, 'regionOffice': 'GRB'},
    'MARATHON': {'cntyCode': 37, 'region': 'NC', 'fips': 55073, 'district': 4, 'regionOffice': 'RAP'},
    'MARINETTE': {'cntyCode': 38, 'region': 'NE', 'fips': 55075, 'district': 3, 'regionOffice': 'GRB'},
    'MARQUETTE': {'cntyCode': 39, 'region': 'NC', 'fips': 55077, 'district': 4, 'regionOffice': 'RAP'},
    'MILWAUKEE': {'cntyCode': 40, 'region': 'SE', 'fips': 55079, 'district': 2, 'regionOffice': 'WKE'},
    'MONROE': {'cntyCode': 41, 'region': 'SW', 'fips': 55081, 'district': 5, 'regionOffice': 'LAC'},
    'OCONTO': {'cntyCode': 42, 'region': 'NE', 'fips': 55083, 'district': 3, 'regionOffice': 'GRB'},
    'ONEIDA': {'cntyCode': 43, 'region': 'NC', 'fips': 55085, 'district': 7, 'regionOffice': 'RHI'},
    'OUTAGAMIE': {'cntyCode': 44, 'region': 'NE', 'fips': 55087, 'district': 3, 'regionOffice': 'GRB'},
    'OZAUKEE': {'cntyCode': 45, 'region': 'SE', 'fips': 55089, 'district': 2, 'regionOffice': 'WKE'},
    'PEPIN': {'cntyCode': 46, 'region': 'NW', 'fips': 55091, 'district': 6, 'regionOffice': 'EAU'},
    'PIERCE': {'cntyCode': 47, 'region': 'NW', 'fips': 55093, 'district': 6, 'regionOffice': 'EAU'},
    'POLK': {'cntyCode': 48, 'region': 'NW', 'fips': 55095, 'district': 8, 'regionOffice': 'SUP'},
    'PORTAGE': {'cntyCode': 49, 'region': 'NC', 'fips': 55097, 'district': 4, 'regionOffice': 'RAP'},
    'PRICE': {'cntyCode': 50, 'region': 'NC', 'fips': 55099, 'district': 7, 'regionOffice': 'RHI'},
    'RACINE': {'cntyCode': 51, 'region': 'SE', 'fips': 55101, 'district': 2, 'regionOffice': 'WKE'},
    'RICHLAND': {'cntyCode': 52, 'region': 'SW', 'fips': 55103, 'district': 5, 'regionOffice': 'LAC'},
    'ROCK': {'cntyCode': 53, 'region': 'SW', 'fips': 55105, 'district': 1, 'regionOffice': 'MAD'},
    'RUSK': {'cntyCode': 54, 'region': 'NW', 'fips': 55107, 'district': 8, 'regionOffice': 'SUP'},
    'ST. CROIX': {'cntyCode': 55, 'region': 'NW', 'fips': 55109, 'district': 6, 'regionOffice': 'EAU'},
    'SAUK': {'cntyCode': 56, 'region': 'SW', 'fips': 55111, 'district': 1, 'regionOffice': 'MAD'},
    'SAWYER': {'cntyCode': 57, 'region': 'NW', 'fips': 55113, 'district': 8, 'regionOffice': 'SUP'},
    'SHAWANO': {'cntyCode': 58, 'region': 'NC', 'fips': 55115, 'district': 3, 'regionOffice': 'RHI'},
    'SHEBOYGAN': {'cntyCode': 59, 'region': 'NE', 'fips': 55117, 'district': 3, 'regionOffice': 'GRB'},
    'TAYLOR': {'cntyCode': 60, 'region': 'NW', 'fips': 55119, 'district': 6, 'regionOffice': 'EAU'},
    'TREMPEALEAU': {'cntyCode': 61, 'region': 'NW', 'fips': 55121, 'district': 5, 'regionOffice': 'EAU'},
    'VERNON': {'cntyCode': 62, 'region': 'SW', 'fips': 55123, 'district': 5, 'regionOffice': 'LAC'},
    'VILAS': {'cntyCode': 63, 'region': 'NC', 'fips': 55125, 'district': 7, 'regionOffice': 'RHI'},
    'WALWORTH': {'cntyCode': 64, 'region': 'SE', 'fips': 55127, 'district': 2, 'regionOffice': 'WKE'},
    'WASHBURN': {'cntyCode': 65, 'region': 'NW', 'fips': 55129, 'district': 8, 'regionOffice': 'SUP'},
    'WASHINGTON': {'cntyCode': 66, 'region': 'SE', 'fips': 55131, 'district': 2, 'regionOffice': 'WKE'},
    'WAUKESHA': {'cntyCode': 67, 'region': 'SE', 'fips': 55133, 'district': 2, 'regionOffice': 'WKE'},
    'WAUPACA': {'cntyCode': 68, 'region': 'NC', 'fips': 55135, 'district': 4, 'regionOffice': 'RAP'},
    'WAUSHARA': {'cntyCode': 69, 'region': 'NC', 'fips': 55137, 'district': 4, 'regionOffice': 'RAP'},
    'WINNEBAGO': {'cntyCode': 70, 'region': 'NE', 'fips': 55139, 'district': 3, 'regionOffice': 'GRB'},
    'WOOD': {'cntyCode': 71, 'region': 'NC', 'fips': 55141, 'district': 4, 'regionOffice': 'RAP'},
    'MENOMINEE': {'cntyCode': 73, 'region': 'NC', 'fips': 55078, 'district': 3, 'regionOffice': 'RHI'}

}

#TODO make sql generator for cams and message signs

# noinspection DuplicatedCode
def _dict_keys_lower_case(d: dict):
    return_dict = dict()
    for k, v in d.items():
        return_dict[k.lower()] = v
    return return_dict


def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = str(ElementTree.tostring(elem, 'utf-8'), 'utf-8').replace('xsi:noNamespaceSchemaLocation',
                                                                             'xsinoNamespaceSchemaLocation')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ").replace('xsinoNamespaceSchemaLocation', 'xsi:noNamespaceSchemaLocation')


def _get_org_info(el_name: str, org: str = ' '):
    _org_info = ElementTree.Element(el_name)

    _org_id = ElementTree.Element('organization-id')
    _org_id.text = 'WisDOT'
    _org_info.append(_org_id)

    _org_name = ElementTree.Element('organization-name')
    _org_name.text = 'WisDOT'
    _org_info.append(_org_name)

    _org_center_id = ElementTree.Element('center-id')
    _org_center_id.text = org
    _org_info.append(_org_center_id)

    _org_center_name = ElementTree.Element('center-name')
    _org_center_name.text = org
    _org_info.append(_org_center_name)

    return _org_info


def _el_tag_text(tag_name: str, txt) -> ElementTree.Element:
    the_el = ElementTree.Element(tag_name)
    the_el.text = str(txt)
    return the_el


def _get_time_el(d: datetime, el_name: str):
    _ret_el = ElementTree.Element(el_name)

    _ret_el.append(_el_tag_text('date', d.strftime('%Y%m%d')))
    _ret_el.append(_el_tag_text('time', d.strftime('%H%M%S')))
    _ret_el.append(_el_tag_text('offset', d.strftime('%z')[1:]))

    return _ret_el


class _GeoJson:

    @classmethod
    @abc.abstractmethod
    def get(cls, id_):
        pass

    @classmethod
    def get_geojson(cls, id_: int = None):
        features: typing.List[_GeoJson] = cls.get(id_)
        # cls.
        # features: typing.List[_GeoJson] = cls.__dict__['get'](id_)

        return {
            "type": "FeatureCollection",
            "crs": {
                'type': 'name',
                'properties': {
                    'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'
                }
            },
            "features": [f.geojson for f in features]
        }

    @property
    @abc.abstractmethod
    def geojson(self):
        return {
            'type': 'Feature',
            'geometry': {
                'type': '',
                'coordinates': [],
            },
            'properties': self.json
        }

    @property
    @abc.abstractmethod
    def json(self):
        pass


class Atms:
    url: str = None
    token: str = None

    _url_all = None
    _url_by_id = None

    @classmethod
    @abc.abstractmethod
    def get(cls, id_: int = None) -> typing.List:
        if cls == Atms:
            raise NotImplementedError("Cannot call 'get' on base class")

        if Atms.url is None:
            raise ValueError("'url' value of Atms class must be set")

        if Atms.token is None:
            raise ValueError("'token' value of Atms class must be set")

        if id_ is not None:
            request_url = cls.url + cls._url_by_id.format(id=id_)
        else:
            request_url = cls.url + cls._url_all

        response = requests.get(
            request_url,
            headers={
                'Accept': 'application/json',
                'token': cls.token
            }
        )

        if response.status_code == 401:
            raise ValueError('Unauthorized - token not valid')
        elif response.status_code == 404:
            raise ValueError('404 {0}'.format(request_url))

        if not response.status_code == 200:
            raise ValueError('unknown error - non 200 status code')

        json_response = response.json()

        if id_ is not None:
            json_response = [json_response]

        ret = []

        for r in json_response:
            dta = _dict_keys_lower_case(r)
            if 'id' not in dta.keys():
                dta['id'] = -1
            ret.append(cls(dta))

        return ret

    def __init__(self, data: dict):
        self._id = data['id']

    @property
    def id(self):
        return self._id

    @property
    def json(self):
        return {
            'id': self.id
        }

    @property
    def xml_el(self):
        raise NotImplementedError


class _Location:

    @staticmethod
    def geom_from_two_locations(loc1: '_Location', loc2: '_Location'):
        loc1_valid = loc1.latitude is not None and loc1.latitude != 0 and \
                     loc1.longitude is not None and loc1.longitude != 0

        loc2_valid = \
            loc2.latitude is not None and loc2.latitude != 0 and loc2.longitude is not None and loc2.longitude != 0

        if loc1_valid and loc2_valid:
            if loc1.latitude == loc2.latitude and loc1.longitude == loc2.longitude:
                return {
                    "type": "Point",
                    "coordinates": [loc1.longitude, loc1.latitude]
                }
            else:
                return {
                    "type": "MultiPoint",
                    "coordinates": [
                        [loc1.longitude, loc1.latitude],
                        [loc2.longitude, loc2.latitude]
                    ]
                }
        if loc1_valid and not loc2_valid:
            return {
                "type": "Point",
                "coordinates": [loc1.longitude, loc1.latitude]
            }
        if not loc1_valid and loc2_valid:
            return {
                "type": "Point",
                "coordinates": [loc2.longitude, loc2.latitude]
            }
        if not loc1_valid and not loc2_valid:
            return None

    def __init__(self, data: dict):
        dta = {} if data is None else _dict_keys_lower_case(data)

        self.roadway_name: str = dta.get('roadwayname', None)
        self.direction: str = dta.get('direction', None)
        self.longitude: str = dta.get('longitude', None)
        self.latitude: str = dta.get('latitude', None)
        self.county: str = dta.get('county', None)

    @property
    def json(self) -> dict:
        return {
            "roadwayName": self.roadway_name,
            "direction": self.direction,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "county": self.county,
        }


def _parse_date(date_str: str) -> datetime or None:
    if date_str is None:
        return None
    else:
        return datetime.fromisoformat(
            re.sub('Z$', '+00:00', date_str)
        ).replace(tzinfo=timezone.utc).astimezone(tz=None)


class _EventBase(Atms, _GeoJson):

    def __init__(self, data: dict):
        super().__init__(data)
        # print(data)
        self._description: str = data['description']
        self._head_location: _Location = _Location(data['headlocation'])
        self._tail_location: _Location = _Location(data['taillocation'])
        self._type: str = data['type']
        self._cause: str = data['cause']
        self._severity: str = data['severity']
        self._lane_pattern: str = data['lanepattern']
        self._lane_status: str = data['lanestatus']
        self._detour_route_id: str = data['detourrouteid']
        self._detour_route: str = data['detourroute']
        self._last_updated: datetime = _parse_date(data['lastupdated'])
        self._isCleared: bool = data['iscleared']
        self._isFloodgate: bool = data['isfloodgate']
        self._sourceEventId: str = data['sourceeventid']
        self._estimatedDurationHours: int = data['estimateddurationhours']

    @classmethod
    @abc.abstractmethod
    def get(cls, id_=None):
        response_data = super().get(id_)
        return response_data

    @property
    def lanes_affected(self):
        lanes = 0
        for i in range(len(self._lane_pattern)):
            if self._lane_pattern[i] == 'T' and self._lane_status[i] == 'X':
                lanes += 1

        return lanes

    @property
    def json(self):
        ret = super().json

        ret['description'] = self._description
        ret['headLocation'] = self._head_location.json
        ret['tailLocation'] = self._head_location.json
        ret['type'] = self._type
        ret['cause'] = self._cause
        ret['severity'] = self._severity
        ret['lanePattern'] = self._lane_pattern
        ret['laneStatus'] = self._lane_status
        ret['detourRouteId'] = self._detour_route_id
        ret['detourRoute'] = self._detour_route
        ret['lastUpdated'] = self._last_updated.isoformat()
        ret['isCleared'] = self._isCleared
        ret['isFloodgate'] = self._isFloodgate
        ret['sourceEventId'] = self._sourceEventId
        ret['estimatedDurationHours'] = self._estimatedDurationHours

        return ret

    @property
    def geojson(self):
        geo = super().geojson
        geo['geometry'] = _Location.geom_from_two_locations(self._head_location, self._tail_location)

        return geo


class EventUnplanned(_EventBase):
    _url_all = '/api/UnplannedEvents'
    _url_by_id = '/api/UnplannedEvents/{id}'

    @classmethod
    def get(cls, id_=None) -> typing.List['EventUnplanned']:
        return super().get(id_)

    def __init__(self, data: dict):
        super().__init__(data)
        self._is_cleared: bool = data['iscleared']

        print(data)

    @property
    def json(self):
        ret = super().json
        ret['isCleared'] = self._is_cleared
        return ret

    @property
    def xml_el(self):
        # print(self.id)
        # print(json.dumps(self.json, indent=4))

        # print(self._head_location.county.upper())

        # print(county_lookup.get(self._head_location.county.upper(), None))

        lk = county_lookup.get(self._head_location.county.upper(), None)

        county_fips = str(0 if lk is None else lk['fips'])
        org = "none" if lk is None else lk['regionOffice']

        # print(county_fips)

        el = ElementTree.Element('fullEventUpdate')

        header = ElementTree.Element('message-header')
        header.append(_get_org_info('organization-sending', org))
        header.append(_el_tag_text('message-type-id', 'FEU'))
        header.append(_el_tag_text('message-type-version', '1'))
        header.append(_el_tag_text('message-number', '1'))
        header.append(_get_time_el(self._last_updated, 'message-time-stamp'))
        el.append(header)

        event_ref = ElementTree.Element('event-reference')
        event_ref.append(_el_tag_text('event-id', self.id))
        event_ref.append(_el_tag_text('event-update', 1))
        el.append(event_ref)

        # print(self._type)
        # print(self._cause)
        # print(self._description)
        # print(self._lane_pattern)
        # print(self._lane_status)

        event_indicators = ElementTree.Element('event-indicators')
        event_indicator = ElementTree.Element('event-indicator')
        event_indicator.append(_el_tag_text('status', 'current'))
        event_indicators.append(event_indicator)
        el.append(event_indicators)

        accidents_and_incidents = self._cause.lower()

        if accidents_and_incidents == 'crash':
            accidents_and_incidents = 'accident'

        event_headline = ElementTree.Element('event-headline')
        headline = ElementTree.Element('headline')
        headline.append(_el_tag_text('accidentsAndIncidents', accidents_and_incidents))
        event_headline.append(headline)
        el.append(event_headline)

        event_element_details = ElementTree.Element('event-element-details')
        event_element_detail = ElementTree.Element('event-element-detail')
        element_descriptions = ElementTree.Element('element-descriptions')

        element_description1 = ElementTree.Element('element-description')
        phrase1 = ElementTree.Element('phrase')
        phrase1.append(_el_tag_text('accidentsAndIncidents', self._description))
        element_description1.append(phrase1)
        element_descriptions.append(element_description1)

        element_description2 = ElementTree.Element('element-description')
        descrip1 = ElementTree.Element('additional-text')
        descrip1.append(_el_tag_text('description',accidents_and_incidents))
        element_description2.append(descrip1)
        element_descriptions.append(element_description2)

        event_element_detail.append(element_descriptions)

        element_locations = ElementTree.Element('element-locations')
        element_location = ElementTree.Element('element-location')
        location_on_link = ElementTree.Element('location-on-link')
        location_on_link.append(_el_tag_text('link-ownership', 'WisDOT'))

        location_on_link.append(
            _el_tag_text(
                'link-designator',
                self._head_location.roadway_name[:self._head_location.roadway_name.find(' ')])
        )

        primary_location = ElementTree.Element('primary-location')

        geo_location = ElementTree.Element('geo-location')
        geo_location.append(_el_tag_text('latitude', str(self._head_location.latitude).replace('.', '')[:8]))
        geo_location.append(_el_tag_text('longitude', str(self._head_location.longitude).replace('.', '')[:9]))
        primary_location.append(geo_location)

        primary_location.append(_el_tag_text('link-name', self._head_location.roadway_name))

        upward_area_reference = ElementTree.Element('upward-area-reference')
        #TODO upward are reference is the fipscode
        upward_area_reference.append(_el_tag_text('area-id', county_fips))
        upward_area_reference.append(_el_tag_text('area-name', self._head_location.county.upper()))

        primary_location.append(upward_area_reference)

        location_on_link.append(primary_location)

        if self._tail_location.latitude is not None and self._tail_location.longitude is not None:
            secondary_location = ElementTree.Element('secondary-location')
            geo_location2 = ElementTree.Element('geo-location')
            geo_location2.append(_el_tag_text('latitude', str(self._tail_location.latitude).replace('.', '')[:8]))
            geo_location2.append(_el_tag_text('longitude', str(self._tail_location.longitude).replace('.', '')[:9]))
            secondary_location.append(geo_location2)
            secondary_location.append(_el_tag_text('link-name', self._tail_location.roadway_name))
            location_on_link.append(secondary_location)

        try:
            location_on_link.append(_el_tag_text('link-direction', self._head_location.direction.lower()))
        except AttributeError:
            location_on_link.append(_el_tag_text('link-direction', ''))

        element_location.append(location_on_link)
        element_locations.append(element_location)
        event_element_detail.append(element_locations)

        element_times = ElementTree.Element('element-times')
        element_times.append(_get_time_el(self._last_updated, 'update-time'))

        valid_period = ElementTree.Element('valid-period')
        valid_period.append(
            _el_tag_text(
                'estimated-duration',
                0 if self._estimatedDurationHours is None else self._estimatedDurationHours)
        )
        element_times.append(valid_period)
        event_element_detail.append(element_times)

        element_lanes = ElementTree.Element('element-lanes')
        element_lanes.append(_el_tag_text('lanes-total-affected', self.lanes_affected))

        event_element_detail.append(element_lanes)

        event_element_details.append(event_element_detail)
        el.append(event_element_details)

        return el


class EventPlanned(_EventBase):
    _url_all = '/api/PlannedEvents'
    _url_by_id = '/api/PlannedEvents/{id}'

    @classmethod
    def get(cls, id_=None) -> typing.List['EventPlanned']:
        return super().get(id_)

    def __init__(self, data: dict):
        super().__init__(data)
        self._is_active: bool = data['isactive']
        self._schedule_start: datetime = _parse_date(data['schedulestart'])
        self._schedule_end: datetime = _parse_date(data['scheduleend'])
        self._repeating: bool = data['repeating']
        self._occurrence_end: datetime = _parse_date(data['occurrenceend'])
        self._source_event_id = data['sourceeventid']

    @property
    def json(self):
        ret = super().json
        ret['isActive'] = self._is_active
        ret['scheduleStart'] = None if self._schedule_start is None else self._schedule_start.isoformat()
        ret['scheduleEnd'] = None if self._schedule_end is None else self._schedule_end.isoformat()
        ret['repeating'] = self._repeating
        ret['occurrenceEnd'] = None if self._occurrence_end is None else self._occurrence_end.isoformat()
        ret['sourceEventId'] = self._source_event_id

        return ret

    @property
    def xml_el(self):
        # print(self.id)
        # print(json.dumps(self.json, indent=4))

        el = ElementTree.Element('fullEventUpdate')

        return el


class EventMedia(Atms):
    _url_all = '/api/UnplannedEvents/EventMedia'
    _url_by_id = '/api/UnplannedEvents/{id}/EventMedia'

    @classmethod
    def get(cls, id_=None) -> typing.List['EventMedia']:
        return super().get(id_)

    def __init__(self, data: dict):
        super().__init__(data)
        self._event_id = data['eventid']
        self._publish_social_media: bool = data['publishsocialmedia']
        self._publish_on_511: bool = data['publishon511']

    @property
    def json(self):
        return {
            'eventId': self._event_id,
            'publishSocialMedia': self._publish_social_media,
            'publishOn511': self._publish_on_511
        }

    @property
    def xml_el(self):
        return super().xml_el


class SignInventory(Atms, _GeoJson):
    _url_all = '/api/Signs'
    _url_by_id = '/api/Signs/{id}'

    @classmethod
    def get(cls, id_=None) -> typing.List['SignInventory']:
        return super().get(id_)

    def __init__(self, data: dict):
        super().__init__(data)
        self._description = data['description']
        self._location = _Location(data['location'])

    @property
    def json(self):
        ret = super().json

        ret['description'] = self._description
        ret['location'] = self._location.json

        # ret['geometry']['coordinates'] = [self._location.longitude, self._location.latitude]

        return ret

    @property
    def geojson(self):
        geo = super().geojson
        geo['geometry']['type'] = 'Point'
        geo['geometry']['coordinates'] = [self._location.longitude, self._location.latitude]

        return geo

    @property
    def xml_el(self):
        return super().xml_el


# noinspection DuplicatedCode
class SignStatus(Atms):
    _url_all = '/api/Signs/Statuses'
    _url_by_id = '/api/Signs/{id}/Status'

    @classmethod
    def get(cls, id_=None) -> typing.List['SignStatus']:
        return super().get(id_)

    def __init__(self, data: dict):
        super().__init__(data)
        self._status: str = data['status']
        self._message: str = data['message']
        self._phase_time: int = data['phasetime']
        self._last_updated: datetime = _parse_date(data['lastupdated'])
        self._is_bit_map: bool = data['isbitmap']
        self._bitmap_base64_strings: str = data['bitmapbase64strings']

    @property
    def json(self):
        ret = super().json

        ret['status'] = self._status
        ret['message'] = self._message
        ret['phaseTime'] = self._phase_time
        ret['lastUpdated'] = self._last_updated.isoformat()
        ret['isBitMap'] = self._is_bit_map
        ret['bitmapBase64Strings'] = self._bitmap_base64_strings

        return ret

    @property
    def xml_el(self):
        el = ElementTree.Element('dMSDeviceStatus')

        el.append(_get_org_info('organization-information'))
        el.append(_el_tag_text('operator-id', 'DEFAULT'))
        el.append(_el_tag_text('device-id', self.id))

        """
                    on (1)
            off (2)
            in service (3)
            out of service (4)
            unavailable (5)
            unknown (6)
        """

        """
        •	Ok
•	Not Communicating
•	Unknown
•	Not in Service

        """

        if self._status == 'Ok':
            stat_int = 3
        elif self._status in ('Not Communicating', 'Unknown', 'Device Error'):
            stat_int = 6
        elif self._status == 'Not in Service':
            stat_int = 4
        else:
            raise ValueError("sign status match not found: {0}".format(self._status))

        el.append(_el_tag_text('dms-device-status', stat_int))
        el.append(_el_tag_text('dms-current-message', self._message))
        el.append(_get_time_el(self._last_updated, 'last-comm-time'))

        return el

    @property
    def message(self):
        return self._message

    @property
    def last_updated(self):
        return self._last_updated


class CameraInventory(Atms, _GeoJson):
    _url_all = '/api/CCTV'
    _url_by_id = '/api/CCTV/{id}'

    @classmethod
    def get(cls, id_=None) -> typing.List['CameraInventory']:
        return super().get(id_)

    def __init__(self, data: dict):
        super().__init__(data)
        self._description = data['description']
        self._image_url = data['imageurl']
        self._location = _Location(data['location'])

    @property
    def json(self):
        ret = super().json

        ret['description'] = self._description
        ret['imageUrl'] = self._image_url
        ret['location'] = self._location.json

        # ret['geometry']['coordinates'] = [self._location.longitude, self._location.latitude]

        return ret

    @property
    def geojson(self):
        geo = super().geojson
        geo['geometry']['type'] = 'Point'
        geo['geometry']['coordinates'] = [self._location.longitude, self._location.latitude]

        return geo

    @property
    def xml_el(self):
        return super().xml_el


class RouteInventory(Atms):
    _url_all = '/api/Routes'
    _url_by_id = '/api/Routes/{id}'

    @classmethod
    def get(cls, id_=None) -> typing.List['RouteInventory']:
        return super().get(id_)

    def __init__(self, data: dict):
        self._name: str = data['name']
        self._routeLength: float = float(data['routelength'])
        self._free_flow_travel_time: int = data['freeflowtraveltime']
        self._start_location: _Location = _Location(data['startlocation'])
        self._end_location: _Location = _Location(data['endlocation'])
        self._waypoints: typing.List[_Location] = [_Location(ll) for ll in data['waypoints']]
        super().__init__(data)

    @property
    def json(self):
        ret = super().json
        ret['name'] = self._name
        ret['freeFlowTravelTime'] = self._free_flow_travel_time
        ret['routeLength'] = self._routeLength
        ret['startLocation'] = self._start_location.json
        ret['endLocation'] = self._end_location.json
        ret['waypoints'] = [w.json for w in self._waypoints]

        return ret

    @property
    def free_flow(self):
        return self._free_flow_travel_time

    @property
    def route_length(self):
        return self._routeLength

    @property
    def xml_el(self):
        return super().xml_el


class RouteStatus(Atms):

    _url_all = '/api/Routes/Statuses'
    _url_by_id = '/api/Routes/{id}/Status'

    @classmethod
    def get(cls, id_=None) -> typing.List['RouteStatus']:
        return super().get(id_)

    def __init__(self, data: dict):
        super().__init__(data)

        self._calculated_tt: int = data['calculatedtt']
        self._displayed_tt: int = data['displayedtt']
        self._interval_start: datetime = _parse_date(data['intervalstart'])
        self._interval_end: datetime = _parse_date(data['intervalend'])

        self._min_tt = -1
        self._nom_tt = -1
        self._max_tt = -1

        self._rte_len = -1

    @property
    def json(self):
        ret = super().json
        ret['calculatedTt'] = self._calculated_tt
        ret['displayedTt'] = self._displayed_tt
        ret['intervalStart'] = self._interval_start.isoformat()
        ret['intervalEnd'] = self._interval_end.isoformat()

        return ret

    def set_min_nom_max(self, min_tt, nom_tt, max_tt):
        self._min_tt = min_tt
        self._nom_tt = nom_tt
        self._max_tt = max_tt

    def set_route_len(self, rte_len):
        self._rte_len = int(rte_len)

    @property
    def xml_el(self):
        el = ElementTree.Element('routeData')

        el.append(_get_org_info('organization-information'))
        el.append(_el_tag_text('route-id', self.id))
        el.append(_el_tag_text('route-status', '1'))

        if self._rte_len > -1:
            el.append(_el_tag_text('total-distance', int(self._rte_len)))

        el.append(_el_tag_text('display-travel-time', self._displayed_tt))
        el.append(_el_tag_text('calculated-travel-time', self._calculated_tt))

        if self._min_tt != -1:
            el.append(_el_tag_text('minimum-travel-time', self._min_tt))

        if self._nom_tt != -1:
            el.append(_el_tag_text('nominal-travel-time', self._nom_tt))

            delay_num = self._calculated_tt - self._nom_tt
            delay_num = 0 if delay_num < 0 else delay_num
            el.append(_el_tag_text('delay', delay_num))

        if self._max_tt != -1:
            el.append(_el_tag_text('maximum-travel-time', self._max_tt))

        el.append(_get_time_el(self._interval_end, 'last-update-time'))
        return el


class RwisInventory(Atms):
    _url_all = '/api/RWIS'
    _url_by_id = '/api/RWIS/{id}'

    @classmethod
    def get(cls, id_=None) -> typing.List['RwisInventory']:
        return super().get(id_)

    def __init__(self, data: dict):
        super().__init__(data)

        self._description: str = data['description']
        self._latitude: float = data['latitude']
        self._longitude: float = data['longitude']
        self._measurements = data['measurements']

    @property
    def json(self):
        ret = super().json

        return ret

    @property
    def xml_el(self):
        return super().xml_el


class RwisStatus(Atms):
    _url_all = '/api/RWIS/Statuses'
    _url_by_id = '/api/RWIS/{id}/Status'

    @classmethod
    def get(cls, id_=None) -> typing.List['RwisStatus']:
        return super().get(id_)

    def __init__(self, data: dict):
        super().__init__(data)

        self._status: int = data['status']
        self._current_measurements = data['currentmeasurements']
        self._last_updated = _parse_date(data['lastupdated'])

    @property
    def json(self):
        ret = super().json

        return ret

    @property
    def xml_el(self):
        return super().xml_el


def printd(*args):
    """
    Helper print command to provide an easy link to the line where the print statement occurs
    Can easily navigate to the location using many IDEs

    :param args: same as with default 'print' statement
    :return:
    """
    enclosing_frame = currentframe().f_back

    """
    Line number get found at
    http://code.activestate.com/recipes/145297-grabbing-the-current-line-number-easily/
    """
    line_num = enclosing_frame.f_lineno

    working_path = os.getcwd()

    file_dir = os.path.dirname(enclosing_frame.f_code.co_filename)
    file_name = os.path.basename(enclosing_frame.f_code.co_filename)

    common_prefix = os.path.commonprefix([working_path, file_dir])

    pth = os.path.join(file_dir, file_name)

    if len(common_prefix) > 0:
        working_path = working_path.replace(common_prefix, '')
        file_path = file_dir.replace(common_prefix, '')

        path_parts = working_path.split(os.sep)
        file_parts = file_path.split(os.sep)

        if len(file_parts) >= len(path_parts):
            file_parts.append(file_name)
            pth = os.path.join(*file_parts)
        else:
            pth_list = []
            for i in range(len(path_parts) - len(file_parts)):
                pth_list.append(os.pardir)

            pth_list.append(file_name)

            pth = os.path.join(*pth_list)

    print("{0}:{1}".format(pth, line_num), *args)
