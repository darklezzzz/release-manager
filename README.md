# Задание 6. Автоматизация программных релизов

core: SemVer, bump, register и check_tag; отдельные workflow обычного CI и релизной сборки.

## Установка и запуск

Нужны Python 3.11+ и uv. Проект является самостоятельным Git-репозиторием;
его можно скопировать отдельно от учебного workspace. Внутри этого workspace
для команд пакетов используйте `uv run --all-packages <команда>`, либо сначала
из корня выполните `uv sync --all-packages`, затем запускайте команды из `.venv/bin/`.
После отдельного клонирования:

```sh
uv sync --locked
uv run release-manager --help
uv run pytest -v
uv run ruff check .
```

Все команды ниже выполняются из корня отдельного проекта с новой базой `.data/application.db`.
Команды с идентификатором 1 предполагают пустую базу. Повторная регистрация ID — ошибка.
Вывод — UTF-8 / JSON; неверные аргументы завершаются с кодом 2.

```sh
uv run release-manager show
uv run release-manager bump 1.2.3 minor
uv run release-manager check-tag --tag v1.0.0
uv build
uv tool install dist/release_manager-1.0.0-py3-none-any.whl
```

## Архитектура и алгоритм

Обычный push/PR → pytest без обязательного тега; push v* → строгое сравнение тега и project.version → тесты → wheel + sdist → Artifacts.

Код в `src/`, автоматизированные проверки в `tests/`, воспроизводимая демонстрация —
`examples/demo.py`, результаты — `examples/`. Запуск: `uv run python examples/demo.py`.
Она использует временное хранилище и обновляет только демонстрационные результаты.

## Связь с управлением конфигурацией

Идентификация, история и проверяемые состояния описаны в [SCMP.md](SCMP.md).
История версий: [CHANGELOG.md](CHANGELOG.md). Учебный отчёт: [REPORT.md](REPORT.md).
Git-доказательства: `git log --graph --oneline --all`, `git branch`, `git tag`.

## Ограничения

Поддерживается запрошенное подмножество SemVer MAJOR.MINOR.PATCH без prerelease/build. Регистрация двух файлов рассчитана на одного оператора; публикации в PyPI нет.

## GitHub

[darklezzzz/release-manager](https://github.com/darklezzzz/release-manager).

Подтверждения успешных и предусмотренных неуспешных сценариев: [CI_EVIDENCE.md](CI_EVIDENCE.md).
