import random

MALE_NAMES = ["Алексей", "Максим", "Дмитрий", "Иван", "Андрей", "Ethan", "Daniel", "Michael", "Ryan", "Leo"]
FEMALE_NAMES = ["Алина", "София", "Мария", "Анна", "Екатерина", "Emma", "Olivia", "Mia", "Lily", "Chloe"]

def build_virtual_profile(preferred_gender: str | None = None, age_min: int = 18, age_max: int = 50) -> dict:
    gender = preferred_gender if preferred_gender in {"м", "ж"} else random.choice(["м", "ж"])
    names = MALE_NAMES if gender == "м" else FEMALE_NAMES
    age_min = max(18, int(age_min or 18))
    age_max = min(50, int(age_max or 50))
    if age_min > age_max:
        age_min, age_max = age_max, age_min
    return {
        "name": random.choice(names),
        "age": random.randint(age_min, age_max),
        "gender": gender,
    }
