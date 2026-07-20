import re
from backend.skills import SKILLS

from pathlib import Path

from backend.config import (
    RESUME_FOLDER,
    JD_FOLDER,
    VECTOR_DB_PATH,
    REPORT_FOLDER
)

def create_folder(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def create_project_directories():
    folders = [
        RESUME_FOLDER,
        JD_FOLDER,
        VECTOR_DB_PATH,
        REPORT_FOLDER,
    ]

    for folder in folders:
        create_folder(folder)

import re

EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
PHONE_PATTERN = r"(?:\+?\d{1,3}[- ]?)?\d{10}"


def extract_email(text):
    emails = re.findall(EMAIL_PATTERN, text)
    return emails[0] if emails else ""


def extract_phone(text):
    phones = re.findall(PHONE_PATTERN, text)
    return phones[0] if phones else ""


def extract_name(text):
    lines = text.splitlines()

    for line in lines[:10]:
        line = line.strip()

        if len(line.split()) <= 4:
            return line

    return ""

def extract_skills(text: str) -> list:

    text = text.lower()

    found = []

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found.append(skill)

    return sorted(list(set(found)))


def extract_experience(text: str) -> int:

    pattern = r"(\d+)\+?\s*(?:years|year)"

    matches = re.findall(pattern, text.lower())

    if matches:
        return max(int(year) for year in matches)

    return 0


def extract_education(text: str) -> list:

    education_keywords = [

        "b.tech",
        "bachelor",
        "master",
        "m.tech",
        "msc",
        "bsc",
        "phd",
        "degree"

    ]

    text = text.lower()

    found = []

    for item in education_keywords:

        if item in text:
            found.append(item)

    return sorted(list(set(found)))