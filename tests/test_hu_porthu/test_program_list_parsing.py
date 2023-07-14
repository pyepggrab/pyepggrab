# ruff: noqa: E501

import json
import pathlib
import unittest
from datetime import date

from requests import Response

from pyepggrab.grabbers.hu_porthu import hu_porthu
from pyepggrab.log import Log
from pyepggrab.xmltv import (
    XmltvActor,
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
        with TESTDATADIR.joinpath("series.json").open(
            encoding="UTF-8",
        ) as jfile, TESTDATADIR.joinpath("series.html").open(encoding="UTF-8") as hfile:
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
        with TESTDATADIR.joinpath("series.json").open(encoding="UTF-8") as file:
            jdata = json.load(file)
            xprog = hu_porthu.create_xprogramme([jdata], None)

            self.assertEqual(1, len(xprog))
            self.assertEqual(str(parse_series), str(xprog[0]))
            self.assertEqual(parse_series, xprog[0])

    def test_series_parse_movie_slow(self) -> None:
        with TESTDATADIR.joinpath("movie.json").open(
            encoding="UTF-8",
        ) as jfile, TESTDATADIR.joinpath("movie.html").open(encoding="UTF-8") as hfile:
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
        with TESTDATADIR.joinpath("movie.json").open(encoding="UTF-8") as file:
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
    start="20230209002500 +0100",
    stop="20230209005500 +0100",
    channel="194.port.hu",
    titles=[XmltvTitle("South Park")],
    sub_titles=[
        XmltvSubTitle(
            "Gluténmentes ebola - (amerikai animációs sorozat, 18/2. rész, 1997)",
            "hu",
        ),
    ],
    descs=[
        XmltvDesc(
            "Az aktuális rész ismertetője: South Park gluténmentessé válik.\n\n"
            "A műsor ismertetése: A South Park minden idők egyik legismertebb animációs sorozata, 4 mocskos szájú negyedikesről, amely szürreális humorával űz gúnyt világunkból.",
            "hu",
        ),
    ],
    credits_=XmltvCredits(
        directors=[
            XmltvDirector(
                name="Trey Parker",
                urls=[
                    XmltvUrl(
                        "https://port.hu/adatlap/szemely/trey-parker/person-18931",
                        "port.hu",
                    ),
                ],
            ),
            XmltvDirector(
                name="Matt Stone",
                urls=[
                    XmltvUrl(
                        "https://port.hu/adatlap/szemely/matt-stone/person-105060",
                        "port.hu",
                    ),
                ],
            ),
            XmltvDirector(
                name="Eric Stough",
                urls=[
                    XmltvUrl(
                        "https://port.hu/adatlap/szemely/eric-stough/person-217037",
                        "port.hu",
                    ),
                ],
            ),
        ],
        actors=[
            XmltvActor(
                name="Trey Parker",
                urls=[
                    XmltvUrl(
                        "https://port.hu/adatlap/szemely/trey-parker/person-18931",
                        "port.hu",
                    ),
                ],
            ),
            XmltvActor(
                name="Matt Stone",
                urls=[
                    XmltvUrl(
                        "https://port.hu/adatlap/szemely/matt-stone/person-105060",
                        "port.hu",
                    ),
                ],
            ),
            XmltvActor(
                name="Mary Kay Bergman",
                urls=[
                    XmltvUrl(
                        "https://port.hu/adatlap/szemely/mary-kay-bergman/person-105061",
                        "port.hu",
                    ),
                ],
            ),
            XmltvActor(
                name="Isaac Hayes",
                urls=[
                    XmltvUrl(
                        "https://port.hu/adatlap/szemely/isaac-hayes/person-9026",
                        "port.hu",
                    ),
                ],
            ),
            XmltvActor(
                name="Eliza Schneider",
                urls=[
                    XmltvUrl(
                        "https://port.hu/adatlap/szemely/eliza-schneider/person-217039",
                        "port.hu",
                    ),
                ],
            ),
        ],
    ),
    date=XmltvDate("1997"),
    categories=[
        XmltvCategory("Movie/Drama", "en"),
        XmltvCategory("Film/Dráma", "hu"),
        XmltvCategory("series", "en"),
    ],
    urls=[
        XmltvUrl(
            "https://port.hu/adatlap/sorozat/tv/south-park/glutenmentes-ebola/event-tv-1159526715-194/episode-317219",
            "port.hu",
        ),
    ],
    episode_nums=[XmltvEpisodeNum("17.1.0/1", "xmltv_ns")],
    ratings=[
        XmltvRating(
            value=XmltvValue("18"),
            icons=[
                XmltvIcon("https://port.hu/img/agelimit/raster/18_age_icon_black.png"),
            ],
        ),
    ],
)

parse_series = XmltvProgramme(
    start="20230209002500 +0100",
    stop="20230209005500 +0100",
    channel="194.port.hu",
    titles=[XmltvTitle("South Park")],
    sub_titles=[
        XmltvSubTitle(
            "Gluténmentes ebola - (amerikai animációs sorozat, 18/2. rész)",
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
            "https://port.hu/adatlap/sorozat/tv/south-park/glutenmentes-ebola/event-tv-1159526715-194/episode-317219",
            "port.hu",
        ),
    ],
    episode_nums=[XmltvEpisodeNum("17.1.0/1", "xmltv_ns")],
    ratings=[
        XmltvRating(
            value=XmltvValue("18"),
            icons=[
                XmltvIcon("https://port.hu/img/agelimit/raster/18_age_icon_black.png"),
            ],
        ),
    ],
)

parse_movie_slow = XmltvProgramme(
    start="20230211100500 +0100",
    stop="20230211120000 +0100",
    channel="6.port.hu",
    titles=[XmltvTitle("Marley meg én")],
    sub_titles=[
        XmltvSubTitle("(amerikai vígjáték, filmdráma, családi film, 2008)", "hu"),
    ],
    descs=[
        XmltvDesc(
            "John és Jennifer Grogan friss házasok. Mindketten újságíróként dolgoznak, szeretik a munkájukat, de még jobban egymást. Amikor beköltöznek első közös otthonukba, John úgy érzi, ideje lenne igazi családot alapítani. Mivel azonban még nem érzi magát felkészültnek az apaságra, egyik barátja tanácsára örökbe fogadnak egy kölyökkutyát, hogy némi tapasztalatot szerezzenek a gondoskodásról. Marley, a pajkos és játékos labradorkölyök azonban teljesen felforgatja addigi életüket, és hamarosan katasztrófa sújtotta övezetté változtatja otthonukat...",
            "hu",
        ),
    ],
    credits_=XmltvCredits(
        directors=[
            XmltvDirector(
                name="David Frankel",
                urls=[
                    XmltvUrl(
                        "https://port.hu/adatlap/szemely/david-frankel/person-132192",
                        "port.hu",
                    ),
                ],
            ),
        ],
        actors=[
            XmltvActor(
                name="Owen Wilson",
                urls=[
                    XmltvUrl(
                        "https://port.hu/adatlap/szemely/owen-wilson/person-12884",
                        "port.hu",
                    ),
                ],
            ),
            XmltvActor(
                name="Jennifer Aniston",
                urls=[
                    XmltvUrl(
                        "https://port.hu/adatlap/szemely/jennifer-aniston/person-14454",
                        "port.hu",
                    ),
                ],
            ),
            XmltvActor(
                name="Eric Dane",
                urls=[
                    XmltvUrl(
                        "https://port.hu/adatlap/szemely/eric-dane/person-178440",
                        "port.hu",
                    ),
                ],
            ),
            XmltvActor(
                name="Kathleen Turner",
                urls=[
                    XmltvUrl(
                        "https://port.hu/adatlap/szemely/kathleen-turner/person-8302",
                        "port.hu",
                    ),
                ],
            ),
            XmltvActor(
                name="Alan Arkin",
                urls=[
                    XmltvUrl(
                        "https://port.hu/adatlap/szemely/alan-arkin/person-7994",
                        "port.hu",
                    ),
                ],
            ),
        ],
        producers=[
            XmltvProducer(
                name="Gil Netter",
                urls=[
                    XmltvUrl(
                        "https://port.hu/adatlap/szemely/gil-netter/person-121926",
                        "port.hu",
                    ),
                ],
            ),
            XmltvProducer(
                name="Karen Rosenfelt",
                urls=[
                    XmltvUrl(
                        "https://port.hu/adatlap/szemely/karen-rosenfelt/person-295041",
                        "port.hu",
                    ),
                ],
            ),
        ],
        composers=[
            XmltvComposer(
                name="Theodore Shapiro",
                urls=[
                    XmltvUrl(
                        "https://port.hu/adatlap/szemely/theodore-shapiro/person-152429",
                        "port.hu",
                    ),
                ],
            ),
        ],
    ),
    date=XmltvDate("2008"),
    categories=[
        XmltvCategory("Comedy", "en"),
        XmltvCategory("Movie/Drama", "en"),
        XmltvCategory("Children's/Youth programmes", "en"),
        XmltvCategory("Vígjáték", "hu"),
        XmltvCategory("Film/Dráma", "hu"),
        XmltvCategory("Gyerek/Ifjúsági program", "hu"),
        XmltvCategory("movie", "en"),
    ],
    length=XmltvLength("118", "minutes"),
    urls=[
        XmltvUrl(
            "https://port.hu/adatlap/film/tv/marley-meg-en-marley-me/event-tv-1159915099-6/movie-100058",
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
    start="20230211100500 +0100",
    stop="20230211120000 +0100",
    channel="6.port.hu",
    titles=[XmltvTitle("Marley meg én")],
    sub_titles=[
        XmltvSubTitle("(amerikai vígjáték, filmdráma, családi film, 2008)", "hu"),
    ],
    date=XmltvDate("2008"),
    categories=[
        XmltvCategory("Comedy", "en"),
        XmltvCategory("Movie/Drama", "en"),
        XmltvCategory("Children's/Youth programmes", "en"),
        XmltvCategory("Vígjáték", "hu"),
        XmltvCategory("Film/Dráma", "hu"),
        XmltvCategory("Gyerek/Ifjúsági program", "hu"),
        XmltvCategory("movie", "en"),
    ],
    urls=[
        XmltvUrl(
            "https://port.hu/adatlap/film/tv/marley-meg-en-marley-me/event-tv-1159915099-6/movie-100058",
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
