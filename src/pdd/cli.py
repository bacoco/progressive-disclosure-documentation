from __future__ import annotations

import argparse
import json
from pathlib import Path

from pdd.artifacts.receipts import write_receipt
from pdd.generation.renderer import generate_docs
from pdd.index.sqlite_fts import build_index
from pdd.inventory.models import Inventory
from pdd.inventory.scanner import scan_repo
from pdd.review import coverage_receipt, grounding_receipt, regression_receipt


def _write_json(path: str | Path, payload: dict[str, object]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _read_inventory(path: str | Path) -> Inventory:
    return Inventory.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))


def cmd_inventory(args: argparse.Namespace) -> int:
    inventory = scan_repo(args.repo)
    _write_json(args.out, inventory.to_dict())
    print(f"wrote {args.out}")
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    stats = generate_docs(_read_inventory(args.inventory), args.out)
    print(json.dumps(stats, indent=2))
    return 0


def cmd_convert(args: argparse.Namespace) -> int:
    inventory = scan_repo(args.repo)
    _write_json(Path(args.out).parent / ".pdd" / "inventory.json", inventory.to_dict())
    stats = generate_docs(inventory, args.out)
    print(json.dumps({"converted_from": args.docs, **stats}, indent=2))
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    inventory = scan_repo(args.repo)
    stats = generate_docs(inventory, args.out)
    print(json.dumps({"updated_from": args.docs, **stats}, indent=2))
    return 0


def cmd_review(args: argparse.Namespace) -> int:
    inventory = _read_inventory(args.inventory)
    out = Path(args.out)
    source_map = Path(args.docs).parent / ".pdd" / "source-map.json"
    write_receipt(out, "coverage", coverage_receipt(args.docs, inventory))
    write_receipt(out, "grounding", grounding_receipt(args.docs, source_map))
    write_receipt(out, "regression", regression_receipt(args.docs))
    print(f"wrote review receipts to {out}")
    return 0


def cmd_index(args: argparse.Namespace) -> int:
    print(json.dumps(build_index(args.docs, args.out), indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pdd")
    sub = parser.add_subparsers(dest="command", required=True)
    inv = sub.add_parser("inventory")
    inv.add_argument("--repo", required=True)
    inv.add_argument("--out", required=True)
    inv.set_defaults(func=cmd_inventory)
    gen = sub.add_parser("generate")
    gen.add_argument("--inventory", required=True)
    gen.add_argument("--out", required=True)
    gen.set_defaults(func=cmd_generate)
    conv = sub.add_parser("convert")
    conv.add_argument("--docs", required=True)
    conv.add_argument("--repo", required=True)
    conv.add_argument("--out", required=True)
    conv.set_defaults(func=cmd_convert)
    upd = sub.add_parser("update")
    upd.add_argument("--repo", required=True)
    upd.add_argument("--docs", required=True)
    upd.add_argument("--out", required=True)
    upd.set_defaults(func=cmd_update)
    rev = sub.add_parser("review")
    rev.add_argument("--docs", required=True)
    rev.add_argument("--inventory", required=True)
    rev.add_argument("--out", required=True)
    rev.set_defaults(func=cmd_review)
    idx = sub.add_parser("index")
    idx.add_argument("--docs", required=True)
    idx.add_argument("--out", required=True)
    idx.set_defaults(func=cmd_index)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
