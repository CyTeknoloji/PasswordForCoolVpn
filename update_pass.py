#!/usr/bin/env python3
"""Scrape current VPNBook OpenVPN password and write password.json.

Preferred: parse the visible credentials block on /freevpn.
Fallback: regex near the word vpnbook with a strict blacklist.
"""

from __future__ import annotations

import json
import re
import sys

from playwright.sync_api import sync_playwright

PASSWORD_FILE = "password.json"
URLS = (
    "https://www.vpnbook.com/freevpn",
    "https://www.vpnbook.com/freevpn/openvpn",
)
BLACKLIST = {
    "vpnbook",
    "password",
    "username",
    "locations",
    "ocations",
    "static",
    "chunks",
    "viewport",
    "visible",
    "openvpn",
    "wireguard",
    "outline",
    "servers",
    "protocol",
    "copy",
    "freevpn",
    "https",
    "http",
}


def looks_like_password(token: str) -> bool:
    token = token.strip().lower()
    if len(token) < 6 or len(token) > 12:
        return False
    if token in BLACKLIST:
        return False
    if not re.fullmatch(r"[a-z0-9]+", token):
        return False
    # Must mix letters and digits (VPNBook style), reject pure words/numbers.
    has_letter = any(c.isalpha() for c in token)
    has_digit = any(c.isdigit() for c in token)
    return has_letter and has_digit


def extract_from_text(body_text: str) -> str | None:
    # Explicit "Password" label followed by token (table / copy block).
    labeled = re.findall(
        r"Password\s*[:\n\r\t ]+`?([a-z0-9]{6,12})`?",
        body_text,
        flags=re.IGNORECASE,
    )
    for candidate in labeled:
        if looks_like_password(candidate):
            return candidate.strip().lower()

    # Username vpnbook then nearby password-like token.
    if "vpnbook" in body_text.lower():
        after = body_text.lower().split("vpnbook")[-1]
        for match in re.finditer(r"\b([a-z0-9]{6,12})\b", after):
            token = match.group(1)
            if looks_like_password(token):
                return token
    return None


def fetch_password() -> str | None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 900},
        )
        page = context.new_page()
        try:
            for url in URLS:
                print(f"Fetching {url}")
                page.goto(url, wait_until="domcontentloaded", timeout=60_000)
                page.wait_for_timeout(2_000)
                body = page.inner_text("body")
                password = extract_from_text(body)
                if password:
                    print(f"Found password: {password}")
                    return password
            print("Password not found on any URL", file=sys.stderr)
            return None
        finally:
            browser.close()


def write_password(password: str) -> None:
    with open(PASSWORD_FILE, "w", encoding="utf-8") as handle:
        json.dump({"pass": password, "user": "vpnbook"}, handle, indent=4)
        handle.write("\n")
    print(f"Wrote {PASSWORD_FILE}")


if __name__ == "__main__":
    found = fetch_password()
    if not found:
        raise SystemExit(1)
    write_password(found)
