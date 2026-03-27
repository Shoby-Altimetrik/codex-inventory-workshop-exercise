#!/usr/bin/env python3
from __future__ import annotations

import html
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
README_PATH = ROOT_DIR / "README.md"
HTML_PATH = ROOT_DIR / "workshop-exercises.html"
EXPECTED_EXERCISE_COUNT = 8


@dataclass
class Exercise:
    number: int
    title: str
    time_range: str
    has_acceptance_criteria: bool


def normalize(text: str) -> str:
    text = html.unescape(text)
    return " ".join(text.split())


def parse_readme_exercises(raw: str) -> list[Exercise]:
    header_re = re.compile(
        r"^## Exercise (\d+): (.+?) \((\d+-\d+ minutes)\)\s*$", re.MULTILINE
    )
    matches = list(header_re.finditer(raw))
    exercises: list[Exercise] = []

    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(raw)
        section = raw[start:end]
        exercises.append(
            Exercise(
                number=int(match.group(1)),
                title=normalize(match.group(2)),
                time_range=normalize(match.group(3)),
                has_acceptance_criteria="### Acceptance criteria" in section,
            )
        )

    return exercises


def parse_html_exercises(raw: str) -> list[Exercise]:
    article_re = re.compile(
        r'<article class="exercise" id="ex(\d+)">(.*?)</article>', re.DOTALL
    )
    h3_re = re.compile(r"<h3>\s*Exercise \d+:\s*(.*?)\s*</h3>", re.DOTALL)
    time_re = re.compile(r'<span class="chip time">\s*([^<]+)\s*</span>')

    exercises: list[Exercise] = []
    for article_match in article_re.finditer(raw):
        number = int(article_match.group(1))
        section = article_match.group(2)

        title_match = h3_re.search(section)
        time_match = time_re.search(section)

        if title_match is None or time_match is None:
            continue

        title = re.sub(r"<[^>]+>", "", title_match.group(1))
        exercises.append(
            Exercise(
                number=number,
                title=normalize(title),
                time_range=normalize(time_match.group(1)),
                has_acceptance_criteria="Acceptance criteria" in section,
            )
        )

    return exercises


def validate_sequence(label: str, exercises: list[Exercise], errors: list[str]) -> None:
    if len(exercises) != EXPECTED_EXERCISE_COUNT:
        errors.append(
            f"{label}: expected {EXPECTED_EXERCISE_COUNT} exercises, found {len(exercises)}"
        )
        return

    expected_numbers = list(range(1, EXPECTED_EXERCISE_COUNT + 1))
    numbers = [exercise.number for exercise in exercises]
    if numbers != expected_numbers:
        errors.append(f"{label}: exercise order mismatch {numbers} != {expected_numbers}")


def main() -> int:
    readme_raw = README_PATH.read_text(encoding="utf-8")
    html_raw = HTML_PATH.read_text(encoding="utf-8")

    readme_exercises = parse_readme_exercises(readme_raw)
    html_exercises = parse_html_exercises(html_raw)

    errors: list[str] = []
    validate_sequence("README", readme_exercises, errors)
    validate_sequence("HTML", html_exercises, errors)

    indexed_readme = {exercise.number: exercise for exercise in readme_exercises}
    indexed_html = {exercise.number: exercise for exercise in html_exercises}
    numbers = set(indexed_readme.keys()) | set(indexed_html.keys())

    for number in sorted(numbers):
        r = indexed_readme.get(number)
        h = indexed_html.get(number)
        if r is None or h is None:
            errors.append(f"Exercise {number}: missing in {'README' if r is None else 'HTML'}")
            continue

        if r.title != h.title:
            errors.append(
                f"Exercise {number}: title mismatch README='{r.title}' HTML='{h.title}'"
            )
        if r.time_range != h.time_range:
            errors.append(
                f"Exercise {number}: time mismatch README='{r.time_range}' HTML='{h.time_range}'"
            )
        if not r.has_acceptance_criteria:
            errors.append(f"Exercise {number}: README missing acceptance criteria section")
        if not h.has_acceptance_criteria:
            errors.append(f"Exercise {number}: HTML missing acceptance criteria section")
        if r.time_range != "10-20 minutes":
            errors.append(
                f"Exercise {number}: unexpected time range '{r.time_range}', expected '10-20 minutes'"
            )

    if errors:
        print("Guide sync validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Guide sync validation passed: README and HTML are aligned.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
