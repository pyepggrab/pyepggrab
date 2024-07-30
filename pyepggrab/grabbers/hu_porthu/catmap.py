"""Category mappings for port.hu."""

from enum import Enum


class Cat(Enum):
    """Map ETSI EN 300 468 V1.14.1 categories to translated strings."""

    MOVIE_DRAMA = ("Movie/Drama", "Film/Dráma")
    DETECTIVE_THRILLER = ("Detective/Thriller", "Bűnügyi/Thriller")
    ADVENTURE_WESTERN_WAR = ("Adventure/Western/War", "Kaland/Western/Háborús")
    SCIENCEFICTION_FANTASY_HORROR = (
        "Science fiction/Fantasy/Horror",
        "Sci-fi/Fantasy/Horror",
    )
    COMEDY = ("Comedy", "Vígjáték")
    SOAP_MELODRAMA_FOLKLORIC = (
        "Soap/Melodrama/Folkloric",
        "Szappanopera/Melodráma/Folklór",
    )
    ROMANCE = ("Romance", "Romantikus")
    SERIOUS_CLASSICAL_RELIGIOUS_HISTORICAL_MOVIE_DRAMA = (
        "Serious/Classical/Religious/Historical movie/drama",
        "Komoly/Klasszikus/Vallási/Történelmi/Dráma",
    )
    ADULT_MOVIE_DRAMA = ("Adult movie/drama", "Felnőtt film/dráma")

    NEWS_CURRENTAFFAIRS = ("News/Current affairs", "Hírek/Aktualitások")
    NEWS_WEATHERREPORT = ("News/Weather report", "Hírek/Időjárásjelentés")
    NEWS_MAGAZINE = ("News Magazine", "Hírmagazin")
    DOCUMENTARY = ("Documentary", "Dokumentum")
    DISCUSSION_INTERVIEW_DEBATE = (
        "Discussion/Interview/Debate",
        "Beszélgetés/Interjú/Vita",
    )

    SHOW_GAMESHOW = ("Show/Game show", "Show/Játék show")
    GAMESHOW_QUIZ_CONTEST = ("Game show/Quiz/Contest", "Játék show/Kvíz/Verseny")
    VARIETYSHOW = ("Variety Show", "Revü")
    TALKSHOW = ("Talk show", "Beszélgetős műsor")

    SPORTS = ("Sports", "Sport")
    SPECIALEVENTS = ("Special events", "Különleges esemény")
    SPORTSMAGAZINES = ("Sports magazines", "Sport magazin")
    FOOTBALL_SOCCER = ("Football/Soccer", "Labdarúgás")
    TENNIS_SQUASH = ("Tennis/Squash", "Tenisz/Squash")
    TEAMSPORTS = ("Team sports", "Csapatsport")
    ATHLETICS = ("Athletics", "Atlétika")
    MOTORSPORT = ("Motor sport", "Motorsport")
    WATERSPORT = ("Water sport", "Vízisport")
    WINTERSPORTS = ("Winter sports", "Téli sport")
    EQUESTRIAN = ("Equestrian", "Lovas")
    MARTIALSPORTS = ("Martial sports", "Harci sport")

    CHILDRENS_YOUTH_PROGRAMMES = (
        "Children's/Youth programmes",
        "Gyerek/Ifjúsági program",
    )
    PRESCHOOL_CHILDRENS_PROGRAMMES = (
        "Pre-school children's programmes",
        "Óvodás program",
    )
    ENTERTAINMENT_PROGRAMMES_FOR_6TO14 = (
        "Entertainment programmes for 6 to 14",
        "Szórakoztató program 6-14 éveseknek",
    )
    ENTERTAINMENT_PROGRAMMES_FOR_10TO16 = (
        "Entertainment programmes for 10 to 16",
        "Szórakoztató program 10-16 éveseknek",
    )
    INFORMATIONAL_EDUCATIONAL_SCHOOL_PROGRAMMES = (
        "Informational/Educational/School programme",
        "Információs/Oktató/Iskolai program",
    )
    CARTOONS_PUPPETS = ("Cartoons/Puppets", "Animációs/Báb")

    MUSIC_BALLET_DANCE = ("Music/Ballet/Dance", "Zene/Balett/Tánc")
    ROCK_POP = ("Rock/Pop", "Rock/Pop")
    SERIOUSMUSIC_CLASSICALMUSIC = (
        "Serious Music/Classical music",
        "Komoly/Klasszikus zene",
    )
    FOLK_TRADITIONALMUSIC = ("Folk/Traditional music", "Népzene/Hagyományos zene")
    JAZZ = ("Jazz", "Jazz")
    MUSICAL_OPERA = ("Musical/Opera", "Musical/Opera")
    BALLET = ("Ballet", "Balett")

    ARTS_CULTURE = ("Arts/Culture", "Művészet/Kultúra")
    PERFORMINGARTS = ("Performing arts", "Előadóművészet")
    FINEARTS = ("Fine arts", "Képzőművészet")
    RELIGION = ("Religion", "Vallás")
    POPULARCULTURE_TRADITIONALARTS = (
        "Popular culture/Traditional arts",
        "Popkultúra/Hagyományos művészetek",
    )
    LITERATURE = ("Literature", "Irodalom")
    FILM_CINEMA = ("Film/Cinema", "Film/Mozi")
    EXPERIMENTALFILM_VIDEO = ("Experimental film/video", "Kísérleti film/Videó")
    BROADCASTING_PRESS = ("Broadcasting/Press", "Közvetítés/Sajtó")
    NEWMEDIA = ("New Media", "Új Média")
    ARTS_CULTURE_MAGAZINES = ("Arts/Culture magazines", "Művészeti/Kulturális magazin")
    FASHION = ("Fashion", "Divat")

    SOCIAL_POLITICALISSUES_ECONOMICS = (
        "Social/Political issues/Economics",
        "Szociális/Politikai/Gazdasági",
    )
    MAGAZINES_REPORTS_DOCUMENTARY = (
        "Magazines/Reports/Documentary",
        "Magazinok/Riportok/Dokumentumfilm",
    )
    ECONOMICS_SOCIAL_ADVISORY = (
        "Economics/Social advisory",
        "Gazdasági/Szociális tanácsadó",
    )
    REMARKABLE_PEOPLE = ("Remarkable People", "Híres Emberek")

    EDUCATION_SCIENCE_FACTUAL = (
        "Education/Science/Factual",
        "Oktatás/Tudomány/Tényfeltáró",
    )
    NATURE_ANIMALS_ENVIRONMENT = (
        "Nature/Animals/Environment",
        "Természet/Állatok/Környezet",
    )
    TECHNOLOGY_NATURALSCIENCES = (
        "Technology/Natural sciences",
        "Technika/Természettudományi",
    )
    MEDICINE_PHYSIOLOGY_PSYCHOLOGY = (
        "Medicine/Physiology/Psychology",
        "Orvosi/Élettani/Pszichológiai",
    )
    FOREIGNCOUNTRIES_EXPEDITIONS = (
        "Foreign Countries/Expeditions",
        "Idegen Országok/Felfedező utak",
    )
    SOCIAL_SPIRITUALSCIENCES = (
        "Social/Spiritual sciences",
        "Szociális/Lélek tudományok",
    )
    FURTHEREDUCATION = ("Further Education", "Továbbtanulás")
    LANGUAGES = ("Languages", "Nyelvek")

    LEISURE_HOBBIES = ("Leisure/Hobbies", "Szabadidő/Hobbi")
    TOURISM_TRAVEL = ("Tourism/Travel", "Turizmus/Utazás")
    HANDICRAFT = ("Handicraft", "Kézművesség")
    MOTORING = ("Motoring", "Autózás")
    FITNESS_HEALTH = ("Fitness & health", "Fitnesz & Egészség")
    COOKING = ("Cooking", "Főzés")
    ADVERTISEMENT_SHOPPING = ("Advertisement/Shopping", "Hirdetés/Vásárlás")
    GARDENING = ("Gardening", "Kertészkedés")


CATDICT = {
    "akció-horror": Cat.SCIENCEFICTION_FANTASY_HORROR,
    "akció-vígjáték": Cat.COMEDY,
    "akciófilm": Cat.MOVIE_DRAMA,
    "akciófilm-sorozat": Cat.MOVIE_DRAMA,
    "akcióthriller": Cat.DETECTIVE_THRILLER,
    "akcióvígjáték-sorozat": Cat.COMEDY,
    "animációs akciósorozat": Cat.MOVIE_DRAMA,
    "animációs film": Cat.MOVIE_DRAMA,
    "animációs kalandfilm": Cat.MOVIE_DRAMA,
    "animációs minisorozat": Cat.MOVIE_DRAMA,
    "animációs rövidfilm": Cat.MOVIE_DRAMA,
    "animációs sorozat": Cat.MOVIE_DRAMA,
    "animációs vígjáték": Cat.MOVIE_DRAMA,
    "animációs vígjátéksorozat": Cat.MOVIE_DRAMA,
    "autós magazin": Cat.MOTORING,
    "bábfilm": Cat.CARTOONS_PUPPETS,
    "bábfilmsorozat": Cat.CARTOONS_PUPPETS,
    "bűnügyi film": Cat.DETECTIVE_THRILLER,
    "bűnügyi tévéfilmsorozat": Cat.DETECTIVE_THRILLER,
    "családi animációs film": Cat.CHILDRENS_YOUTH_PROGRAMMES,
    "családi film": Cat.CHILDRENS_YOUTH_PROGRAMMES,
    "családi filmsorozat": Cat.CHILDRENS_YOUTH_PROGRAMMES,
    "családi kalandfilm": Cat.CHILDRENS_YOUTH_PROGRAMMES,
    "családi vígjáték": Cat.CHILDRENS_YOUTH_PROGRAMMES,
    "dokumentum játékfilm": Cat.MOVIE_DRAMA,
    "dokumentumfilm": Cat.EDUCATION_SCIENCE_FACTUAL,
    "dokumentumfilm összeállítás": Cat.EDUCATION_SCIENCE_FACTUAL,
    "dokumentumfilm sorozat": Cat.EDUCATION_SCIENCE_FACTUAL,
    "dokureality-sorozat": Cat.SHOW_GAMESHOW,
    "dokusorozat": Cat.EDUCATION_SCIENCE_FACTUAL,
    "dráma": Cat.MOVIE_DRAMA,
    "dráma minisorozat": Cat.MOVIE_DRAMA,
    "drámasorozat": Cat.MOVIE_DRAMA,
    "életmódmagazin": Cat.LEISURE_HOBBIES,
    "életrajzi dráma": Cat.MAGAZINES_REPORTS_DOCUMENTARY,
    "életrajzi film": Cat.MAGAZINES_REPORTS_DOCUMENTARY,
    "életrajzi minisorozat": Cat.MAGAZINES_REPORTS_DOCUMENTARY,
    "erotikus-thriller": Cat.ADULT_MOVIE_DRAMA,
    "extrém vetélkedő": Cat.GAMESHOW_QUIZ_CONTEST,
    "fantasy": Cat.SCIENCEFICTION_FANTASY_HORROR,
    "fantasy sorozat": Cat.SCIENCEFICTION_FANTASY_HORROR,
    "fantasztikus akciófilm": Cat.SCIENCEFICTION_FANTASY_HORROR,
    "fantasztikus film": Cat.SCIENCEFICTION_FANTASY_HORROR,
    "fantasztikus kalandfilm": Cat.ADVENTURE_WESTERN_WAR,
    "fantasztikus thriller": Cat.DETECTIVE_THRILLER,
    "fekete komédia": Cat.COMEDY,
    "fikciós dokumentumfilm": Cat.EDUCATION_SCIENCE_FACTUAL,
    "film": Cat.MOVIE_DRAMA,
    "filmdráma": Cat.MOVIE_DRAMA,
    "filmesszé": Cat.MOVIE_DRAMA,
    "filmetűd": Cat.MOVIE_DRAMA,
    "filmsorozat": Cat.MOVIE_DRAMA,
    "filmszatíra": Cat.MOVIE_DRAMA,
    "főzős műsor": Cat.COOKING,
    "főzőshow": Cat.SHOW_GAMESHOW,
    "gála": Cat.MUSIC_BALLET_DANCE,
    "gasztro-reality": Cat.SHOW_GAMESHOW,
    "gasztronómiai műsor": Cat.COOKING,
    "gasztroshow": Cat.COOKING,
    "gazdasági műsor": Cat.SOCIAL_POLITICALISSUES_ECONOMICS,
    "gengszterfilm": Cat.DETECTIVE_THRILLER,
    "gyerekfilm sorozat": Cat.CHILDRENS_YOUTH_PROGRAMMES,
    "gyerekműsor": Cat.CHILDRENS_YOUTH_PROGRAMMES,
    "gyermekfilm": Cat.CHILDRENS_YOUTH_PROGRAMMES,
    "háborús filmdráma": Cat.ADVENTURE_WESTERN_WAR,
    "háborús minisorozat": Cat.ADVENTURE_WESTERN_WAR,
    "háborús vígjáték": Cat.ADVENTURE_WESTERN_WAR,
    "hírműsor": Cat.NEWS_CURRENTAFFAIRS,
    "horror": Cat.SCIENCEFICTION_FANTASY_HORROR,
    "horror-dráma": Cat.MOVIE_DRAMA,
    "horror-vígjáték": Cat.COMEDY,
    "horrorsorozat": Cat.SCIENCEFICTION_FANTASY_HORROR,
    "ifjúsági film": Cat.CHILDRENS_YOUTH_PROGRAMMES,
    "ifjúsági filmsorozat": Cat.CHILDRENS_YOUTH_PROGRAMMES,
    "ifjúsági kalandfilm": Cat.CHILDRENS_YOUTH_PROGRAMMES,
    "ifjúsági kalandfilmsorozat": Cat.CHILDRENS_YOUTH_PROGRAMMES,
    "ifjúsági vígjáték": Cat.COMEDY,
    "Információs műsor": Cat.DISCUSSION_INTERVIEW_DEBATE,
    "interaktív filmsorozat": Cat.MOVIE_DRAMA,
    "ismeretterjesztő film": Cat.EDUCATION_SCIENCE_FACTUAL,
    "ismeretterjesztő filmsorozat": Cat.EDUCATION_SCIENCE_FACTUAL,
    "ismeretterjesztő magazin": Cat.MAGAZINES_REPORTS_DOCUMENTARY,
    "ismeretterjesztő műsor": Cat.EDUCATION_SCIENCE_FACTUAL,
    "Ismeretterjesztő sorozat": Cat.EDUCATION_SCIENCE_FACTUAL,
    "játékfilm": Cat.MOVIE_DRAMA,
    "kabaréshow": Cat.SHOW_GAMESHOW,
    "kaland minisorozat": Cat.ADVENTURE_WESTERN_WAR,
    "kalandfilm": Cat.ADVENTURE_WESTERN_WAR,
    "kalandfilmsorozat": Cat.ADVENTURE_WESTERN_WAR,
    "karatefilm": Cat.MOVIE_DRAMA,
    "katasztrófa film": Cat.SERIOUS_CLASSICAL_RELIGIOUS_HISTORICAL_MOVIE_DRAMA,
    "kísérleti film": Cat.EXPERIMENTALFILM_VIDEO,
    "kisfilm-összeállítás": Cat.MOVIE_DRAMA,
    "kisjátékfilm": Cat.MOVIE_DRAMA,
    "komédia": Cat.COMEDY,
    "komédia sorozat": Cat.COMEDY,
    "komolyzenei film": Cat.SERIOUSMUSIC_CLASSICALMUSIC,
    "komolyzenei műsor": Cat.SERIOUSMUSIC_CLASSICALMUSIC,
    "koncertfilm": Cat.MUSIC_BALLET_DANCE,
    "közéleti-kulturális magazin": Cat.DISCUSSION_INTERVIEW_DEBATE,
    "közlekedésbiztonsági sorozat": Cat.NEWS_CURRENTAFFAIRS,
    "krimi": Cat.DETECTIVE_THRILLER,
    "krimi minisorozat": Cat.DETECTIVE_THRILLER,
    "krimi vígjáték": Cat.COMEDY,
    "krimi-dráma": Cat.MOVIE_DRAMA,
    "krimi-vígjáték": Cat.COMEDY,
    "krimisorozat": Cat.DETECTIVE_THRILLER,
    "kulináris krimi": Cat.DETECTIVE_THRILLER,
    "kulturális magazin": Cat.MAGAZINES_REPORTS_DOCUMENTARY,
    "kvíz-show": Cat.GAMESHOW_QUIZ_CONTEST,
    "magazinműsor": Cat.MAGAZINES_REPORTS_DOCUMENTARY,
    "melodráma": Cat.SOAP_MELODRAMA_FOLKLORIC,
    "mesefilm": Cat.CHILDRENS_YOUTH_PROGRAMMES,
    "mesejáték": Cat.CHILDRENS_YOUTH_PROGRAMMES,
    "mesesorozat": Cat.CHILDRENS_YOUTH_PROGRAMMES,
    "miniportré-sorozat": Cat.MAGAZINES_REPORTS_DOCUMENTARY,
    "minisorozat": Cat.MOVIE_DRAMA,
    "misztikus film": Cat.SCIENCEFICTION_FANTASY_HORROR,
    "misztikus sorozat": Cat.SCIENCEFICTION_FANTASY_HORROR,
    "misztikus thriller": Cat.DETECTIVE_THRILLER,
    "musical": Cat.MUSICAL_OPERA,
    "műveltségi vetélkedő": Cat.GAMESHOW_QUIZ_CONTEST,
    "művészeti magazin": Cat.ARTS_CULTURE_MAGAZINES,
    "művészeti műsor": Cat.ARTS_CULTURE,
    "művészeti portésorozat": Cat.ARTS_CULTURE_MAGAZINES,
    "opera": Cat.MUSICAL_OPERA,
    "operafilm": Cat.MUSICAL_OPERA,
    "operettfilm": Cat.MUSICAL_OPERA,
    "párkapcsolati kalauz": Cat.ADULT_MOVIE_DRAMA,
    "politikai dráma": Cat.MOVIE_DRAMA,
    "politikai műsor": Cat.SOCIAL_POLITICALISSUES_ECONOMICS,
    "politikai thriller": Cat.DETECTIVE_THRILLER,
    "portréfilm": Cat.MAGAZINES_REPORTS_DOCUMENTARY,
    "pszichothriller": Cat.DETECTIVE_THRILLER,
    "rajzfilm": Cat.CHILDRENS_YOUTH_PROGRAMMES,
    "rajzfilm összeállítás": Cat.CHILDRENS_YOUTH_PROGRAMMES,
    "rajzfilm sorozat": Cat.CHILDRENS_YOUTH_PROGRAMMES,
    "reality műsor": Cat.GAMESHOW_QUIZ_CONTEST,
    "reality show": Cat.GAMESHOW_QUIZ_CONTEST,
    "reality vígjátéksorozat": Cat.GAMESHOW_QUIZ_CONTEST,
    "reality-sorozat": Cat.GAMESHOW_QUIZ_CONTEST,
    "reklámfilm": Cat.ADVERTISEMENT_SHOPPING,
    "riportfilm": Cat.MAGAZINES_REPORTS_DOCUMENTARY,
    "riportfilm-sorozat": Cat.MAGAZINES_REPORTS_DOCUMENTARY,
    "riportműsor": Cat.MAGAZINES_REPORTS_DOCUMENTARY,
    "road movie": Cat.MOVIE_DRAMA,
    "romantikus dráma": Cat.ROMANCE,
    "romantikus film": Cat.ROMANCE,
    "romantikus kalandfilm": Cat.ADVENTURE_WESTERN_WAR,
    "romantikus komédia": Cat.COMEDY,
    "romantikus sorozat": Cat.ROMANCE,
    "romantikus thriller": Cat.DETECTIVE_THRILLER,
    "romantikus vígjáték": Cat.COMEDY,
    "rövidfilm": Cat.MOVIE_DRAMA,
    "rövidfilm összeállítás": Cat.MOVIE_DRAMA,
    "rövidfilmsorozat": Cat.MOVIE_DRAMA,
    "sci-fi": Cat.SCIENCEFICTION_FANTASY_HORROR,
    "sci-fi akciófilm": Cat.SCIENCEFICTION_FANTASY_HORROR,
    "sci-fi dráma": Cat.SCIENCEFICTION_FANTASY_HORROR,
    "sci-fi kalandfilm": Cat.ADVENTURE_WESTERN_WAR,
    "sci-fi sorozat": Cat.SCIENCEFICTION_FANTASY_HORROR,
    "sci-fi vígjáték": Cat.COMEDY,
    "show műsor": Cat.SHOW_GAMESHOW,
    "show-műsor": Cat.SHOW_GAMESHOW,
    "sportfilm": Cat.SPORTS,
    "sportműsor": Cat.SPORTS,
    "stand-up comedy": Cat.COMEDY,
    "szabadidős műsor": Cat.LEISURE_HOBBIES,
    "szappanopera": Cat.SOAP_MELODRAMA_FOLKLORIC,
    "szatíra": Cat.MOVIE_DRAMA,
    "szatirikus vígjáték": Cat.MOVIE_DRAMA,
    "szélhámosfilm": Cat.MOVIE_DRAMA,
    "színházi felvétel": Cat.ARTS_CULTURE,
    "színházi közvetítés": Cat.ARTS_CULTURE,
    "színházi magazin": Cat.ARTS_CULTURE_MAGAZINES,
    "szórakoztató műsor": Cat.COMEDY,
    "szórakoztató sorozat": Cat.COMEDY,
    "szórakoztató vetélkedő": Cat.GAMESHOW_QUIZ_CONTEST,
    "talk show": Cat.TALKSHOW,
    "telenovella": Cat.MOVIE_DRAMA,
    "televíziós vásárlási műsorablak": Cat.ADVERTISEMENT_SHOPPING,
    "természetfilm": Cat.NATURE_ANIMALS_ENVIRONMENT,
    "természetfilm sorozat": Cat.NATURE_ANIMALS_ENVIRONMENT,
    "tévéfilm": Cat.MOVIE_DRAMA,
    "tévéfilmsorozat": Cat.MOVIE_DRAMA,
    "tévéjáték": Cat.MOVIE_DRAMA,
    "thriller": Cat.DETECTIVE_THRILLER,
    "thriller minisorozat": Cat.DETECTIVE_THRILLER,
    "thrillersorozat": Cat.DETECTIVE_THRILLER,
    "történelmi dokumentumfilm": Cat.EDUCATION_SCIENCE_FACTUAL,
    "történelmi dokumentumfilm-sorozat": Cat.EDUCATION_SCIENCE_FACTUAL,
    "történelmi dráma": Cat.SERIOUS_CLASSICAL_RELIGIOUS_HISTORICAL_MOVIE_DRAMA,
    "történelmi film": Cat.SERIOUS_CLASSICAL_RELIGIOUS_HISTORICAL_MOVIE_DRAMA,
    "történelmi filmsorozat": Cat.SERIOUS_CLASSICAL_RELIGIOUS_HISTORICAL_MOVIE_DRAMA,
    "történelmi kalandfilm": Cat.ADVENTURE_WESTERN_WAR,
    "történelmi sorozat": Cat.SERIOUS_CLASSICAL_RELIGIOUS_HISTORICAL_MOVIE_DRAMA,
    "történelmi vígjáték": Cat.COMEDY,
    "tragikomédia": Cat.COMEDY,
    "útifilm": Cat.FOREIGNCOUNTRIES_EXPEDITIONS,
    "útifilm-sorozat": Cat.FOREIGNCOUNTRIES_EXPEDITIONS,
    "vallási műsor": Cat.RELIGION,
    "valóságshow": Cat.GAMESHOW_QUIZ_CONTEST,
    "versösszeállítás": Cat.LITERATURE,
    "vetélkedő": Cat.GAMESHOW_QUIZ_CONTEST,
    "videófilmösszeállítás": Cat.MOVIE_DRAMA,
    "videóklipek": Cat.MOVIE_DRAMA,
    "vígjáték": Cat.COMEDY,
    "vígjátéksorozat": Cat.COMEDY,
    "vígopera": Cat.MUSICAL_OPERA,
    "werkfilm": Cat.MOVIE_DRAMA,
    "western": Cat.ADVENTURE_WESTERN_WAR,
    "western-vígjáték": Cat.COMEDY,
    "westernsorozat": Cat.ADVENTURE_WESTERN_WAR,
    "zenefilm": Cat.MUSIC_BALLET_DANCE,
    "zenei sorozat": Cat.MUSIC_BALLET_DANCE,
    "zenés dráma": Cat.MOVIE_DRAMA,
    "zenés film": Cat.MOVIE_DRAMA,
    "zenés műsor": Cat.MUSIC_BALLET_DANCE,
    "zenés vígjáték": Cat.COMEDY,
}
