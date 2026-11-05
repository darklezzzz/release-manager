# Подтверждения GitHub Actions

Все ссылки ведут на реальные завершённые запуски.

- [Push main: успешный CI](https://github.com/darklezzzz/release-manager/actions/runs/42021370327): `success`, commit `e73bc7a6074d0d0def813b640611ae104a00f32a`.
- [Pull request: успешный CI](https://github.com/darklezzzz/release-manager/actions/runs/42021440317): `success`, commit `1e3c2ba6ff701d35fc36e75e2e633166b6ed8aaf`.
- [Релиз v1.0.0: wheel и sdist](https://github.com/darklezzzz/release-manager/actions/runs/42021370495): `success`, commit `b3b544ea6d59b79a08581aabcdc261c3b2e9d521`.
- [Релиз v1.0.1: отказ до сборки](https://github.com/darklezzzz/release-manager/actions/runs/42021492986): `failure`, commit `b3b544ea6d59b79a08581aabcdc261c3b2e9d521`.

[Pull request с проверкой](https://github.com/darklezzzz/release-manager/pull/1).

Успешный Release build сохраняет python-distributions в Actions Artifacts.
У v1.0.1 упал шаг Check release tag before building artifacts; артефактов нет.
Обычный Python CI не требует тега и остаётся независимым от релизной проверки.
Это автоматизированная сборка; публикация в PyPI и deployment не выполняются.

Полная метаинформация: github-evidence.json в общем комплекте сдачи.
