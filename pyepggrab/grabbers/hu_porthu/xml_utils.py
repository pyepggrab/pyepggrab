"""XML utilities to build and parse to XMLTV format."""

import re
from datetime import datetime
from typing import Dict, Iterable, List, Optional, Tuple

import extruct  # type: ignore[import]
import requests
import roman  # type: ignore[import]

from pyepggrab.grabbers.hu_porthu.catmap import CATDICT
from pyepggrab.grabbers.hu_porthu.utils import (
    append_if_not_empty,
    eventid_to_xmlid,
    portid_to_xmlid,
    to_absolute_porturl,
    to_friendlyimage,
)
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
    XmltvPreviouslyShown,
    XmltvProducer,
    XmltvProgramme,
    XmltvRating,
    XmltvSubTitle,
    XmltvTitle,
    XmltvUrl,
    XmltvValue,
    to_xmltv_date,
)

RE_JSONDESC = re.compile(
    r"^(?P<countries>[A-Za-zÁáÉéÍíÓóÖöŐőÚúÜüŰű -]+)?"
    r"(?:(?: |^)(?P<categories>[A-Za-zÁáÉéÍíÓóÖöŐőÚúÜüŰű, -]+)(?:, |$))?"
    r"(?:(?:(?<=, )|^)(?P<season>[IVXLCDM]+)(?: / ))?"
    r"(?:(?P<episode>[0-9]+)\. rész)?(?:, )?"
    r"(?P<year>[0-9]{4})?$",
)
"""`countries` captures the first part of the `categories` if no country present
because it's impossible to distinguish between a county name and a category name

`countries` also captures the first part of the `categories` if the first
category contains space

example 1:

angol tévéfilmsorozat, IV / 15. rész -> angol | tévéfilmsorozat | IV | 15

talk show, I / 9. rész -> talk | show | I | 9

example 2:

török romantikus vígjáték , I / 13. rész -> török romantikus | vígjáték  | I | 13
                         ^ extra space came from port.hu

example 3:

venezuelai-amerikai-Puerto Rico-i filmsorozat, 230. rész ->
    venezuelai-amerikai-Puerto Rico-i | filmsorozat | 230

if the `countries` can be categorized then it's a category not a country
"""

RE_DESC_TAG = re.compile(r"<div class=\"description\">([\s\S]+?)</div>")
RE_EXTRACT_TEXT = re.compile(r">([\s\S]+?)<")

RE_HTML_TAG = re.compile(r"<[^>]*>")


RE_MYTHTVCAT: List[Tuple[re.Pattern, str]] = [
    # Order matters
    (re.compile(r"sport"), "sports"),
    (re.compile(r"sorozat"), "series"),
    (
        re.compile(
            r"(?!^.*sorozat)(?:^.*(?:film|dráma|kaland|romantikus|western|akció|krimi"
            r"|thriller|misztikus|horror|sci-fi|fantasy|vígjáték|kabaré|történel|komédia|comedy))",
        ),
        "movie",
    ),
    (re.compile(r".+"), "tvshow"),
]


def match_categories(cats: List[str]) -> List[XmltvCategory]:
    """Match a list of categories to ETSI and mythtv compatible categories.

    ETSI: ETSI EN 300 468 V1.14.1
    mythtv: sports, series, movie, tvshow

    Categories are ordered in ETSI en, ETSI hu, mythtv order.
    ETSI categories can contain more than one entry.
    """
    encats: List[XmltvCategory] = []
    hucats: List[XmltvCategory] = []
    mythcat: Optional[XmltvCategory] = None
    log = Log.get_grabber_logger()

    flatcats = []
    for cat in cats:
        flatcats += cat.split(", ")

    for cat in cats:
        # match category
        if cat in CATDICT:
            encats.append(XmltvCategory(CATDICT[cat].value[0], "en"))
            hucats.append(XmltvCategory(CATDICT[cat].value[1], "hu"))
        # TODO: elif try to match unknown catergory
        else:
            log.warning("Unknown category: '%s'", cat)

        # try to match mythtv category if not already
        if mythcat is None:
            for re_cat in RE_MYTHTVCAT:
                if re_cat[0].search(cat) is not None:
                    mythcat = XmltvCategory(re_cat[1], "en")
                    break

    res = encats + hucats
    if res is None:
        log.warning("No category matched. Categories: %s", str(flatcats))

    if mythcat:
        res.append(mythcat)
    else:
        log.warning("Mythtv category not matched. Categories: %s", str(flatcats))

    return res


def is_category(catstr: str) -> bool:
    """Check if a string is matching a category."""
    # maybe check with regex too
    return catstr in CATDICT


def build_description(texts: Iterable[str]) -> str:
    """Build a description for a program.

    :param texts: lines/paragraphs of the description div

    Port.hu descriptions contains an "Az aktuális rész ismertetője" section and
    an "A műsor ismertetése" section. To keep the formatting of the page if both
    are present insert 2 newlines between them.
    """
    desc = ""
    for txt in texts:
        pad = " "
        if txt == "A műsor ismertetése:" and desc:
            pad = "\n\n"
        elif not desc:
            pad = ""
        desc += pad + txt
    return desc


def build_subtitle(  # noqa: PLR0913
    episode_title: Optional[str] = None,
    countries: Optional[str] = None,
    genre: Optional[str] = None,
    season_num: Optional[str] = None,
    episode_num: Optional[str] = None,
    release_date: Optional[str] = None,
) -> str:
    """Build a subtitle from the presented information.

    Format is
    `title - ([country] [genre], [<seasonnum>/<episodenum>. rész|<episodenum>. rész], [releasedate])`
    """  # noqa: E501
    subt = ""
    subt = append_if_not_empty(subt, "", countries)
    subt = append_if_not_empty(subt, " ", genre)
    subt = append_if_not_empty(subt, ", ", season_num)
    if season_num in (None, ""):
        subt = append_if_not_empty(subt, ", ", episode_num, ". rész")
    else:
        subt = append_if_not_empty(subt, "/", episode_num, ". rész")
    subt = append_if_not_empty(subt, ", ", release_date)
    if subt not in (None, ""):
        subt = f"({subt})"
    return append_if_not_empty(episode_title, " - ", subt)


def create_xprogramme(  # noqa: PLR0912, PLR0915
    progjsons: List[Dict],
    response: Optional[requests.Response] = None,
) -> List[XmltvProgramme]:
    """Build an XMLTV program from json and by scraping the page of the program."""
    log = Log.get_grabber_logger()

    retprogs = []

    # results of different parsers
    page_soup = None
    page_opengraph = None
    page_jsonld = None

    # opengraph
    og_duration = None
    og_release_date = None

    # jsonld
    # Descriptions are better from html
    # jld_desc = None
    jld_genre = None
    jld_episode_num = None
    jld_season_num = None
    jld_countrylist = []
    jld_actors = []
    jld_composers = []
    jld_directors = []
    jld_producers = []
    # Images currently not used
    # jld_image = None
    jld_subtitle = None

    # html
    page_desc = None

    if response and response.status_code == requests.codes.OK:
        page_extract: Dict = extruct.extract(
            response.text,
            syntaxes=["opengraph", "json-ld"],
            uniform=True,
        )
        page_opengraph = page_extract.get("opengraph", [None])[0]
        page_jsonld = page_extract.get("json-ld", [None])[0]
        # Currently, only the desc is used from the HTML
        # Doing it with regex it much faster than bs4
        # page_soup = BeautifulSoup(response.text, "html.parser")

    if page_opengraph:
        # From Opengraph data
        # same present in json-ld but this is easier to parse
        og_duration = page_opengraph.get("video:duration")
        og_release_date = page_opengraph.get("video:release_date")

    if page_jsonld:
        # From json-ld data
        # jld_desc = page_jsonld.get("description")
        jld_genre = page_jsonld.get("genre")
        if jld_genre:
            # Sometimes there is a leading space before the comma
            # or trailing space after the last category.
            # Causes failed category matches.
            jld_genre = jld_genre.replace(" , ", ", ").strip()

        jld_episode_num = page_jsonld.get("episodeNumber")
        jld_season_num = page_jsonld.get("partOfSeason", {}).get("seasonNumber")

        country: Dict
        for country in page_jsonld.get("countryOfOrigin", []):
            name = country.get("name")
            if name:
                jld_countrylist.append(name)

        actor: Dict
        for actor in page_jsonld.get("actor", []):
            name = actor.get("name")
            url = actor.get("sameAs")
            if name:
                jld_actors.append((name, url))

        composer: Dict
        for composer in page_jsonld.get("musicBy", []):
            name = composer.get("name")
            url = composer.get("sameAs")
            if name:
                jld_composers.append((name, url))

        director: Dict
        for director in page_jsonld.get("director", []):
            name = director.get("name")
            url = director.get("sameAs")
            if name:
                jld_directors.append((name, url))

        producer: Dict
        for producer in page_jsonld.get("producer", []):
            name = producer.get("name")
            url = producer.get("sameAs")
            if name:
                jld_producers.append((name, url))

        # jld_image = page_jsonld.get("image", {}).get("url")

    # From html
    if page_soup:
        soup_desc = page_soup.select_one("div.description")
        if soup_desc:
            page_desc = build_description(soup_desc.stripped_strings)
    elif response and response.status_code == requests.codes.OK:
        desc = RE_DESC_TAG.search(response.text)
        if desc:
            stripedtexts = [s.strip() for s in RE_HTML_TAG.split(desc.group(0))]
            texts = filter(len, stripedtexts)
            page_desc = build_description(texts)
        else:
            log.warning(
                "A response is received but the description can't be found. url: %s",
                response.url,
            )

    for progjson in progjsons:
        prog_subt = None

        j_title = None
        j_short_desc = None
        j_episode_title = None
        j_prev_shown = False
        j_age_limit = None
        j_age_limit_img = None

        # regex matched
        j_re_countries = None
        j_re_categories = None
        j_re_season = None
        j_re_episode = None
        j_re_year = None
        j_re_subtitle = None

        # From json data
        if "title" in progjson:
            j_title = progjson["title"]
        else:
            chid = progjson.get("id")
            chid = eventid_to_xmlid(chid) if chid else "unknown"
            start_time = progjson.get("start_datetime", "unknown")
            msg = (
                "No title present for program on channel "
                f"'{chid}' at '{start_time}'. Every program should have a title"
            )
            raise RuntimeError(msg)

        j_short_desc = progjson.get("short_description")
        if (
            None
            in [
                jld_countrylist,
                jld_genre,
                og_release_date,
                jld_season_num,
                jld_episode_num,
            ]
            and j_short_desc is not None
        ):
            # Sometimes there is a leading space before the comma
            # or trailing space if the categories are on the end.
            # Causes incorrect matches
            j_short_desc = j_short_desc.replace(" , ", ", ").strip()

            match = RE_JSONDESC.search(j_short_desc)
            if match and len(match.group(0)) > 0:
                j_re_countries = match.group("countries")
                j_re_categories = match.group("categories")
                j_re_season = match.group("season")
                j_re_episode = match.group("episode")
                j_re_year = match.group("year")

                # Country may be the first part of the category, not a country.
                # First try all parts of the country to see if is a category
                # if not decrease the number of parts.
                # Search is stopped after the first successful match

                j_re_country_splits = (
                    j_re_countries.split(" ") if j_re_countries else ""
                )
                cat_str = j_re_categories if j_re_categories else ""

                for i in range(len(j_re_country_splits)):
                    concat_country = " ".join(j_re_country_splits[i:])
                    if is_category(
                        f"{concat_country} {cat_str}".rstrip().split(", ")[0],
                    ):
                        if j_re_categories:
                            j_re_categories = f"{concat_country} {cat_str}"
                        else:
                            j_re_categories = concat_country
                        j_re_countries = " ".join(j_re_country_splits[:i])

                        break

        j_episode_title = progjson.get("episode_title")
        j_porturl = progjson.get("film_url")
        j_prev_shown = progjson.get("is_repeat", False)
        if "restriction" in progjson:
            restr: dict = progjson["restriction"]
            j_age_limit = restr.get("age_limit")
            j_age_limit_img = restr.get("ageLimitImage")
            if j_age_limit_img:
                j_age_limit_img = to_absolute_porturl(to_friendlyimage(j_age_limit_img))

        xtitle = XmltvTitle(j_title)

        xdescs = [XmltvDesc(page_desc, lang="hu")] if page_desc else []

        xdirectors = [
            XmltvDirector(name=name, urls=[XmltvUrl(url, "port.hu")] if url else [])
            for name, url in jld_directors
        ]

        xactors = [
            XmltvActor(name=name, urls=[XmltvUrl(url, "port.hu")] if url else [])
            for name, url in jld_actors
        ]

        xproducers = [
            XmltvProducer(name=name, urls=[XmltvUrl(url, "port.hu")] if url else [])
            for name, url in jld_producers
        ]

        xcomposers = [
            XmltvComposer(name=name, urls=[XmltvUrl(url, "port.hu")] if url else [])
            for name, url in jld_composers
        ]

        xcredits = None
        if len(xdirectors) + len(xactors) + len(xproducers) + len(xcomposers) > 0:
            xcredits = XmltvCredits(
                directors=xdirectors,
                actors=xactors,
                producers=xproducers,
                composers=xcomposers,
            )

        releasedate = og_release_date if og_release_date else j_re_year
        xdate = XmltvDate(releasedate) if releasedate else None

        xcategories = []
        if jld_genre:
            xcategories = match_categories(jld_genre.split(", "))
        elif j_re_categories:
            xcategories = match_categories(j_re_categories.split(", "))

        xlength = XmltvLength(og_duration, units="minutes") if og_duration else None
        xurls = (
            [XmltvUrl(to_absolute_porturl(j_porturl), "port.hu")] if j_porturl else []
        )

        if jld_season_num:
            seasonnum = int(jld_season_num)
        elif j_re_season and roman.romanNumeralPattern.search(j_re_season):
            seasonnum = roman.fromRoman(j_re_season)
        elif j_re_season and j_re_season.isdecimal():
            seasonnum = int(j_re_season)
        else:
            seasonnum = None

        if jld_episode_num:
            episodenum = int(jld_episode_num)
        elif j_re_episode and j_re_episode.isnumeric():
            episodenum = int(j_re_episode)
        else:
            episodenum = None

        xepnum = []
        if seasonnum or episodenum:
            xepnum = [
                XmltvEpisodeNum(
                    ".".join(
                        [
                            str(seasonnum - 1) if seasonnum else "",
                            str(episodenum - 1) if episodenum else "",
                            "0/1",
                        ],
                    ),
                    system="xmltv_ns",
                ),
            ]

        xprevshown = XmltvPreviouslyShown() if j_prev_shown else None

        xratings = (
            [
                XmltvRating(
                    XmltvValue(str(j_age_limit)),
                    icons=[XmltvIcon(j_age_limit_img)] if j_age_limit_img else [],
                ),
            ]
            if j_age_limit is not None
            else []
        )

        if page_jsonld:
            jld_subtitle = build_subtitle(
                j_episode_title,
                "-".join(jld_countrylist),
                jld_genre,
                jld_season_num,
                jld_episode_num,
                og_release_date,
            )

        if (
            j_re_countries
            or j_re_categories
            or j_re_season
            or j_re_episode
            or j_re_year
        ):
            j_re_subtitle = build_subtitle(
                j_episode_title,
                j_re_countries,
                j_re_categories,
                # j_re_season already processed -> seasonnum
                str(seasonnum) if seasonnum else None,
                # j_re_episode already processed -> episodenum
                str(episodenum) if episodenum else None,
                j_re_year,
            )

        j_short_desc_len = len(j_short_desc) if j_short_desc else 0
        j_ep_title_len = len(j_episode_title) if j_episode_title else 0
        jld_subt_len = len(jld_subtitle) if jld_subtitle else 0
        j_re_subt_len = len(j_re_subtitle) if j_re_subtitle else 0

        # Order of preference:
        # jld_subtitle > j_re_subtitle > j_short_desc + j_episode_title
        prog_subt = jld_subtitle
        if jld_subt_len < j_re_subt_len:
            prog_subt = j_re_subtitle
        elif jld_subt_len < j_short_desc_len + j_ep_title_len:
            prog_subt = ""
            if j_short_desc not in (None, ""):
                prog_subt = f"({j_short_desc})"
            prog_subt = append_if_not_empty(j_episode_title, " - ", prog_subt)

        xsub_titles = [XmltvSubTitle(prog_subt, lang="hu")] if prog_subt else []

        retprogs.append(
            XmltvProgramme(
                start=to_xmltv_date(datetime.fromisoformat(progjson["start_datetime"])),
                stop=to_xmltv_date(datetime.fromisoformat(progjson["end_datetime"])),
                channel=eventid_to_xmlid(progjson["id"]),
                titles=[xtitle],
                sub_titles=xsub_titles,
                descs=xdescs,
                credits_=xcredits,
                date=xdate,
                categories=xcategories,
                length=xlength,
                urls=xurls,
                episode_nums=xepnum,
                previously_shown=xprevshown,
                ratings=xratings,
            ),
        )
    return retprogs


def create_xmltvchannel(ch: Dict) -> XmltvChannel:
    """Create an XMLTV channel from a channel json."""
    return XmltvChannel(
        id_=portid_to_xmlid(ch["id"]),
        display_names=[XmltvDisplayName(display_name=ch["name"], lang="hu")],
    )
