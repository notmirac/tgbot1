# services/virtual_profiles.py
import random

MALE_NAMES_RU   = ["Алексей", "Максим", "Дмитрий", "Иван", "Андрей", "Кирилл", "Роман", "Артём"]
FEMALE_NAMES_RU = ["Алина", "София", "Мария", "Анна", "Екатерина", "Диана", "Валерия", "Ника"]
MALE_NAMES_EN   = ["Ethan", "Daniel", "Michael", "Ryan", "Leo", "Jake", "Chris", "Tyler"]
FEMALE_NAMES_EN = ["Emma", "Olivia", "Mia", "Lily", "Chloe", "Sofia", "Ava", "Grace"]

CITIES_RU = ["Москве", "Питере", "Казани", "Екатеринбурге", "Новосибирске", "Краснодаре"]
CITIES_EN = ["Moscow", "London", "Berlin", "New York", "Amsterdam", "Paris"]

INTERESTS_RU = [
    "люблю путешествовать", "занимаюсь спортом", "обожаю кино",
    "читаю книги", "хожу в спортзал", "люблю готовить",
    "занимаюсь танцами", "слушаю музыку",
]
INTERESTS_EN = [
    "love travelling", "into fitness", "enjoy movies",
    "read a lot", "go to the gym", "love cooking",
    "into dancing", "listen to music",
]


def build_virtual_profile(
    preferred_gender: str | None = None,
    age_min: int = 18,
    age_max: int = 50,
    lang: str = "ru",
) -> dict:
    gender   = preferred_gender if preferred_gender in {"м", "ж"} else random.choice(["м", "ж"])
    age_min  = max(18, int(age_min or 18))
    age_max  = min(50, int(age_max or 50))
    if age_min > age_max:
        age_min, age_max = age_max, age_min

    if lang == "en":
        names = MALE_NAMES_EN if gender == "м" else FEMALE_NAMES_EN
        city  = random.choice(CITIES_EN)
        interest = random.choice(INTERESTS_EN)
    else:
        names = MALE_NAMES_RU if gender == "м" else FEMALE_NAMES_RU
        city  = random.choice(CITIES_RU)
        interest = random.choice(INTERESTS_RU)

    return {
        "name":     random.choice(names),
        "age":      random.randint(age_min, age_max),
        "gender":   gender,
        "city":     city,
        "interest": interest,
        "lang":     lang,
    }
