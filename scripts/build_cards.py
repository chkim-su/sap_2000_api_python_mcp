from __future__ import annotations

from pathlib import Path

from mcp.cards import build_cards_from_html, write_cards_jsonl


if __name__ == "__main__":
    html_root = Path("build/html")
    output_path = Path("build/cards/functions_base.jsonl")
    cards = build_cards_from_html(html_root)
    write_cards_jsonl(cards, output_path)
    print(f"Wrote {len(cards)} cards to {output_path}")