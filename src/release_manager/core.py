"""Strict MAJOR.MINOR.PATCH versions and release-only Git tag validation."""
import re
import tomllib
from datetime import date
from pathlib import Path

PATTERN = r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)'


def parse_version(version):
    if not isinstance(version, str) or not re.fullmatch(PATTERN, version):
        raise ValueError('Версия должна иметь формат MAJOR.MINOR.PATCH без ведущих нулей')
    return tuple(map(int, version.split('.')))


def bump(version, part):
    values = list(parse_version(version))
    if part not in ('major', 'minor', 'patch'):
        raise ValueError('Укажите major, minor или patch')
    index = ('major', 'minor', 'patch').index(part)
    values[index] += 1
    values[index + 1:] = [0] * (2 - index)
    return '.'.join(map(str, values))


def package_version(project):
    try:
        value = tomllib.loads(Path(project).read_text(encoding='utf-8'))['project']['version']
        parse_version(value)
        return value
    except (OSError, KeyError, tomllib.TOMLDecodeError) as exc:
        raise ValueError('Не удалось прочитать версию из pyproject.toml') from exc


def check_tag(project, tag):
    if not tag:
        raise ValueError('Отсутствует релизный Git-тег')
    if not tag.startswith('v'):
        raise ValueError('Тег должен иметь формат vX.Y.Z')
    parse_version(tag[1:])
    if tag[1:] != package_version(project):
        raise ValueError('Версия Git-тега не соответствует версии пакета')
    return tag


def register(project, changelog, version, changes):
    target = Path(project)
    current = package_version(target)
    if parse_version(version) <= parse_version(current):
        raise ValueError('Новая версия должна быть больше текущей')
    log = Path(changelog)
    history = log.read_text(encoding='utf-8') if log.exists() else '# CHANGELOG\n'
    if re.search(r'^## \[' + re.escape(version) + r'\]', history, re.MULTILINE):
        raise ValueError('Версия уже зарегистрирована')
    if not changes or any(not isinstance(c, str) or not c.strip() for c in changes):
        raise ValueError('Перечень изменений обязателен')
    # Match the project table only, leaving dependency and tool versions intact.
    text = target.read_text(encoding='utf-8')
    match = re.search(r'(?ms)^\[project\]\s*\n(.*?)(?=^\[|\Z)', text)
    if not match:
        raise ValueError('Таблица project отсутствует')
    section, count = re.subn(r'(?m)^(version\s*=\s*)["\'][^"\']+["\']',
                            lambda m: m[1] + '"' + version + '"', match[1], count=1)
    if count != 1:
        raise ValueError('Не найдено поле project.version')
    updated = text[:match.start(1)] + section + text[match.end(1):]
    entry = f'## [{version}] — {date.today().isoformat()}\n' + ''.join(f'- {c}\n' for c in changes)
    log.write_text(history.rstrip() + '\n\n' + entry, encoding='utf-8')
    target.write_text(updated, encoding='utf-8')
    return version
