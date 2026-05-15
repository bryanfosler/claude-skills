# Install product-discovery plugin

## Symlink into Claude Code's local plugins directory

```bash
mkdir -p ~/.claude/plugins/local
ln -sf "/Users/bryan/Documents/Claude/product-discovery-plugin/product-discovery" ~/.claude/plugins/local/product-discovery
```

## Restart Claude Code

```
/exit
# then reopen
```

## Verify it loaded

In Claude Code:
```
/pd-status
```

Should print the plugin's status banner.

## First run

```
/pd-quick "your test market"
```

The quick mode runs D1-D3 only — frame, mine voices, JTBD. Takes ~20-30 min. Output lands in `./.discovery/<topic>/`.

## Uninstall

```bash
rm ~/.claude/plugins/local/product-discovery
```
