from __future__ import annotations

import os
import random
from pathlib import Path

BASE_DIR = Path('photos_18')
MALE_DIR = BASE_DIR / 'male'
FEMALE_DIR = BASE_DIR / 'female'

MALE_NAMES = [
    'Алексей', 'Максим', 'Дмитрий', 'Иван', 'Андрей',
    'Егор', 'Никита', 'Артём', 'Кирилл', 'Сергей',
    'Роман', 'Влад', 'Павел', 'Антон', 'Михаил',
]

FEMALE_NAMES = [
    'Алина', 'София', 'Мария', 'Анна', 'Екатерина',
    'Виктория', 'Полина', 'Дарья', 'Ксения', 'Анастасия',
    'Ева', 'Лера', 'Юлия', 'Карина', 'Диана',
]

PHOTO_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}


def ensure_photo_dirs() -> None:
    MALE_DIR.mkdir(parents=True, exist_ok=True)
    FEMALE_DIR.mkdir(parents=True, exist_ok=True)


def get_gender_folder(gender: str) -> Path:
    if gender == 'male':
        return MALE_DIR
    if gender == 'female':
        return FEMALE_DIR
    raise ValueError(f'Unknown gender: {gender}')


def get_gender_label(gender: str) -> str:
    return 'Мужской' if gender == 'male' else 'Женский'


def get_names_by_gender(gender: str) -> list[str]:
    return MALE_NAMES if gender == 'male' else FEMALE_NAMES


def get_all_photos(gender: str) -> list[str]:
    ensure_photo_dirs()
    folder = get_gender_folder(gender)
    files: list[str] = []
    for file_name in os.listdir(folder):
        path = folder / file_name
        if path.is_file() and path.suffix.lower() in PHOTO_EXTENSIONS:
            files.append(str(path))
    files.sort()
    return files


def make_profile_for_photo(gender: str, photo_path: str) -> dict:
    rnd = random.Random(f'{gender}:{photo_path}')
    name = rnd.choice(get_names_by_gender(gender))
    age = rnd.randint(18, 50)
    return {
        'name': name,
        'age': age,
        'gender': 'м' if gender == 'male' else 'ж',
        'gender_key': gender,
        'gender_label': get_gender_label(gender),
        'photo_path': photo_path,
    }
