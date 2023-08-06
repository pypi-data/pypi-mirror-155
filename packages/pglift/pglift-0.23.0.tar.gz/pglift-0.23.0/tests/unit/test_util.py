import stat
import string
from pathlib import Path

import pytest

from pglift import util


def test_xdg_config_home(monkeypatch: pytest.MonkeyPatch) -> None:
    with monkeypatch.context() as m:
        m.setattr("pathlib.Path.home", lambda: Path("/ho/me"))
        assert util.xdg_config_home() == Path("/ho/me/.config")


def test_xdg_data_home(monkeypatch: pytest.MonkeyPatch) -> None:
    with monkeypatch.context() as m:
        m.setenv("XDG_DATA_HOME", "/x/y")
        assert util.xdg_data_home() == Path("/x/y")
    with monkeypatch.context() as m:
        try:
            m.delenv("XDG_DATA_HOME")
        except KeyError:
            pass
        m.setattr("pathlib.Path.home", lambda: Path("/ho/me"))
        assert util.xdg_data_home() == Path("/ho/me/.local/share")


def test_xdg_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    configdir = tmp_path / "pglift"
    configdir.mkdir()
    configfile = configdir / "x"
    configfile.touch()
    with monkeypatch.context() as m:
        m.setenv("XDG_CONFIG_HOME", str(tmp_path))
        assert util.xdg_config("x") == configfile
    assert util.xdg_config("x") is None


def test_dist_config() -> None:
    pg_hba = util.dist_config("postgresql", "pg_hba.conf")
    assert pg_hba is not None
    assert pg_hba.parent == util.datapath / "postgresql"


def test_gen_certificate(tmp_path: Path) -> None:

    util.generate_certificate(tmp_path)
    crt = tmp_path / "server.crt"
    key = tmp_path / "server.key"
    assert crt.exists()
    assert key.exists()
    assert stat.filemode(crt.stat().st_mode) == "-rw-------"
    assert stat.filemode(key.stat().st_mode) == "-rw-------"


def test_total_memory(meminfo: Path) -> None:
    assert util.total_memory(meminfo) == 6166585344.0


def test_total_memory_error(tmp_path: Path) -> None:
    meminfo = tmp_path / "meminfo"
    meminfo.touch()
    with pytest.raises(Exception, match="could not retrieve memory information from"):
        util.total_memory(meminfo)


def test_generate_password() -> None:
    pwd = util.generate_password(2)
    assert set(pwd) & set(string.ascii_letters) and set(pwd) & set(string.digits)
