# Проверка и демонстрация CI

## Локальная проверка отдельного клона

```sh
uv sync --locked
uv run pytest -v
uv run ruff check .
uv run python examples/demo.py
```

Python CI запускается при push и pull_request на Python 3.11 и 3.12.
Локальные протоколы examples/verification.txt и результаты GitHub Actions — разные
свидетельства. Ссылки на удалённые запуски собраны в CI_EVIDENCE.md.

## Обычный CI и релиз

Обычные push/PR не требуют релизного Git-тега и не вызывают проверку check-tag.
Отдельный release.yml работает только при push тега v*. Сначала он сравнивает тег
с project.version, затем запускает тесты и сборку, затем сохраняет wheel/sdist.

- v1.0.0 соответствует версии пакета 1.0.0: два артефакта.
- v1.0.1 не соответствует: ошибка проверки, релизные артефакты отсутствуют.
- vbad не соответствует формату: ошибка до сборки.

Локальная команда: `uv run python scripts/release_build.py --tag v1.0.0`.
После регистрации новой версии обновите uv.lock через `uv lock`.
