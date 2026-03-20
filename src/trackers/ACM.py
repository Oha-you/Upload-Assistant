# Upload Assistant © 2025 Audionut & wastaken7 — Licensed under UAPL v1.0
from typing import Any, Optional

import cli_ui

from src.console import console
from src.get_desc import DescriptionBuilder
from src.trackers.COMMON import COMMON
from src.trackers.UNIT3D import UNIT3D

Meta = dict[str, Any]
Config = dict[str, Any]


class ACM(UNIT3D):
    def __init__(self, config: Config) -> None:
        super().__init__(config, tracker_name='ACM')
        self.config = config
        self.common = COMMON(config)

        self.common.unit3d_region_map = {
            'KOR': 1, 'CHN': 2, 'JPN': 3, 'TWN': 4, 'SGP': 5, 'PHI': 6, 'THA': 7, 'VIE': 8, 'MAS': 9, 'IDN': 10, 'CAM': 11, 'LAO': 12, 'HKG': 13, 'USA': 14, 'GBR': 15, 'ESP': 16, 'GER': 17, 'FRA': 18, 'EUR': 19, 'MEX': 20, 'AUS': 21, 'IND': 22, 'RUS': 23, 'AUT': 24
        }

        self.common.unit3d_additional_distributors = {
            'ABC STUDIOS': 966, 'ABC': 966, 'ADV FILMS': 967, 'ADV': 967, 'ARTHAUS': 968, 'ARTSMAGIC': 969, 'ARTS MAGIC': 969, 'BANDAI ENTERTAINMENT': 970, 'BANDAI': 970, 'CANADIAN INTERNATIONAL PICTURES': 971, 'CANADIAN INTERNATIONAL': 971, 'CELLULOID DREAMS': 972, 'CELLULOID': 972, 'CENTRAL PARK MEDIA': 973, 'CENTRAL PARK': 973, 'CHAMELEON FILMS': 974, 'CHAMELEON': 974, 'CHANNEL ONE': 975, 'CHIMERA ENTERTAINMENT': 976, 'CHIMERA': 976, 'CINÉMATOGRAPHE': 977, 'CINEMATOGRAPHE': 977, 'CRUNCHYROLL, LLC': 978, 'CRUNCHYROLL LLC': 978, 'CRUNCHYROLL': 978, 'DARK STAR PICTURES': 979, 'DARK STAR': 979, 'DARKSTAR': 979, 'DECAL RELEASING': 980, 'DECAL': 980, 'ERROR 4444': 981, 'ERROR4444': 981, 'FACTORY25': 982, 'FACTORY 25': 982, 'GABITA BARBIERI FILMS': 983, 'GABITA BARBIERI': 983, 'INDICATOR': 984, 'JANSON MEDIA': 985, 'JANSON': 985, 'JOY SALES': 986, 'JOYSALES': 986, 'JOY': 986, 'LEVEL 33 ENTERTAINMENT': 987, 'LEVEL 33': 987, 'LEVEL33': 987, 'LOST TIME MEDIA': 988, 'LOST TIME': 988, 'LOSTTIME': 988, 'MELUSINE': 989, 'PANIK HOUSE': 990, 'PANIK': 990, 'PIONEER': 991, 'PLAION': 992, 'RADIANCE FILMS': 993, 'RADIANCE': 993, 'RENTRAK': 994, 'SAMURAIDVD': 995, 'SAMURAI': 995, 'SATURN\'S CORE AUDIO & VIDEO': 996, 'SATURN\'S CORE': 996, 'TERROR VISION': 997, 'TERROR': 997, 'U.S. MANGA CORPS': 998, 'US MANGA CORPS': 998, 'U.S. MANGA': 998, 'US MANGA': 998, 'URBAN VISION': 999, 'URBAN': 999, 'UTOPIA DISTRIBUTION': 1000, 'UTOPIA': 1000, 'WARNER ARCHIVE COLLECTION': 1001, 'WARNER ARCHIVE': 1001, 'WHOLE GRAIN PICTURES': 1002, 'WHOLE GRAIN': 1002, 'AFILM': 1003, 'DEAF CROCODILE': 1004
        }

        self.tracker = 'ACM'
        self.base_url = 'https://eiga.moi'
        self.id_url = f'{self.base_url}/api/torrents/'
        self.upload_url = f'{self.base_url}/api/torrents/upload'
        self.requests_url = f'{self.base_url}/api/requests/filter'
        self.search_url = f'{self.base_url}/api/torrents/filter'
        self.torrent_url = f'{self.base_url}/torrents/'
        self.banned_groups = ['']
        pass

    async def get_type_id(
        self,
        meta: Meta,
        type: Optional[str] = None,
        reverse: bool = False,
        mapping_only: bool = False
    ) -> dict[str, str]:
        type_id = {
            'DISC': '1',
            'REMUX': '7',
            'WEBDL': '9',
            'WEBRIP': '13',
            'SDTV': '13',
            'HDTV': '17',
            'UHDTV': '19',
            'ENCODE': '13',
            'DVDRIP': '13'
        }
        if mapping_only:
            return type_id
        elif reverse:
            return {v: k for k, v in type_id.items()}
        elif type:
            return {'type_id': type_id.get(type, '1')}
        else:
            meta_type = meta.get('type', '')
            resolved_id = type_id.get(meta_type, '1')

            if meta_type not in ['DISC', 'REMUX', 'WEBDL']:
                if meta.get('uhd') == 'UHD' or meta.get('source') == 'UHDTV':
                    resolved_id = '19' # UHDTV type
                if meta.get('sd') == 1:
                    resolved_id = '13' # SDTV type

            return {'type_id': resolved_id}

    async def get_resolution_id(self,
        meta: Meta,
        resolution: Optional[str] = None,
        reverse: bool = False,
        mapping_only: bool = False
    ) -> dict[str, str]:
        resolution_id = {
            'OTHER': '6', # needs to be uppercase for request searching
            '8640p': '6', # map all non-existent resolutions to Other
            '4320p': '6',
            '2160p': '1',
            '1440p': '6',
            '1080p': '2',
            '1080i': '2',
            '720p': '3',
            '576p': '4',
            '576i': '4',
            '480p': '5',
            '480i': '5',
        }
        if mapping_only:
            return resolution_id
        elif reverse:
            return {v: k for k, v in resolution_id.items()}
        elif resolution:
            return {'resolution_id': resolution_id.get(resolution, '6')}
        else:
            meta_resolution = meta.get('resolution', '')
            resolved_id = resolution_id.get(meta_resolution, '6')
            return {'resolution_id': resolved_id}

    async def get_additional_checks(self, meta: Meta) -> bool:
        if (
            meta.get('type') in ['WEBRIP', 'ENCODE', 'DVDRIP']
            and (not meta.get('unattended') or (meta.get('unattended') and meta.get('unattended_confirm')))
        ):
            console.print('[bold red]Encodes are not allowed on AsianCinema.')
            if not cli_ui.ask_yes_no('Do you want to upload anyway?', default=False):
                return False

        return True

    async def get_additional_data(self, meta: Meta) -> dict[str, Any]:
        data = {
            'mod_queue_opt_in': await self.get_flag(meta, 'modq'),
        }

        return data

    # All uploads are allowed a maximum of 10 keywords
    # A keyword is defined as being 3 words or fewer, separated by a comma from the next keyword
    async def get_keywords(self, meta: Meta) -> dict[str, str]:
        raw_keywords = meta.get('keywords') or ''

        if not isinstance(raw_keywords, str):
            return {'keywords': ''}

        keywords = []

        for keyword in raw_keywords.split(','):
            keyword = keyword.strip()
            if not keyword:
                continue

            word_count = len(keyword.split())
            if word_count > 3:
                continue

            keywords.append(keyword)

            if len(keywords) == 10:
                break

        return {'keywords': ', '.join(keywords)}

    # Custom description header for WEB-DL uploads only
    async def get_description(self, meta: Meta) -> dict[str, str]:
        if meta.get('type') == 'WEBDL' and meta.get('service_longname'):
            self.tracker_config['custom_description_header'] = (
                f"[center][b][color=#ff00ff][size=18]This release is sourced from {meta['service_longname']} and is not "
                f"transcoded, just remuxed from the direct {meta['service_longname']} stream[/size][/color][/b][/center]"
            )

        return {
            'description': await DescriptionBuilder(self.tracker, self.config).unit3d_edit_desc(meta, comparison=True)
        }

    async def get_name(self, meta: Meta) -> dict[str, str]:
        acm_name = meta.get('name', '')
        return {'name': acm_name}
