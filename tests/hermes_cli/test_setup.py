"""Tests for FarmFriend setup output."""

from pathlib import Path

import hermes_cli.setup as setup


def test_print_setup_summary_uses_farmfriend_commands(monkeypatch, capsys):
    monkeypatch.setattr(setup, "get_env_value", lambda key: "")
    monkeypatch.setattr(setup, "get_config_path", lambda: "/tmp/config.yaml")
    monkeypatch.setattr(setup, "get_env_path", lambda: "/tmp/.env")

    setup._print_setup_summary({}, Path("/tmp/hermes-home"))

    output = capsys.readouterr().out

    assert "farmfriend setup" in output
    assert "farmfriend config edit" in output
    assert "farmfriend gateway" in output
    assert "hermes setup" not in output
    assert "Hermes" not in output
