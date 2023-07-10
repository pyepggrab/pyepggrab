import pathlib
import unittest
from datetime import datetime

from lxml import etree

from pyepggrab.xmltv import (
    XmltvActor,
    XmltvAdapter,
    XmltvAspect,
    XmltvAudio,
    XmltvCategory,
    XmltvChannel,
    XmltvColour,
    XmltvCommentator,
    XmltvComposer,
    XmltvCountry,
    XmltvCredits,
    XmltvDate,
    XmltvDesc,
    XmltvDirector,
    XmltvDisplayName,
    XmltvEditor,
    XmltvEpisodeNum,
    XmltvGuest,
    XmltvIcon,
    XmltvImage,
    XmltvKeyword,
    XmltvLanguage,
    XmltvLastChance,
    XmltvLength,
    XmltvNew,
    XmltvOrigLanguage,
    XmltvPremiere,
    XmltvPresent,
    XmltvPresenter,
    XmltvPreviouslyShown,
    XmltvProducer,
    XmltvProgramme,
    XmltvQuality,
    XmltvRating,
    XmltvReview,
    XmltvStarRating,
    XmltvStereo,
    XmltvSubTitle,
    XmltvSubtitles,
    XmltvTitle,
    XmltvTv,
    XmltvUrl,
    XmltvValue,
    XmltvVideo,
    XmltvWriter,
    to_xmltv_date,
)

try:
    from zoneinfo import ZoneInfo  # type: ignore # noqa: F401, RUF100
except ImportError:
    from backports.zoneinfo import ZoneInfo  # type: ignore # noqa: F401, RUF100

DTD = pathlib.Path(__file__).parent.parent.parent.joinpath(
    "pyepggrab/resources/xmltv.dtd",
)


class TestXmltvParsing(unittest.TestCase):
    def test_fullparse(self) -> None:
        try:
            tree = tvfulltree.to_xmltree()
            dtd = etree.DTD(DTD)
            dtd.assertValid(tree)
        except Exception as e:
            self.fail(str(e))


tvfulltree = XmltvTv(
    date="20230101",
    source_info_url="http://example.com",
    source_info_name="Example",
    source_data_url="http://example.com/data",
    generator_info_name="Example generator",
    generator_info_url="http://example.com/generator",
    channels=[
        XmltvChannel(
            id_="exampleid",
            display_names=[
                XmltvDisplayName(display_name="exdisp1", lang="en"),
                XmltvDisplayName(display_name="exdisp2", lang="ro"),
            ],
            icons=[
                XmltvIcon(src="http://example.com/icon1", width=10, height=20),
                XmltvIcon(src="http://example.com/icon2", width=20, height=30),
            ],
            urls=[
                XmltvUrl(url="http://example.com/url1", system="example"),
                XmltvUrl(url="http://example.com/url2", system="example"),
            ],
        ),
        XmltvChannel(
            id_="example2id",
            display_names=[
                XmltvDisplayName(display_name="exdisp11", lang="en"),
                XmltvDisplayName(display_name="exdisp22", lang="ro"),
            ],
            icons=[
                XmltvIcon(src="http://example.com/icon1", width=10, height=20),
                XmltvIcon(src="http://example.com/icon2", width=20, height=30),
            ],
            urls=[
                XmltvUrl(url="http://example.com/url1", system="example"),
                XmltvUrl(url="http://example.com/url2", system="example"),
            ],
        ),
    ],
    programmes=[
        XmltvProgramme(
            start="197001010000",
            channel="exampleid",
            titles=[
                XmltvTitle(title="exampletitle", lang="en"),
                XmltvTitle(title="exampletitle2", lang="ro"),
            ],
            stop="200001010000",
            pdc_start="197001010000",
            vps_start="197001010000",
            showview="0",
            videoplus="1",
            clumpidx="1/3",
            sub_titles=[
                XmltvSubTitle(sub_title="example movie", lang="en"),
                XmltvSubTitle(sub_title="example movie2", lang="at"),
            ],
            descs=[
                XmltvDesc(desc="ex. desc", lang="en"),
                XmltvDesc(desc="ex. desc2", lang="fr"),
            ],
            credits_=XmltvCredits(
                directors=[
                    XmltvDirector(
                        name="person1",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                    XmltvDirector(
                        name="person2",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                ],
                actors=[
                    XmltvActor(
                        name="person1",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                    XmltvActor(
                        name="person2",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                ],
                writers=[
                    XmltvWriter(
                        name="person1",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                    XmltvWriter(
                        name="person2",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                ],
                adapters=[
                    XmltvAdapter(
                        name="person1",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                    XmltvAdapter(
                        name="person2",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                ],
                producers=[
                    XmltvProducer(
                        name="person1",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                    XmltvProducer(
                        name="person2",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                ],
                composers=[
                    XmltvComposer(
                        name="person1",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                    XmltvComposer(
                        name="person2",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                ],
                editors=[
                    XmltvEditor(
                        name="person1",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                    XmltvEditor(
                        name="person2",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                ],
                presenters=[
                    XmltvPresenter(
                        name="person1",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                    XmltvPresenter(
                        name="person2",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                ],
                commentators=[
                    XmltvCommentator(
                        name="person1",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                    XmltvCommentator(
                        name="person2",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                ],
                guests=[
                    XmltvGuest(
                        name="person1",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                    XmltvGuest(
                        name="person2",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                ],
            ),
            date=XmltvDate(
                to_xmltv_date(datetime(1990, 1, 2, 3, 4, 5, tzinfo=ZoneInfo("UTC"))),
            ),
            categories=[
                XmltvCategory(category="cat1", lang="en"),
                XmltvCategory(category="cat2", lang="jp"),
            ],
            keywords=[XmltvKeyword("kw1", lang="en"), XmltvKeyword("kw2", lang="py")],
            language=XmltvLanguage("Py"),
            orig_language=XmltvOrigLanguage("Perl"),
            length=XmltvLength(length="180", units="hours"),
            icons=[
                XmltvIcon(src="http://example.com/icon1", width=10, height=20),
                XmltvIcon(src="http://example.com/icon2", width=20, height=30),
            ],
            urls=[
                XmltvUrl(url="http://example.com/url1", system="example"),
                XmltvUrl(url="http://example.com/url2", system="example"),
            ],
            countries=[
                XmltvCountry(country="US", lang="en"),
                XmltvCountry(country="GB", lang="en"),
            ],
            episode_nums=[
                XmltvEpisodeNum(episode_num="2/123.4/45.2/6", system="xmltv_ns"),
                XmltvEpisodeNum(episode_num="2/4-2", system="onscreen"),
            ],
            video=XmltvVideo(
                present=XmltvPresent("yes"),
                colour=XmltvColour("yes"),
                aspect=XmltvAspect("16:9"),
                quality=XmltvQuality("8x8"),
            ),
            audio=XmltvAudio(present=XmltvPresent("yes"), stereo=XmltvStereo("no")),
            previously_shown=XmltvPreviouslyShown(
                start="198001010011",
                channel="example2id",
            ),
            premiere=XmltvPremiere(premiere="Maybe", lang="en"),
            last_chance=XmltvLastChance(last_chance="Maybe", lang="en"),
            new=XmltvNew(),
            subtitles=[
                XmltvSubtitles(language=XmltvLanguage("en"), type_="teletext"),
                XmltvSubtitles(language=XmltvLanguage("en"), type_="onscreen"),
            ],
            ratings=[
                XmltvRating(
                    value=XmltvValue("12"),
                    system="example",
                    icons=[
                        XmltvIcon(src="http://example.com/icon1", width=10, height=20),
                        XmltvIcon(src="http://example.com/icon2", width=20, height=30),
                    ],
                ),
                XmltvRating(
                    value=XmltvValue("6"),
                    system="example",
                    icons=[
                        XmltvIcon(src="http://example.com/icon1", width=10, height=20),
                        XmltvIcon(src="http://example.com/icon2", width=20, height=30),
                    ],
                ),
            ],
            star_ratings=[
                XmltvStarRating(
                    value=XmltvValue("5/5"),
                    system="example",
                    icons=[
                        XmltvIcon(src="http://example.com/icon1", width=10, height=20),
                        XmltvIcon(src="http://example.com/icon2", width=20, height=30),
                    ],
                ),
            ],
            reviews=[
                XmltvReview(review="re1", type_="text", reviewer="me", lang="en"),
                XmltvReview(review="re2", type_="text", reviewer="me", lang="en"),
            ],
            images=[
                XmltvImage(
                    url="http://example.com/i1",
                    type_="poster",
                    size=1,
                    orient="P",
                    system="example",
                ),
                XmltvImage(
                    url="http://example.com/i2",
                    type_="still",
                    size=2,
                    orient="L",
                    system="example",
                ),
            ],
        ),
        XmltvProgramme(
            start="200001010000",
            channel="exampleid",
            titles=[
                XmltvTitle(title="exampletitle", lang="en"),
                XmltvTitle(title="exampletitle2", lang="ro"),
            ],
            stop="20380119031407",
            pdc_start="200001010000",
            vps_start="200001010000",
            showview="0",
            videoplus="1",
            clumpidx="1/3",
            sub_titles=[
                XmltvSubTitle(sub_title="example movie", lang="en"),
                XmltvSubTitle(sub_title="example movie2", lang="at"),
            ],
            descs=[
                XmltvDesc(desc="ex. desc", lang="en"),
                XmltvDesc(desc="ex. desc2", lang="fr"),
            ],
            credits_=XmltvCredits(
                directors=[
                    XmltvDirector(
                        name="person1",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                    XmltvDirector(
                        name="person2",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                ],
                actors=[
                    XmltvActor(
                        name="person1",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                    XmltvActor(
                        name="person2",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                ],
                writers=[
                    XmltvWriter(
                        name="person1",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                    XmltvWriter(
                        name="person2",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                ],
                adapters=[
                    XmltvAdapter(
                        name="person1",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                    XmltvAdapter(
                        name="person2",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                ],
                producers=[
                    XmltvProducer(
                        name="person1",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                    XmltvProducer(
                        name="person2",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                ],
                composers=[
                    XmltvComposer(
                        name="person1",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                    XmltvComposer(
                        name="person2",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                ],
                editors=[
                    XmltvEditor(
                        name="person1",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                    XmltvEditor(
                        name="person2",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                ],
                presenters=[
                    XmltvPresenter(
                        name="person1",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                    XmltvPresenter(
                        name="person2",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                ],
                commentators=[
                    XmltvCommentator(
                        name="person1",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                    XmltvCommentator(
                        name="person2",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                ],
                guests=[
                    XmltvGuest(
                        name="person1",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                    XmltvGuest(
                        name="person2",
                        images=[
                            XmltvImage(
                                url="http://example.com/i1",
                                type_="poster",
                                size=1,
                                orient="P",
                                system="example",
                            ),
                            XmltvImage(
                                url="http://example.com/i2",
                                type_="still",
                                size=2,
                                orient="L",
                                system="example",
                            ),
                        ],
                        urls=[
                            XmltvUrl(url="http://example.com/url1", system="example"),
                            XmltvUrl(url="http://example.com/url2", system="example"),
                        ],
                    ),
                ],
            ),
            date=XmltvDate(
                to_xmltv_date(datetime(1990, 1, 2, 3, 4, 5, tzinfo=ZoneInfo("UTC"))),
            ),
            categories=[
                XmltvCategory(category="cat1", lang="en"),
                XmltvCategory(category="cat2", lang="jp"),
            ],
            keywords=[XmltvKeyword("kw1", lang="en"), XmltvKeyword("kw2", lang="py")],
            language=XmltvLanguage("Py"),
            orig_language=XmltvOrigLanguage("Perl"),
            length=XmltvLength(length="180", units="hours"),
            icons=[
                XmltvIcon(src="http://example.com/icon1", width=10, height=20),
                XmltvIcon(src="http://example.com/icon2", width=20, height=30),
            ],
            urls=[
                XmltvUrl(url="http://example.com/url1", system="example"),
                XmltvUrl(url="http://example.com/url2", system="example"),
            ],
            countries=[
                XmltvCountry(country="US", lang="en"),
                XmltvCountry(country="GB", lang="en"),
            ],
            episode_nums=[
                XmltvEpisodeNum(episode_num="2/123.4/45.2/6", system="xmltv_ns"),
                XmltvEpisodeNum(episode_num="2/4-2", system="onscreen"),
            ],
            video=XmltvVideo(
                present=XmltvPresent("yes"),
                colour=XmltvColour("yes"),
                aspect=XmltvAspect("16:9"),
                quality=XmltvQuality("8x8"),
            ),
            audio=XmltvAudio(present=XmltvPresent("yes"), stereo=XmltvStereo("no")),
            previously_shown=XmltvPreviouslyShown(
                start="198001010011",
                channel="example2id",
            ),
            premiere=XmltvPremiere(premiere="Maybe", lang="en"),
            last_chance=XmltvLastChance(last_chance="Maybe", lang="en"),
            new=XmltvNew(),
            subtitles=[
                XmltvSubtitles(language=XmltvLanguage("en"), type_="teletext"),
                XmltvSubtitles(language=XmltvLanguage("en"), type_="onscreen"),
            ],
            ratings=[
                XmltvRating(
                    value=XmltvValue("12"),
                    system="example",
                    icons=[
                        XmltvIcon(src="http://example.com/icon1", width=10, height=20),
                        XmltvIcon(src="http://example.com/icon2", width=20, height=30),
                    ],
                ),
                XmltvRating(
                    value=XmltvValue("6"),
                    system="example",
                    icons=[
                        XmltvIcon(src="http://example.com/icon1", width=10, height=20),
                        XmltvIcon(src="http://example.com/icon2", width=20, height=30),
                    ],
                ),
            ],
            star_ratings=[
                XmltvStarRating(
                    value=XmltvValue("5/5"),
                    system="example",
                    icons=[
                        XmltvIcon(src="http://example.com/icon1", width=10, height=20),
                        XmltvIcon(src="http://example.com/icon2", width=20, height=30),
                    ],
                ),
            ],
            reviews=[
                XmltvReview(review="re1", type_="text", reviewer="me", lang="en"),
                XmltvReview(review="re2", type_="text", reviewer="me", lang="en"),
            ],
            images=[
                XmltvImage(
                    url="http://example.com/i1",
                    type_="poster",
                    size=1,
                    orient="P",
                    system="example",
                ),
                XmltvImage(
                    url="http://example.com/i2",
                    type_="still",
                    size=2,
                    orient="L",
                    system="example",
                ),
            ],
        ),
    ],
)
