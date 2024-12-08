# ruff: noqa: E501

import json
import pathlib
import unittest
from datetime import date

from requests import Response

from pyepggrab.grabbers.hu_porthu import hu_porthu
from pyepggrab.log import Log
from pyepggrab.xmltv import (
    XmltvCategory,
    XmltvChannel,
    XmltvComposer,
    XmltvCredits,
    XmltvDate,
    XmltvDesc,
    XmltvDirector,
    XmltvDisplayName,
    XmltvEpisodeNum,
    XmltvIcon,
    XmltvLength,
    XmltvProducer,
    XmltvProgramme,
    XmltvRating,
    XmltvSubTitle,
    XmltvTitle,
    XmltvUrl,
    XmltvValue,
)

TESTDATADIR = pathlib.Path(__file__).parent.joinpath("testdata")


class ModdedResponseForTesting(Response):
    def set_content(self, content: bytes) -> None:
        self._content = content


class TestProgramListParsing(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        Log.init_loggers()
        Log.set_loglevel("DEBUG")
        Log.finalize_loggers()

    def test_daystart_dayend(self) -> None:
        with TESTDATADIR.joinpath("daystart_dayend.json").open(
            encoding="UTF-8",
        ) as file:
            jdata = json.load(file)
            chans, progjsons = hu_porthu.extract_channel_data(
                jdata,
                ["tvhammel-194", "tvchannel-9"],
                date.fromisoformat("2023-02-09"),
            )

            self.assertCountEqual(daystart_dayend_channels, chans.values())
            self.assertCountEqual(daystart_dayend_progjsons, progjsons)

    def test_series_parse_series_slow(self) -> None:
        with TESTDATADIR.joinpath("episode-3042606.json").open(
            encoding="UTF-8",
        ) as jfile, TESTDATADIR.joinpath("episode-3042606.html").open(
            encoding="UTF-8",
        ) as hfile:
            jdata = json.load(jfile)
            html = hfile.read()

            rsp = ModdedResponseForTesting()
            rsp.status_code = 200
            rsp.set_content(html.encode())

            xprog = hu_porthu.create_xprogramme([jdata], rsp)

            self.assertEqual(1, len(xprog))
            self.assertEqual(str(parse_series_slow), str(xprog[0]))
            self.assertEqual(parse_series_slow, xprog[0])

    def test_series_parse_series(self) -> None:
        with TESTDATADIR.joinpath("episode-3042606.json").open(
            encoding="UTF-8",
        ) as file:
            jdata = json.load(file)
            xprog = hu_porthu.create_xprogramme([jdata], None)

            self.assertEqual(1, len(xprog))
            self.assertEqual(str(parse_series), str(xprog[0]))
            self.assertEqual(parse_series, xprog[0])

    def test_series_parse_movie_slow(self) -> None:
        with TESTDATADIR.joinpath("movie-256363.json").open(
            encoding="UTF-8",
        ) as jfile, TESTDATADIR.joinpath("movie-256363.html").open(
            encoding="UTF-8",
        ) as hfile:
            jdata = json.load(jfile)
            html = hfile.read()

            rsp = ModdedResponseForTesting()
            rsp.status_code = 200
            rsp.set_content(html.encode())

            xprog = hu_porthu.create_xprogramme([jdata], rsp)

            self.assertEqual(1, len(xprog))
            self.assertEqual(str(parse_movie_slow), str(xprog[0]))
            self.assertEqual(parse_movie_slow, xprog[0])

    def test_series_parse_movie(self) -> None:
        with TESTDATADIR.joinpath("movie-256363.json").open(encoding="UTF-8") as file:
            jdata = json.load(file)
            xprog = hu_porthu.create_xprogramme([jdata], None)

            self.assertEqual(1, len(xprog))
            self.assertEqual(str(parse_movie), str(xprog[0]))
            self.assertEqual(parse_movie, xprog[0])

    def test_space_in_country_name(self) -> None:
        with TESTDATADIR.joinpath("space_country.json").open(encoding="UTF-8") as file:
            jdata = json.load(file)
            xprog = hu_porthu.create_xprogramme([jdata], None)

            self.assertEqual(1, len(xprog))
            self.assertEqual(str(space_country), str(xprog[0]))
            self.assertEqual(space_country, xprog[0])


daystart_dayend_channels = [
    XmltvChannel(
        id_="194.port.hu",
        display_names=[XmltvDisplayName("Comedy Central", "hu")],
        # Not implemented
        # icons=[
        #    XmltvIcon(
        #        "https://media.port.hu/images/001/545/100x100/386.jpg"
        #    )
        # ],
        # urls=[
        #    XmltvUrl(
        #        "https://port.hu/csatorna/tv/comedy-central/tvchannel-194",
        #        "port.hu"
        #    )
        # ]
    ),
    XmltvChannel(
        id_="9.port.hu",
        display_names=[XmltvDisplayName("Spektrum", "hu")],
        # Not implemented
        # icons=[
        #    XmltvIcon(
        #        "https://media.port.hu/images/001/545/100x100/718.jpg"
        #    )
        # ],
        # urls=[
        #     XmltvUrl(
        #         "https://port.hu/csatorna/tv/spektrum/tvchannel-9",
        #         "port.hu"
        #     )
        # ]
    ),
]

daystart_dayend_progjsons = [
    {
        "id": "event-tv-1159526715-194",
        "start_datetime": "2023-02-09T00:25:00+01:00",
        "start_time": "00:25",
        "start_ts": 1675898700,
        "end_time": "00:55",
        "end_datetime": "2023-02-09T00:55:00+01:00",
        "is_child_event": False,
        "title": "South Park",
        "sound_quality": None,
        "italics": None,
        "episode_title": "Gluténmentes ebola",
        "description": None,
        "short_description": "amerikai animációs sorozat, XVIII / 2. rész",
        "highlight": None,
        "is_repeat": False,
        "is_live_mp": False,
        "is_overlapping": False,
        "film_id": "movie-18285",
        "film_url": "/adatlap/sorozat/tv/south-park/glutenmentes-ebola/event-tv-1159526715-194/episode-317219",
        "favorite_url": None,
        "del_calendar_url": None,
        "has_reminder": False,
        "show_reminder": False,
        "is_notified": False,
        "show_notification": False,
        "media_url": None,
        "media": None,
        "has_video": False,
        "attributes_text": "",
        "outer_links": {
            "film_outer_link": None,
            "watch_movie_link": None,
            "extra_link": None,
        },
        "restriction": {
            "age_limit": 18,
            "ageLimitImage": "/img/agelimit/vector/18_age_icon_black.svg",
            "ageLimitName": "18 éven aluliak számára nem ajánlott",
            "category": "filmsorozat",
        },
        "type": "past",
    },
    {
        "id": "event-tv-1159928131-1",
        "start_datetime": "2023-02-09T23:30:00+01:00",
        "start_time": "23:30",
        "start_ts": 1675981800,
        "end_time": "00:00",
        "end_datetime": "2023-02-10T00:00:00+01:00",
        "is_child_event": False,
        "title": "VILÁGHÍRADÓ",
        "sound_quality": None,
        "italics": None,
        "episode_title": None,
        "description": None,
        "short_description": "",
        "highlight": None,
        "is_repeat": True,
        "is_live_mp": False,
        "is_overlapping": False,
        "film_id": "movie-43421",
        "film_url": "/adatlap/film/tv/vilaghirado-vilaghirado/event-tv-1159928131-1/movie-43421",
        "favorite_url": None,
        "del_calendar_url": None,
        "has_reminder": False,
        "show_reminder": True,
        "is_notified": False,
        "show_notification": True,
        "media_url": None,
        "media": None,
        "has_video": False,
        "attributes_text": "<span class='mtxt'> (ism.)</span>",
        "outer_links": {
            "film_outer_link": None,
            "watch_movie_link": None,
            "extra_link": None,
        },
        "restriction": {
            "age_limit": 0,
            "ageLimitImage": "/img/agelimit/vector/0_age_icon_black.svg",
            "ageLimitName": "korhatárra való tekintet nélkül megtekinthető",
            "category": "hir-politikai-musor",
        },
        "type": "evening",
    },
    {
        "id": "event-tv-1156778488-9",
        "start_datetime": "2023-02-09T00:00:00+01:00",
        "start_time": "00:00",
        "start_ts": 1675897200,
        "end_time": "00:25",
        "end_datetime": "2023-02-09T00:25:00+01:00",
        "is_child_event": False,
        "title": "Határtalan drogháborúk",
        "sound_quality": None,
        "italics": None,
        "episode_title": None,
        "description": None,
        "short_description": "amerikai dokumentumfilm, III / 5. rész",
        "highlight": None,
        "is_repeat": False,
        "is_live_mp": False,
        "is_overlapping": False,
        "film_id": "movie-228004",
        "film_url": "/adatlap/film/tv/hatartalan-droghaboruk-drug-wars/event-tv-1156778488-9/episode-1956638",
        "favorite_url": None,
        "del_calendar_url": None,
        "has_reminder": False,
        "show_reminder": False,
        "is_notified": False,
        "show_notification": False,
        "media_url": None,
        "media": None,
        "has_video": False,
        "attributes_text": "",
        "outer_links": {
            "film_outer_link": None,
            "watch_movie_link": None,
            "extra_link": None,
        },
        "restriction": {
            "age_limit": 16,
            "ageLimitImage": "/img/agelimit/vector/16_age_icon_black.svg",
            "ageLimitName": "16 éven aluliak számára nem ajánlott",
            "category": "dokumentumfilm",
        },
        "type": "past",
    },
    {
        "id": "event-tv-1156778481-9",
        "start_datetime": "2023-02-09T00:25:00+01:00",
        "start_time": "00:25",
        "start_ts": 1675898700,
        "end_time": "01:15",
        "end_datetime": "2023-02-09T01:15:00+01:00",
        "is_child_event": False,
        "title": "Gyilkos nemzet",
        "sound_quality": None,
        "italics": None,
        "episode_title": None,
        "description": None,
        "short_description": "amerikai reality-sorozat, I / 3. rész",
        "highlight": None,
        "is_repeat": False,
        "is_live_mp": False,
        "is_overlapping": False,
        "film_id": "movie-237296",
        "film_url": "/adatlap/film/tv/gyilkos-nemzet-murder-nation/event-tv-1156778481-9/episode-2298882",
        "favorite_url": None,
        "del_calendar_url": None,
        "has_reminder": False,
        "show_reminder": False,
        "is_notified": False,
        "show_notification": False,
        "media_url": None,
        "media": None,
        "has_video": False,
        "attributes_text": "",
        "outer_links": {
            "film_outer_link": None,
            "watch_movie_link": None,
            "extra_link": None,
        },
        "restriction": {
            "age_limit": 16,
            "ageLimitImage": "/img/agelimit/vector/16_age_icon_black.svg",
            "ageLimitName": "16 éven aluliak számára nem ajánlott",
            "category": "dokumentumfilm",
        },
        "type": "past",
    },
    {
        "id": "event-tv-1156783174-9",
        "start_datetime": "2023-02-09T23:05:00+01:00",
        "start_time": "23:05",
        "start_ts": 1675980300,
        "end_time": "00:00",
        "end_datetime": "2023-02-10T00:00:00+01:00",
        "is_child_event": False,
        "title": "Pusztító viharok nyomában",
        "sound_quality": None,
        "italics": None,
        "episode_title": None,
        "description": None,
        "short_description": "amerikai dokumentumfilm, I / 3. rész",
        "highlight": None,
        "is_repeat": False,
        "is_live_mp": False,
        "is_overlapping": False,
        "film_id": "movie-226436",
        "film_url": "/adatlap/film/tv/pusztito-viharok-nyomaban-deadline-to-disaster/event-tv-1156783174-9/episode-1839440",
        "favorite_url": None,
        "del_calendar_url": None,
        "has_reminder": False,
        "show_reminder": True,
        "is_notified": False,
        "show_notification": True,
        "media_url": None,
        "media": None,
        "has_video": False,
        "attributes_text": "",
        "outer_links": {
            "film_outer_link": None,
            "watch_movie_link": None,
            "extra_link": None,
        },
        "restriction": {
            "age_limit": 12,
            "ageLimitImage": "/img/agelimit/vector/12_age_icon_black.svg",
            "ageLimitName": "12 éven aluliak számára a megtekintése nagykorú felügyelete mellett ajánlott",
            "category": "dokumentumfilm",
        },
        "type": "evening",
    },
]

parse_series_slow = XmltvProgramme(
    start="20241208041500 +0100",
    stop="20241208050500 +0100",
    channel="9.port.hu",
    titles=[XmltvTitle("A tudomány története")],
    sub_titles=[
        XmltvSubTitle(
            "Mi van rajtunk kívül? - (angol dokumentumfilm sorozat, 1/1. rész, 2010)",
            "hu",
        ),
    ],
    descs=[
        XmltvDesc(
            "Mi van a Földön túl? Honnan jöttünk? Miből lettünk? Mi az élet titka? Valóban határtalanok a képességeink és hatalmunk? Kik vagyunk? Ez az izgalmas sorozat bemutatja, hogyan alakította a tudomány az életünket.",
            "hu",
        ),
    ],
    credits_=XmltvCredits(
        directors=[
            XmltvDirector(
                name="Nicola Cook",
                urls=[
                    XmltvUrl(
                        "http://port.hu/adatlap/szemely/nicola-cook/person-348622",
                        "port.hu",
                    ),
                ],
            ),
            XmltvDirector(
                name="Giles Harrison",
                urls=[
                    XmltvUrl(
                        "http://port.hu/adatlap/szemely/giles-harrison/person-348623",
                        "port.hu",
                    ),
                ],
            ),
            XmltvDirector(
                name="Peter Oxley",
                urls=[
                    XmltvUrl(
                        "http://port.hu/adatlap/szemely/peter-oxley/person-338242",
                        "port.hu",
                    ),
                ],
            ),
            XmltvDirector(
                name="Nat Sharman",
                urls=[
                    XmltvUrl(
                        "http://port.hu/adatlap/szemely/nat-sharman/person-348624",
                        "port.hu",
                    ),
                ],
            ),
            XmltvDirector(
                name="Jeremy Turner",
                urls=[
                    XmltvUrl(
                        "http://port.hu/adatlap/szemely/jeremy-turner/person-257166",
                        "port.hu",
                    ),
                ],
            ),
            XmltvDirector(
                name="Nigel Walk",
                urls=[
                    XmltvUrl(
                        "http://port.hu/adatlap/szemely/nigel-walk/person-273225",
                        "port.hu",
                    ),
                ],
            ),
        ],
        producers=[
            XmltvProducer(
                name="Aidan Laverty",
                urls=[
                    XmltvUrl(
                        "http://port.hu/adatlap/szemely/aidan-laverty/person-334962",
                        "port.hu",
                    ),
                ],
            ),
        ],
        composers=[
            XmltvComposer(
                name="Ty Unwin",
                urls=[
                    XmltvUrl(
                        "http://port.hu/adatlap/szemely/ty-unwin/person-206154",
                        "port.hu",
                    ),
                ],
            ),
        ],
    ),
    date=XmltvDate("2010"),
    categories=[
        XmltvCategory("Education/Science/Factual", "en"),
        XmltvCategory("Oktatás/Tudomány/Tényfeltáró", "hu"),
        XmltvCategory("series", "en"),
    ],
    urls=[
        XmltvUrl(
            "https://port.hu/adatlap/sorozat/tv/a-tudomany-tortenete-history-of-science/mi-van-rajtunk-kivul/event-tv-1624256384-9/episode-3042606",
            "port.hu",
        ),
    ],
    episode_nums=[XmltvEpisodeNum("0.0.0/1", "xmltv_ns")],
    ratings=[
        XmltvRating(
            value=XmltvValue("12"),
            icons=[
                XmltvIcon("https://port.hu/img/agelimit/raster/12_age_icon_black.png"),
            ],
        ),
    ],
)

parse_series = XmltvProgramme(
    start="20241208041500 +0100",
    stop="20241208050500 +0100",
    channel="9.port.hu",
    titles=[XmltvTitle("A tudomány története")],
    sub_titles=[
        XmltvSubTitle(
            "Mi van rajtunk kívül? - (angol dokumentumfilm sorozat, 1/1. rész)",
            "hu",
        ),
    ],
    categories=[
        XmltvCategory("Education/Science/Factual", "en"),
        XmltvCategory("Oktatás/Tudomány/Tényfeltáró", "hu"),
        XmltvCategory("series", "en"),
    ],
    urls=[
        XmltvUrl(
            "https://port.hu/adatlap/sorozat/tv/a-tudomany-tortenete-history-of-science/mi-van-rajtunk-kivul/event-tv-1624256384-9/episode-3042606",
            "port.hu",
        ),
    ],
    episode_nums=[XmltvEpisodeNum("0.0.0/1", "xmltv_ns")],
    ratings=[
        XmltvRating(
            value=XmltvValue("12"),
            icons=[
                XmltvIcon("https://port.hu/img/agelimit/raster/12_age_icon_black.png"),
            ],
        ),
    ],
)

parse_movie_slow = XmltvProgramme(
    start="20241208050500 +0100",
    stop="20241208060000 +0100",
    channel="9.port.hu",
    titles=[XmltvTitle("Tengeralattjárók")],
    sub_titles=[
        XmltvSubTitle("(2023)", "hu"),
    ],
    descs=[
        XmltvDesc(
            "Az aktuális rész ismertetője: A tengeralattjárók a technológia csúcsai. Ilyen a Redoutable, amely 16 nukleáris rakétát képes szállítani. Vagy a Suffren, egy igazi vízalatti ragadozó. És itt van a Rubis is, a II. világháborús veterán.",
            "hu",
        ),
    ],
    date=XmltvDate("2023"),
    length=XmltvLength("63", "minutes"),
    urls=[
        XmltvUrl(
            "https://port.hu/adatlap/film/tv/tengeralattjarok-mega-building-collection-record-breaking-submarines/event-tv-1624256387-9/movie-256363",
            "port.hu",
        ),
    ],
    ratings=[
        XmltvRating(
            value=XmltvValue("12"),
            icons=[
                XmltvIcon("https://port.hu/img/agelimit/raster/12_age_icon_black.png"),
            ],
        ),
    ],
)

parse_movie = XmltvProgramme(
    start="20241208050500 +0100",
    stop="20241208060000 +0100",
    channel="9.port.hu",
    titles=[XmltvTitle("Tengeralattjárók")],
    sub_titles=[
        XmltvSubTitle("(2023)", "hu"),
    ],
    date=XmltvDate("2023"),
    urls=[
        XmltvUrl(
            "https://port.hu/adatlap/film/tv/tengeralattjarok-mega-building-collection-record-breaking-submarines/event-tv-1624256387-9/movie-256363",
            "port.hu",
        ),
    ],
    ratings=[
        XmltvRating(
            value=XmltvValue("12"),
            icons=[
                XmltvIcon("https://port.hu/img/agelimit/raster/12_age_icon_black.png"),
            ],
        ),
    ],
)

space_country = XmltvProgramme(
    start="20230710155000 +0200",
    stop="20230710165500 +0200",
    channel="304.port.hu",
    titles=[XmltvTitle("Vadmacska")],
    sub_titles=[
        XmltvSubTitle(
            "(venezuelai-amerikai-Puerto Rico-i filmsorozat, 230. rész)",
            "hu",
        ),
    ],
    categories=[
        XmltvCategory("Movie/Drama", "en"),
        XmltvCategory("Film/Dráma", "hu"),
        XmltvCategory("series", "en"),
    ],
    urls=[
        XmltvUrl(
            "https://port.hu/adatlap/film/tv/vadmacska-la-gata-salvaje/event-tv-1273317596-304/episode-108551",
            "port.hu",
        ),
    ],
    episode_nums=[XmltvEpisodeNum(".229.0/1", "xmltv_ns")],
    ratings=[
        XmltvRating(
            value=XmltvValue("12"),
            icons=[
                XmltvIcon("https://port.hu/img/agelimit/raster/12_age_icon_black.png"),
            ],
        ),
    ],
)

if __name__ == "__main__":
    unittest.main()
