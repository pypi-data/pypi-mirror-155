import enum
import dataclasses


class SeptuagintBookCode(enum.Enum):
    genesis = "gn"
    exodus = "ex"
    leviticus = "lv"
    numbers = "nm"
    deuteronomy = "dt"
    joshua = "jo"
    judges = "jgs"
    ruth = "ru"
    samuel1 = "1sm"
    samuel2 = "2sm"
    kings1 = "1kgs"
    kings2 = "2kgs"
    chronicles1 = "1chr"
    chronicles2 = "2chr"
    esdras = "1esd"
    ezra = "ezr"
    nehemiah = "neh"
    tobit = "tb"
    judith = "jdt"
    esther = "est"
    maccabees1 = "1mc"
    maccabees2 = "2mc"
    psalms = "ps"
    job = "jb"
    proverbs = "prv"
    ecclesiastes = "eccl"
    song_of_songs = "sg"
    wisdom_of_solomon = "ws"
    wisdom_of_sirach = "sir"
    hosea = "hos"
    amos = "am"
    micah = "mi"
    joel = "jl"
    obadiah = "ob"
    jonah = "jon"
    nahum = "na"
    habakkuk = "hb"
    zephaniah = "zep"
    haggai = "hg"
    zechariah = "zec"
    malachi = "mal"
    isaiah = "is"
    jeremiah = "jer"
    baruch = "bar"
    lamentations = "lam"
    epistle_of_jeremiah = "eoj"
    ezekiel = "ez"
    daniel = "dn"
    prayer_of_manasseh = "poman"


class NewTestamentBookCode(enum.Enum):
    matthew = "mt"
    mark = "mk"
    luke = "lk"
    john = "jn"
    acts = "acts"
    romans = "rom"
    corinthians1 = "1cor"
    corinthians2 = "2cor"
    galatians = "gal"
    ephesians = "eph"
    philippians = "phil"
    colossians = "col"
    thessalonians1 = "1thes"
    thessalonians2 = "2thes"
    timothy1 = "1tm"
    timothy2 = "2tm"
    titus = "ti"
    philemon = "phlm"
    hebrews = "heb"
    james = "jas"
    peter1 = "1pt"
    peter2 = "2pt"
    john1 = "1jn"
    john2 = "2jn"
    john3 = "3jn"
    jude = "jude"
    revelation = "rv"


BookCode = SeptuagintBookCode | NewTestamentBookCode
book_slugs = list(SeptuagintBookCode.__members__.keys()) + list(NewTestamentBookCode.__members__.keys())


@dataclasses.dataclass
class Commentary:

    author: str
    date: str
    text: str
    profile_picture_url: str
    reading_time: str

    @property
    def get_pretty_text(self):
        return f"[{self.author}, {self.date}, {self.reading_time}]\n{self.text}"


def slugify(text: str) -> str:
    text = text.strip()
    text = text.replace(" ", "_")
    text = text.lower()
    return text
