# Contributing

Keep changes scoped to the PDD engine.

Before opening a pull request:

```bash
python -m pytest
python -m pdd.cli inventory --repo examples/minimal-repo --out /tmp/pdd/inventory.json
python -m pdd.cli generate --inventory /tmp/pdd/inventory.json --out /tmp/pdd/docs
python -m pdd.cli review --docs /tmp/pdd/docs --inventory /tmp/pdd/inventory.json --out /tmp/pdd/review
```

Generated artifacts must stay source-grounded.
