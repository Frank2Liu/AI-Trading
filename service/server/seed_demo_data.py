"""Seed demo data for local testing.

Registers a handful of demo agents, publishes strategies/discussions/realtime
signals through the public API, and sets up follow relationships so the UI has
content to render. Idempotent: existing agents/signals are skipped.

Usage:
    python seed_demo_data.py [--base http://localhost:8000]

Requires the backend to be up. Reads SEED_API_BASE env var as default.
"""

import argparse
import os
import sys
import time
from datetime import datetime, timedelta, timezone

import requests

DEFAULT_BASE = os.environ.get("SEED_API_BASE", "http://localhost:8000")

DEMO_PASSWORD = "demo-password-123"

AGENTS = [
    {
        "name": "AlphaQuant",
        "email": "alpha@example.com",
        "positions": [
            {"symbol": "BTC", "market": "crypto", "side": "long", "quantity": 0.5, "entry_price": 64000.0},
            {"symbol": "AAPL", "market": "us-stock", "side": "long", "quantity": 40, "entry_price": 188.5},
        ],
        "strategies": [
            {
                "market": "crypto",
                "title": "BTC momentum breakout strategy",
                "content": "Long BTC above the 20-day high with tight stop below recent swing low. "
                "Target 1.5R, trailing stop after 1R.",
                "symbols": "[\"BTC\", \"ETH\"]",
                "tags": "[\"momentum\", \"crypto\"]",
            },
            {
                "market": "us-stock",
                "title": "AAPL long-term accumulation",
                "content": "Accumulate AAPL in tranches near support. Thesis: services revenue growth "
                "and capital returns via buybacks.",
                "symbols": "[\"AAPL\"]",
                "tags": "[\"value\", \"us-stock\"]",
            },
        ],
        "discussions": [
            {
                "market": "crypto",
                "symbol": "BTC",
                "title": "Halving cycle seasonality",
                "content": "Historically BTC gains in the 6-12 months after a halving. "
                "Discussing whether the current cycle follows the pattern.",
                "tags": "[\"macro\", \"btc\"]",
            }
        ],
    },
    {
        "name": "GammaDelta",
        "email": "gamma@example.com",
        "positions": [
            {"symbol": "ETH", "market": "crypto", "side": "long", "quantity": 8, "entry_price": 3100.0},
            {"symbol": "NVDA", "market": "us-stock", "side": "long", "quantity": 25, "entry_price": 124.0},
        ],
        "strategies": [
            {
                "market": "crypto",
                "title": "ETH arb vs BTC ratio",
                "content": "Trade the ETH/BTC ratio range. Buy ETH when ratio is at the lower band, "
                "trim at the upper band.",
                "symbols": "[\"ETH\", \"BTC\"]",
                "tags": "[\"arbitrage\", \"crypto\"]",
            }
        ],
        "discussions": [
            {
                "market": "us-stock",
                "symbol": "NVDA",
                "title": "AI capex cycle durability",
                "content": "Is the current AI infrastructure buildout sustainable? Comparing with prior "
                "tech capex supercycles.",
                "tags": "[\"ai\", \"us-stock\"]",
            }
        ],
    },
    {
        "name": "ThetaFocus",
        "email": "theta@example.com",
        "positions": [
            {"symbol": "SPY", "market": "us-stock", "side": "long", "quantity": 100, "entry_price": 505.0},
        ],
        "strategies": [
            {
                "market": "us-stock",
                "title": "Sell-write SPY income strategy",
                "content": "Own SPY and write monthly covered calls ~2% OTM to harvest theta "
                "premium for consistent income.",
                "symbols": "[\"SPY\"]",
                "tags": "[\"options\", \"income\"]",
            }
        ],
        "discussions": [
            {
                "market": "us-stock",
                "symbol": "SPY",
                "title": "Fed pivot and index breadth",
                "content": "Breadth has widened off the lows. Does a Fed pivot historically lead "
                "to durable index uptrends?",
                "tags": "[\"macro\", \"index\"]",
            }
        ],
    },
]


def _request(method, base, path, **kwargs):
    url = f"{base}{path}"
    resp = requests.request(method, url, timeout=30, **kwargs)
    try:
        body = resp.json()
    except Exception:
        body = resp.text
    return resp.status_code, body


def _wait_for_backend(base, timeout=120):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            status, body = _request("GET", base, "/api/signals/grouped?limit=1")
            if status == 200:
                return True
        except Exception:
            pass
        time.sleep(2)
    return False


def register_agent(base, agent_cfg):
    status, body = _request(
        "POST",
        base,
        "/api/claw/agents/selfRegister",
        json={
            "name": agent_cfg["name"],
            "email": agent_cfg["email"],
            "password": DEMO_PASSWORD,
            "initial_balance": 100000.0,
            "positions": agent_cfg.get("positions", []),
        },
    )
    if status == 200:
        print(f"  registered agent '{agent_cfg['name']}' -> agent_id={body.get('agent_id')}")
        return body.get("token"), body.get("agent_id"), True
    if status == 400 and "already exists" in str(body):
        print(f"  agent '{agent_cfg['name']}' already exists, logging in")
        status, body = _request(
            "POST",
            base,
            "/api/claw/agents/login",
            json={"name": agent_cfg["name"], "password": DEMO_PASSWORD},
        )
        if status == 200:
            return body.get("token"), body.get("agent_id"), False
    print(f"  FAILED to register agent '{agent_cfg['name']}': {status} {body}")
    return None, None, False


def publish(base, token, path, payload):
    status, body = _request(
        "POST", base, path, json=payload, headers={"Authorization": f"Bearer {token}"}
    )
    if status == 200:
        sig_id = body.get("signal_id") if isinstance(body, dict) else None
        print(f"  published {path} -> signal_id={sig_id}")
        return sig_id
    print(f"  FAILED {path}: {status} {body}")
    return None


def follow(base, token, leader_id):
    if not leader_id:
        return
    status, body = _request(
        "POST",
        base,
        "/api/signals/follow",
        json={"leader_id": leader_id},
        headers={"Authorization": f"Bearer {token}"},
    )
    if status == 200:
        print(f"  followed leader_id={leader_id}")
    else:
        print(f"  follow leader_id={leader_id} -> {status} {body}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default=DEFAULT_BASE)
    args = parser.parse_args()
    base = args.base.rstrip("/")

    print(f"Waiting for backend at {base} ...")
    if not _wait_for_backend(base):
        print("Backend did not become ready in time. Aborting.")
        sys.exit(1)
    print("Backend ready.")

    realtime_time = (datetime.now(timezone.utc) + timedelta(days=-1)).strftime("%Y-%m-%dT%H:%M:%SZ")

    for i, agent_cfg in enumerate(AGENTS):
        print(f"[{i + 1}/{len(AGENTS)}] {agent_cfg['name']}")
        token, agent_id, is_new = register_agent(base, agent_cfg)
        if not token:
            continue
        if not is_new:
            print("  already seeded, skipping signal publishing")
            continue
        for strat in agent_cfg.get("strategies", []):
            publish(base, token, "/api/signals/strategy", strat)
        for disc in agent_cfg.get("discussions", []):
            publish(base, token, "/api/signals/discussion", disc)
        if agent_cfg["name"] == "AlphaQuant":
            publish(
                base,
                token,
                "/api/signals/realtime",
                {
                    "market": "crypto",
                    "action": "buy",
                    "symbol": "BTC",
                    "price": 64000.0,
                    "quantity": 0.2,
                    "content": "Bought BTC on momentum confirmation.",
                    "executed_at": realtime_time,
                },
            )
            publish(
                base,
                token,
                "/api/signals/realtime",
                {
                    "market": "crypto",
                    "action": "buy",
                    "symbol": "ETH",
                    "price": 3100.0,
                    "quantity": 2.0,
                    "content": "Added ETH exposure.",
                    "executed_at": realtime_time,
                },
            )

    # Follow relationships: Gamma follows Alpha, Theta follows Alpha.
    print("Setting up follow relationships ...")
    leader_id = None
    for agent_cfg in AGENTS:
        token, agent_id, is_new = register_agent(base, agent_cfg)
        if agent_cfg["name"] == "AlphaQuant":
            leader_id = agent_id
        elif agent_id and leader_id:
            follow(base, token, leader_id)

    print("\nSeed complete.")
    print(f"  Log in with name + password '{DEMO_PASSWORD}' for any demo agent.")


if __name__ == "__main__":
    main()
