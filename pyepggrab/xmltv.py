"""Classes to create XMLTV XML."""

import datetime
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from lxml import etree

from pyepggrab.utils import remove_suffix

try:
    from typing import override  # type: ignore # noqa: F401, RUF100
except ImportError:
    from typing_extensions import override  # type: ignore # noqa: F401, RUF100


GEN_NAME = Path(sys.argv[0]).stem
GEN_URL = "https://github.com/pyepggrab/pyepggrab"


def to_xmltv_date(datetime: datetime.datetime) -> str:
    """`datetime` to XMLTV date format."""
    return datetime.strftime("%Y%m%d%H%M%S %z")


@dataclass(eq=True)
class _XmltvBase:
    """Base class for all XML objects."""

    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        """Convert the object to XML representation."""
        raise NotImplementedError()

    def _attrs(self, attrs: List[str]) -> Dict[str, str]:
        """Get `attrs` and change them to conform to the XML DTD."""
        ret: Dict[str, str] = {}
        for k, v in vars(self).items():
            if v is not None and k in attrs:
                xkey = remove_suffix(k, "_")  # Used by id_, type_, ...
                xkey = xkey.replace("_", "-")
                ret[xkey] = str(v)
        return ret

    def _to_xml(
        self,
        parent: Optional[etree._Element],
        tag_name: str,
        text: Optional[str] = None,
        attribs: Optional[List[str]] = None,
        subelements: Optional[List[Optional["_XmltvBase"]]] = None,
    ) -> etree._Element:
        """Convert the object to XML representation.

        :param parent: parent element
        :param tag_name: name of the tag that the object represents
        :param text: contents of the tag
        :param attribs: list of attributes that should be included in the XML
        :param subelements: children of this element
        """
        attribs = attribs if attribs else []
        subelements = subelements if subelements else []

        attrs = self._attrs(attribs)
        if parent is not None:
            xelem = etree.SubElement(parent, tag_name, attrs)
        else:
            xelem = etree.Element(tag_name, attrs)
        xelem.text = text
        for sube in subelements:
            if sube is not None:
                sube.to_xml(xelem)
        return xelem

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return False

        for (this_key, this_val), (other_key, other_val) in zip(
            vars(self).items(),
            vars(__o).items(),
        ):
            # lists are considered equal
            # if the elements are in the same order and are equal
            if this_key != other_key or this_val != other_val:
                return False
        return True

    def to_str(self, pretty_print: bool = True) -> str:
        """Convert the object to an XML str."""
        xmlbytes: bytes = etree.tostring(
            self.to_xml(),
            encoding="UTF-8",
            pretty_print=pretty_print,
        )
        return xmlbytes.decode("UTF-8")

    def __str__(self) -> str:
        return self.to_str()


@dataclass
class XmltvDisplayName(_XmltvBase):
    """`display-name` in XMLTV XML."""

    display_name: str
    lang: Optional[str] = None

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "display-name", self.display_name, ["lang"])


@dataclass
class XmltvUrl(_XmltvBase):
    """`url` in XMLTV XML."""

    url: str
    system: Optional[str] = None

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "url", self.url, ["system"])


@dataclass
class XmltvIcon(_XmltvBase):
    """`icon` in XMLTV XML."""

    src: str
    width: Optional[int] = None
    height: Optional[int] = None

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "icon", attribs=["src", "width", "height"])


@dataclass
class XmltvChannel(_XmltvBase):
    """`channel` in XMLTV XML."""

    id_: str
    display_names: List[XmltvDisplayName]
    icons: List[XmltvIcon] = field(default_factory=list)
    urls: List[XmltvUrl] = field(default_factory=list)

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(
            parent,
            "channel",
            attribs=["id_"],
            subelements=[*self.display_names, *self.icons, *self.urls],
        )


@dataclass
class XmltvTitle(_XmltvBase):
    """`title` in XMLTV XML."""

    title: str
    lang: Optional[str] = None

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "title", self.title, ["lang"])


@dataclass
class XmltvSubTitle(_XmltvBase):
    """`sub-title` in XMLTV XML."""

    sub_title: str
    lang: Optional[str] = None

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "sub-title", self.sub_title, ["lang"])


@dataclass
class XmltvDesc(_XmltvBase):
    """`desc` in XMLTV XML."""

    desc: str
    lang: Optional[str] = None

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "desc", self.desc, ["lang"])


@dataclass
class XmltvImage(_XmltvBase):
    """`image` in XMLTV XML."""

    url: str
    type_: Optional[str] = None
    size: Optional[int] = None
    orient: Optional[str] = None
    system: Optional[str] = None

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(
            parent,
            "image",
            self.url,
            ["type_", "size", "orient", "system"],
        )


@dataclass
class _XmltvNameImgUrl(_XmltvBase):
    """Base class for XML objects that contain `name`, `images`, `urls`."""

    _tag_name: str
    name: Optional[str] = None
    images: List[XmltvImage] = field(default_factory=list)
    urls: List[XmltvUrl] = field(default_factory=list)

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(
            parent,
            self._tag_name,
            self.name,
            subelements=[*self.images, *self.urls],
        )


@dataclass
class XmltvDirector(_XmltvNameImgUrl):
    """`director` in XMLTV XML."""

    _tag_name: str = field(default="director", init=False)


@dataclass
class XmltvActor(_XmltvNameImgUrl):
    """`actor` in XMLTV XML."""

    _tag_name: str = field(default="actor", init=False)
    role: Optional[str] = None
    guest: Optional[str] = None

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(
            parent,
            self._tag_name,
            self.name,
            attribs=["role", "guest"],
            subelements=[*self.images, *self.urls],
        )


@dataclass
class XmltvWriter(_XmltvNameImgUrl):
    """`writer` in XMLTV XML."""

    _tag_name: str = field(default="writer", init=False)


@dataclass
class XmltvAdapter(_XmltvNameImgUrl):
    """`adapter` in XMLTV XML."""

    _tag_name: str = field(default="adapter", init=False)


@dataclass
class XmltvProducer(_XmltvNameImgUrl):
    """`producer` in XMLTV XML."""

    _tag_name: str = field(default="producer", init=False)


@dataclass
class XmltvComposer(_XmltvNameImgUrl):
    """`composer` in XMLTV XML."""

    _tag_name: str = field(default="composer", init=False)


@dataclass
class XmltvEditor(_XmltvNameImgUrl):
    """`editor` in XMLTV XML."""

    _tag_name: str = field(default="editor", init=False)


@dataclass
class XmltvPresenter(_XmltvNameImgUrl):
    """`presenter` in XMLTV XML."""

    _tag_name: str = field(default="presenter", init=False)


@dataclass
class XmltvCommentator(_XmltvNameImgUrl):
    """`commentator` in XMLTV XML."""

    _tag_name: str = field(default="commentator", init=False)


@dataclass
class XmltvGuest(_XmltvNameImgUrl):
    """`guest` in XMLTV XML."""

    _tag_name: str = field(default="guest", init=False)


@dataclass
class XmltvCredits(_XmltvBase):
    """`credits` in XMLTV XML."""

    directors: List[XmltvDirector] = field(default_factory=list)
    actors: List[XmltvActor] = field(default_factory=list)
    writers: List[XmltvWriter] = field(default_factory=list)
    adapters: List[XmltvAdapter] = field(default_factory=list)
    producers: List[XmltvProducer] = field(default_factory=list)
    composers: List[XmltvComposer] = field(default_factory=list)
    editors: List[XmltvEditor] = field(default_factory=list)
    presenters: List[XmltvPresenter] = field(default_factory=list)
    commentators: List[XmltvCommentator] = field(default_factory=list)
    guests: List[XmltvGuest] = field(default_factory=list)

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(
            parent,
            "credits",
            subelements=[
                *self.directors,
                *self.actors,
                *self.writers,
                *self.adapters,
                *self.producers,
                *self.composers,
                *self.editors,
                *self.presenters,
                *self.commentators,
                *self.guests,
            ],
        )


@dataclass
class XmltvDate(_XmltvBase):
    """`date` in XMLTV XML."""

    date: str

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "date", self.date)


@dataclass
class XmltvCategory(_XmltvBase):
    """`category` in XMLTV XML."""

    category: str
    lang: Optional[str] = None

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "category", self.category, ["lang"])


@dataclass
class XmltvKeyword(_XmltvBase):
    """`keyword` in XMLTV XML."""

    keyword: str
    lang: Optional[str] = None

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "keyword", self.keyword, ["lang"])


@dataclass
class XmltvLanguage(_XmltvBase):
    """`language` in XMLTV XML."""

    lang: str

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "language", self.lang)


@dataclass
class XmltvOrigLanguage(_XmltvBase):
    """`orig-language` in XMLTV XML."""

    lang: str

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "orig-language", self.lang)


@dataclass
class XmltvLength(_XmltvBase):
    """`length` in XMLTV XML."""

    length: str
    units: str

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "length", self.length, ["units"])


@dataclass
class XmltvCountry(_XmltvBase):
    """`country` in XMLTV XML."""

    country: str
    lang: str

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "country", self.country, ["lang"])


@dataclass
class XmltvEpisodeNum(_XmltvBase):
    """`episode-num` in XMLTV XML."""

    episode_num: str
    system: str = "onscreen"

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "episode-num", self.episode_num, ["system"])


@dataclass
class XmltvPresent(_XmltvBase):
    """`present` in XMLTV XML."""

    present: str

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "present", self.present)


@dataclass
class XmltvColour(_XmltvBase):
    """`colour` in XMLTV XML."""

    colour: str

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "colour", self.colour)


@dataclass
class XmltvAspect(_XmltvBase):
    """`aspect` in XMLTV XML."""

    aspect: str

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "aspect", self.aspect)


@dataclass
class XmltvQuality(_XmltvBase):
    """`quality` in XMLTV XML."""

    quality: str

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "quality", self.quality)


@dataclass
class XmltvVideo(_XmltvBase):
    """`video` in XMLTV XML."""

    present: Optional[XmltvPresent] = None
    colour: Optional[XmltvColour] = None
    aspect: Optional[XmltvAspect] = None
    quality: Optional[XmltvQuality] = None

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(
            parent,
            "video",
            subelements=[self.present, self.colour, self.aspect, self.quality],
        )


@dataclass
class XmltvStereo(_XmltvBase):
    """`stereo` in XMLTV XML."""

    stereo: str

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "stereo", self.stereo)


@dataclass
class XmltvAudio(_XmltvBase):
    """`audio` in XMLTV XML."""

    present: Optional[XmltvPresent] = None
    stereo: Optional[XmltvStereo] = None

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "audio", subelements=[self.present, self.stereo])


@dataclass
class XmltvPreviouslyShown(_XmltvBase):
    """`previously-shown` in XMLTV XML."""

    start: Optional[str] = None
    channel: Optional[str] = None

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "previously-shown", attribs=["start", "channel"])


@dataclass
class XmltvPremiere(_XmltvBase):
    """`premiere` in XMLTV XML."""

    premiere: Optional[str] = None
    lang: Optional[str] = None

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "premiere", self.premiere, ["lang"])


@dataclass
class XmltvLastChance(_XmltvBase):
    """`last-chance` in XMLTV XML."""

    last_chance: Optional[str] = None
    lang: Optional[str] = None

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "last-chance", self.last_chance, ["lang"])


@dataclass
class XmltvNew(_XmltvBase):
    """`new` in XMLTV XML."""

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "new")


@dataclass
class XmltvSubtitles(_XmltvBase):
    """`subtitles` in XMLTV XML."""

    language: Optional[XmltvLanguage] = None
    type_: Optional[str] = None

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(
            parent,
            "subtitles",
            attribs=["type_"],
            subelements=[self.language],
        )


@dataclass
class XmltvValue(_XmltvBase):
    """`value` in XMLTV XML."""

    value: str

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(parent, "value", self.value)


@dataclass
class XmltvRating(_XmltvBase):
    """`rating` in XMLTV XML."""

    value: XmltvValue
    system: Optional[str] = None
    icons: List[XmltvIcon] = field(default_factory=list)

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(
            parent,
            "rating",
            attribs=["system"],
            subelements=[self.value, *self.icons],
        )


@dataclass
class XmltvStarRating(_XmltvBase):
    """`star-rating` in XMLTV XML."""

    value: XmltvValue
    system: Optional[str] = None
    icons: List[XmltvIcon] = field(default_factory=list)

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(
            parent,
            "star-rating",
            attribs=["system"],
            subelements=[self.value, *self.icons],
        )


@dataclass
class XmltvReview(_XmltvBase):
    """`review` in XMLTV XML."""

    review: str
    type_: str
    source: Optional[str] = None
    reviewer: Optional[str] = None
    lang: Optional[str] = None

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(
            parent,
            "review",
            self.review,
            attribs=["type_", "source", "reviewer", "lang"],
        )


@dataclass
class XmltvProgramme(_XmltvBase):
    """`programme` in XMLTV XML."""

    start: str
    channel: str
    titles: List[XmltvTitle]
    stop: Optional[str] = None
    pdc_start: Optional[str] = None
    vps_start: Optional[str] = None
    showview: Optional[str] = None
    videoplus: Optional[str] = None
    clumpidx: str = "0/1"
    sub_titles: List[XmltvSubTitle] = field(default_factory=list)
    descs: List[XmltvDesc] = field(default_factory=list)
    credits_: Optional[XmltvCredits] = None
    date: Optional[XmltvDate] = None
    categories: List[XmltvCategory] = field(default_factory=list)
    keywords: List[XmltvKeyword] = field(default_factory=list)
    language: Optional[XmltvLanguage] = None
    orig_language: Optional[XmltvOrigLanguage] = None
    length: Optional[XmltvLength] = None
    icons: List[XmltvIcon] = field(default_factory=list)
    urls: List[XmltvUrl] = field(default_factory=list)
    countries: List[XmltvCountry] = field(default_factory=list)
    episode_nums: List[XmltvEpisodeNum] = field(default_factory=list)
    video: Optional[XmltvVideo] = None
    audio: Optional[XmltvAudio] = None
    previously_shown: Optional[XmltvPreviouslyShown] = None
    premiere: Optional[XmltvPremiere] = None
    last_chance: Optional[XmltvLastChance] = None
    new: Optional[XmltvNew] = None
    subtitles: List[XmltvSubtitles] = field(default_factory=list)
    ratings: List[XmltvRating] = field(default_factory=list)
    star_ratings: List[XmltvStarRating] = field(default_factory=list)
    reviews: List[XmltvReview] = field(default_factory=list)
    images: List[XmltvImage] = field(default_factory=list)

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(
            parent,
            "programme",
            attribs=[
                "start",
                "stop",
                "pdc_start",
                "vps_start",
                "showview",
                "videoplus",
                "channel",
                "clumpidx",
            ],
            subelements=[
                *self.titles,
                *self.sub_titles,
                *self.descs,
                self.credits_,
                self.date,
                *self.categories,
                *self.keywords,
                self.language,
                self.orig_language,
                self.length,
                *self.icons,
                *self.urls,
                *self.countries,
                *self.episode_nums,
                self.video,
                self.audio,
                self.previously_shown,
                self.premiere,
                self.last_chance,
                self.new,
                *self.subtitles,
                *self.ratings,
                *self.star_ratings,
                *self.reviews,
                *self.images,
            ],
        )


@dataclass
class XmltvTv(_XmltvBase):
    """`tv` in XMLTV XML."""

    date: Optional[str] = None
    source_info_url: Optional[str] = None
    source_info_name: Optional[str] = None
    source_data_url: Optional[str] = None
    generator_info_name: str = GEN_NAME
    generator_info_url: str = GEN_URL
    channels: List[XmltvChannel] = field(default_factory=list)
    programmes: List[XmltvProgramme] = field(default_factory=list)

    @override
    def to_xml(self, parent: Optional[etree._Element] = None) -> etree._Element:
        return self._to_xml(
            parent,
            "tv",
            attribs=[
                "date",
                "source_info_url",
                "source_info_name",
                "source_data_url",
                "generator_info_name",
                "generator_info_url",
            ],
            subelements=[*self.channels, *self.programmes],
        )

    @override
    def to_str(self, pretty_print: bool = True) -> str:
        xmlbytes: bytes = etree.tostring(
            self.to_xml(),
            encoding="UTF-8",
            pretty_print=pretty_print,
            xml_declaration=True,
            doctype='<!DOCTYPE tv SYSTEM "xmltv.dtd">',
        )
        return xmlbytes.decode("UTF-8")

    def to_xmltree(self) -> etree._ElementTree:
        """Convert the object to XML representation with header and doctype."""
        header = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<!DOCTYPE tv SYSTEM "xmltv.dtd"><tv/>'
        )
        root = etree.XML(header.encode("utf-8"))
        return etree.ElementTree(self.to_xml(root))
