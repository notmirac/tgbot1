from __future__ import annotations

import random

FEMALE_NAMES = [
    "Алина", "София", "Вика", "Кира", "Полина", "Лера", "Милана", "Ева", "Лиза", "Катя",
    "Ника", "Марина", "Аня", "Юля", "Дарья", "Настя", "Алина", "Вероника", "Диана", "Оля",
]

MALE_NAMES = [
    "Артём", "Максим", "Данил", "Кирилл", "Егор", "Илья", "Никита", "Роман", "Алексей", "Дима",
    "Матвей", "Саша", "Влад", "Миша", "Павел", "Тимур", "Денис", "Сергей", "Игорь", "Антон",
]

OPENERS_RU = {
    "ж": [
        "Привет 🙂", "Хей) Как ты?", "Приветик, чем занят?", "Ну привет 😌", "Привет, приятно познакомиться",
    ],
    "м": [
        "Привет 👋", "Хай, как дела?", "Привет, чем занимаешься?", "Ну привет", "Здарова 🙂",
    ],
}


def build_virtual_profile(preferred_gender: str, age_min: int, age_max: int) -> dict:
    gender = preferred_gender if preferred_gender in {"м", "ж"} else "ж"
    names = FEMALE_NAMES if gender == "ж" else MALE_NAMES
    safe_min = max(18, min(age_min, age_max))
    safe_max = min(50, max(age_min, age_max))
    age = random.randint(safe_min, safe_max)
    name = random.choice(names)
    return {
        "name": name,
        "age": age,
        "gender": gender,
        "opener": random.choice(OPENERS_RU[gender]),
    }
