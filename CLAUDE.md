# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains a pre-commit hook that checks and formats JSON5 files. It ensures JSON5 files are properly formatted according to specified configuration options.

## Code Structure

- `pretty_format_json5.py`: The main module containing the JSON5 formatting logic
- `setup.py`: Package configuration for installation
- `test_pretty_format_json5.py`: Test suite validating formatting behavior

## Development Commands

### Installation

```bash
# Install the package locally in development mode
pip install -e .

# Install development dependencies
pip install pre-commit pytest json5
```

### Testing

#### Run the Test Suite

```bash
# Run all tests
python -m pytest test_pretty_format_json5.py -v

# Run a specific test
python -m pytest test_pretty_format_json5.py::test_vscode_settings_formatting -v

# Run tests with coverage
python -m pytest test_pretty_format_json5.py --cov=pretty_format_json5
```

#### Manual Testing

Test the formatter with specific files:

```bash
# Run the formatter on specific files
python pretty_format_json5.py file1.json5 file2.json5

# Run with specific options
python pretty_format_json5.py --indent 4 --ensure-ascii --no-sort-keys file.json5

# Test without autofix to see diff
python pretty_format_json5.py --no-autofix file.json5
```

#### Example Test Cases

The test suite includes validation for:

- VS Code settings.json formatting (complete before/after example)
- Unquoted keys for valid JavaScript identifiers
- Trailing commas in JSON5 style
- Mixed quoted/unquoted key handling
- Nested object and array formatting

### Releasing

Update the version in `setup.py` and create a new git tag matching the version.

## Command Line Options

- `--no-autofix`: Don't automatically format JSON5 files
- `--indent ...`: Control indentation (number for spaces or string of whitespace), defaults to 2 spaces
- `--ensure-ascii`: Convert Unicode characters to escape sequences
- `--no-sort-keys`: Retain original key ordering when formatting
- `--top-keys comma,separated,keys`: Keys to keep at the top of mappings
