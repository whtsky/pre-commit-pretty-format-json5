# pre-commit-pretty-format-json5

A pre-commit hook that checks and formats JSON5 files with proper formatting. This tool ensures JSON5 files are consistently formatted with features like unquoted keys for valid identifiers, trailing commas, and proper indentation.

## Features

- **JSON5 Support**: Full JSON5 syntax support including comments, unquoted keys, and trailing commas
- **Smart Key Formatting**: Automatically unquotes valid JavaScript identifiers while keeping quotes where needed
- **Trailing Commas**: Adds trailing commas in JSON5 style for better diffs
- **Configurable Indentation**: Supports both space and tab indentation
- **Key Sorting**: Optional key sorting with ability to pin specific keys to the top
- **Unicode Handling**: Configurable ASCII conversion

## Usage

### As a pre-commit hook

```yaml
- repo: https://github.com/whtsky/pre-commit-pretty-format-json5
  rev: '1.0.0'
  hooks:
      - id: pretty-format-json5
```

### Command Line Usage

```bash
# Format specific files
python pretty_format_json5.py file1.json5 file2.json5

# Check formatting without making changes
python pretty_format_json5.py --no-autofix file.json5

# Custom indentation
python pretty_format_json5.py --indent 4 file.json5
python pretty_format_json5.py --indent "\t" file.json5

# Preserve key order
python pretty_format_json5.py --no-sort-keys file.json5

# Keep specific keys at top
python pretty_format_json5.py --top-keys "name,version,description" package.json5
```

## Command Line Options

- `--no-autofix` - Don't automatically format JSON5 files (show diff only)
- `--indent <value>` - Control indentation (number for spaces or string like "\t"). Defaults to 2 spaces
- `--ensure-ascii` - Convert Unicode characters to escape sequences (\uXXXX)
- `--no-sort-keys` - Retain original key ordering when formatting
- `--top-keys <keys>` - Comma-separated keys to keep at the top of mappings

## Examples

### Before and After

**Input:**

```json5
{
    scripts: {
        build: 'webpack',
        test: 'jest',
    },
    dependencies: {
        react: '^18.0.0',
    },
}
```

**Output:**

```json5
{
    dependencies: {
        react: '^18.0.0',
    },
    scripts: {
        build: 'webpack',
        test: 'jest',
    },
}
```

### VS Code Settings Example

Perfect for formatting `.vscode/settings.json` files:

**Input:**

```json5
{
    'python.analysis.typeCheckingMode': 'basic',
    'files.exclude': {
        '**/__pycache__': true,
        '**/*.pyc': true,
    },
}
```

**Output:**

```json5
{
    'files.exclude': {
        '**/*.pyc': true,
        '**/__pycache__': true,
    },
    'python.analysis.typeCheckingMode': 'basic',
}
```

## Development

### Installation

```bash
# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest json5
```

### Testing

```bash
# Run the test suite
python -m pytest test_pretty_format_json5.py -v

# Run specific test
python -m pytest test_pretty_format_json5.py::test_vscode_settings_formatting -v
```

### Key Features Validated by Tests

- Unquoted keys for valid JavaScript identifiers (`fileMatch`, `url`, etc.)
- Proper quoting for keys that need it (`"python.analysis.typeCheckingMode"`, `"**/*.pyc"`)
- Consistent trailing commas in JSON5 style
- Proper handling of nested objects and arrays
- Key sorting with configurable top-keys

## License

MIT License
