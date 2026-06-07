from __future__ import annotations


def build_disclosure_contract() -> dict[str, object]:
    return {
        "schema": "pdd.disclosure.v1",
        "layers": [
            {
                "name": "inventory",
                "artifact": "inventory.json",
                "role": "source evidence inventory with authority and freshness metadata",
                "required": True,
            },
            {
                "name": "manifest",
                "artifact": "manifest.json",
                "role": "generated documentation manifest",
                "required": True,
            },
            {
                "name": "source_map",
                "artifact": "source-map.json",
                "role": "mapping from generated surfaces to source evidence",
                "required": True,
            },
            {
                "name": "review",
                "artifact": "review/",
                "role": "coverage, grounding, and regression receipts",
                "required": True,
            },
            {
                "name": "index",
                "artifact": "index.sqlite",
                "role": "optional searchable index for consumers",
                "required": False,
            },
        ],
        "answering_contract": {
            "generated_docs_are_source_of_truth": False,
            "must_verify_against": [
                "inventory.json",
                "source-map.json",
                "review/grounding.json",
                "overrides.jsonl",
                "stale-removals.jsonl",
            ],
        },
    }
