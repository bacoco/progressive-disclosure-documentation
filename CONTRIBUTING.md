# Contributing

Keep changes scoped to the PDD engine.

Before opening a pull request:

```bash
python -m pip install -e ".[test]"
python -m pytest
pdd inventory --repo examples/minimal-repo --out /tmp/pdd/inventory.json
pdd generate --inventory /tmp/pdd/inventory.json --out /tmp/pdd/docs
pdd review --docs /tmp/pdd/docs --inventory /tmp/pdd/inventory.json --out /tmp/pdd/review
```

Generated artifacts must stay source-grounded.
