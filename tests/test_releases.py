import pytest
from release_manager.core import bump, check_tag, package_version, parse_version, register


@pytest.fixture
def project(tmp_path):
    path = tmp_path / "pyproject.toml"
    path.write_text(
        '[project]\nname="sample"\nversion="1.0.0"\n\n[tool.example]\nversion="9.0.0"\n'
    )
    return path


@pytest.mark.parametrize(
    ("part", "expected"), [("major", "2.0.0"), ("minor", "1.3.0"), ("patch", "1.2.4")]
)
def test_bump(part, expected):
    assert bump("1.2.3", part) == expected


@pytest.mark.parametrize("version", ["01.0.0", "1.0", "-1.0.0", "1.0.0rc1", "v1.0.0"])
def test_invalid_version(version):
    with pytest.raises(ValueError):
        parse_version(version)


def test_tag_success(project):
    assert check_tag(project, "v1.0.0") == "v1.0.0"


@pytest.mark.parametrize("tag", [None, "", "v2.0.0", "vbad", "1.0.0"])
def test_tag_failure(project, tag):
    with pytest.raises(ValueError):
        check_tag(project, tag)


def test_register(project, tmp_path):
    log = tmp_path / "CHANGELOG.md"
    register(project, log, "1.1.0", ["Добавлен отчёт"])
    assert package_version(project) == "1.1.0"
    assert 'version="9.0.0"' in project.read_text()
    assert "[1.1.0]" in log.read_text()
    with pytest.raises(ValueError):
        register(project, log, "1.1.0", ["Дубликат"])


def test_decrease(project, tmp_path):
    with pytest.raises(ValueError):
        register(project, tmp_path / "log", "0.9.0", ["Ошибка"])
    assert package_version(project) == "1.0.0"


def test_registered_future_version(project, tmp_path):
    log = tmp_path / "log"
    log.write_text("## [2.0.0] — 2026-01-01\n")
    with pytest.raises(ValueError):
        register(project, log, "2.0.0", ["Дубль"])


def test_normal_tests_without_tag(project, monkeypatch):
    monkeypatch.delenv("GITHUB_REF", raising=False)
    assert package_version(project) == "1.0.0"
    assert bump("1.0.0", "patch") == "1.0.1"
