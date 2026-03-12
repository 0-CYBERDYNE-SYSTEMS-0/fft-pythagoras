"""Shared FarmFriend branding helpers for user-facing runtime text."""

from __future__ import annotations

import builtins
import re

BRAND_NAME = "FarmFriend"
BRAND_CLI_COMMAND = "farmfriend"
BRAND_GATEWAY = f"{BRAND_NAME} Gateway"
BRAND_INSIGHTS = f"{BRAND_NAME} Insights"
BRAND_RESPONSE_LABEL = f"⚕ {BRAND_NAME}"
BRAND_OPENROUTER_TITLE = BRAND_NAME
BRAND_HTTP_USER_AGENT = "FarmFriend/1.0"

_TEXT_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"Nous Hermes", re.IGNORECASE), BRAND_NAME),
    (re.compile(r"Hermes Agent"), BRAND_NAME),
    (re.compile(r"Hermes Gateway"), BRAND_GATEWAY),
    (re.compile(r"Hermes Insights"), BRAND_INSIGHTS),
    (re.compile(r"Hermes Setup"), f"{BRAND_NAME} Setup"),
    (re.compile(r"Hermes Tool Configuration"), f"{BRAND_NAME} Tool Configuration"),
    (re.compile(r"Hermes Configuration"), f"{BRAND_NAME} Configuration"),
    (re.compile(r"Nous Research"), BRAND_NAME),
    (re.compile(r"\bHermace\b", re.IGNORECASE), BRAND_NAME),
    (re.compile(r"⚕\s*Hermes"), BRAND_RESPONSE_LABEL),
    (re.compile(r"\bHermes\b"), BRAND_NAME),
)

_COMMAND_PATTERN = re.compile(r"(?<![./_~-])\bhermes\b(?![-_/.\w])")
_PRINT_PATCH_FLAG = "__farmfriend_branding_installed__"


def brand_command(*parts: str) -> str:
    suffix = " ".join(part for part in parts if part).strip()
    return f"{BRAND_CLI_COMMAND} {suffix}".strip()


def scrub_public_text(text: str, *, replace_commands: bool = True) -> str:
    if not text:
        return text

    branded = text
    for pattern, replacement in _TEXT_PATTERNS:
        branded = pattern.sub(replacement, branded)

    if replace_commands:
        branded = _COMMAND_PATTERN.sub(BRAND_CLI_COMMAND, branded)

    return branded


def install_print_branding() -> None:
    if getattr(builtins.print, _PRINT_PATCH_FLAG, False):
        return

    original_print = builtins.print

    def branded_print(*args, **kwargs):
        branded_args = tuple(
            scrub_public_text(arg) if isinstance(arg, str) else arg
            for arg in args
        )
        return original_print(*branded_args, **kwargs)

    setattr(branded_print, _PRINT_PATCH_FLAG, True)
    builtins.print = branded_print


BRAND_BANNER_LOGO = """[bold #7A9B44]███████╗ █████╗ ██████╗ ███╗   ███╗███████╗██████╗ ██╗███████╗███╗   ██╗██████╗ [/]
[bold #8FB255]██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝██╔══██╗██║██╔════╝████╗  ██║██╔══██╗[/]
[#A7C76B]█████╗  ███████║██████╔╝██╔████╔██║█████╗  ██████╔╝██║█████╗  ██╔██╗ ██║██║  ██║[/]
[#B6D37A]██╔══╝  ██╔══██║██╔══██╗██║╚██╔╝██║██╔══╝  ██╔══██╗██║██╔══╝  ██║╚██╗██║██║  ██║[/]
[#C5DE8A]██║     ██║  ██║██║  ██║██║ ╚═╝ ██║██║     ██║  ██║██║███████╗██║ ╚████║██████╔╝[/]
[#D6E8A0]╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═══╝╚═════╝ [/]
[dim #7A9B44]                            practical AI for the farm                              [/]
"""

BRAND_COMPACT_BANNER = f"""
[bold #7A9B44]╔══════════════════════════════════════════════════════════════╗[/]
[bold #7A9B44]║[/]  [#A7C76B]{BRAND_NAME}[/] [dim #6C7E3E]- practical AI assistant[/]           [bold #7A9B44]║[/]
[bold #7A9B44]║[/]  [#C5DE8A]ready for terminal, tools, and messaging[/]           [bold #7A9B44]║[/]
[bold #7A9B44]╚══════════════════════════════════════════════════════════════╝[/]
"""
