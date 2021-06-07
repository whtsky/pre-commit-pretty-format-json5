# pre-commit-pretty-format-json5

A pre-commit hook that checks that all your JSON5 files are pretty.

## Usage

```yaml
- repo: https://github.com/whtsky/pre-commit-pretty-format-json5
  rev: "1.0.0"
  hooks:
    - id: pretty-format-json5
```

commandline options:

- `--no-autofix` - Don't automatically format json files
- `--indent ...` - Control the indentation (either a number for a number of spaces or a string of whitespace). Defaults to 2 spaces.
- `--ensure-ascii` converte unicode characters to escape sequences
- `--no-sort-keys` - when autofixing, retain the original key ordering (instead of sorting the keys)
- `--top-keys comma,separated,keys` - Keys to keep at the top of mappings.
