from pydantic import BaseModel
from .constants.language import LocalisedMessage, Language

class LanguageDataModel(BaseModel):
    """A model for the langauge data stored inside language packs."""

    locale_id: Language
    text: dict[str, str]

def parse_into_model(lang_data: list[dict[str, str]]) -> list[LanguageDataModel]:
    """Parses all of the language data into a list of pydantic models."""

    return [LanguageDataModel(**data) for data in lang_data]
