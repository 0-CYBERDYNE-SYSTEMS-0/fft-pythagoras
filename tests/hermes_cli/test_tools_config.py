"""Tests for hermes_cli.tools_config onboarding and platform persistence."""

import hermes_cli.tools_config as tools_config


def test_get_enabled_platforms_treats_false_whatsapp_as_disabled(monkeypatch):
    values = {
        "TELEGRAM_BOT_TOKEN": "",
        "DISCORD_BOT_TOKEN": "",
        "SLACK_BOT_TOKEN": "",
        "WHATSAPP_ENABLED": "false",
    }

    monkeypatch.setattr(tools_config, "get_env_value", lambda key: values.get(key, ""))

    enabled = tools_config._get_enabled_platforms()

    assert enabled == ["cli"]


def test_get_platform_tools_uses_default_when_platform_not_configured():
    config = {}

    enabled = tools_config._get_platform_tools(config, "cli")

    assert enabled


def test_get_platform_tools_preserves_explicit_empty_selection():
    config = {"platform_toolsets": {"cli": []}}

    enabled = tools_config._get_platform_tools(config, "cli")

    assert enabled == set()


def test_tools_command_first_install_runs_single_global_pass(monkeypatch):
    config = {}
    checklist_calls = []
    configured = []
    saved = []

    monkeypatch.setattr(tools_config, "_get_enabled_platforms", lambda: ["cli", "telegram", "whatsapp"])
    monkeypatch.setattr(tools_config, "_get_platform_tools", lambda config, platform: {"terminal", "web"})
    monkeypatch.setattr(
        tools_config,
        "_prompt_toolset_checklist",
        lambda label, enabled: checklist_calls.append((label, set(enabled))) or {"browser", "terminal", "web"},
    )
    monkeypatch.setattr(tools_config, "_configure_toolset", lambda ts_key, config: configured.append(ts_key))
    monkeypatch.setattr(
        tools_config,
        "_save_platform_tools",
        lambda config, platform, enabled: saved.append((platform, set(enabled))),
    )
    monkeypatch.setattr(tools_config, "save_config", lambda config: None)

    tools_config.tools_command(first_install=True, config=config)

    assert checklist_calls == [("all enabled platforms", {"terminal", "web"})]
    assert configured == ["browser", "web"]
    assert saved == [
        ("cli", {"browser", "terminal", "web"}),
        ("telegram", {"browser", "terminal", "web"}),
        ("whatsapp", {"browser", "terminal", "web"}),
    ]
