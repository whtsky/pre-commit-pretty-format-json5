import os
import tempfile

import pytest

from pretty_format_json5 import _get_pretty_format


def test_vscode_settings_formatting():
    """Test that the JSON5 formatter properly formats a VS Code settings file."""

    # Input JSON5 with comments and mixed formatting
    input_json5 = """{
    "[yaml]": {
        "editor.tabSize": 2,
        "editor.formatOnSave": false,
        "editor.formatOnPaste": false,
        "editor.formatOnType": false
    },
    "json.schemas": [
        {
            "fileMatch": [
                "Taskfile.yml"
            ],
            "url": "./hack/schemas/taskfile.json"
        }
    ],
    "yaml.schemas": {
        "https://taskfile.dev/schema.json": "**/Taskfile.yml",
        "hack/schemas/mkdocs-material/schema.json": "mkdocs.yml"
        // "https://squidfunk.github.io/mkdocs-material/schema.json": "mkdocs.yml"
    },
    "files.associations": {
        "*.cheat": "markdown",
        "Makefile.ci": "makefile",
        "pyproject.toml*": "toml",
        "*.just": "just"
    },
    "pylint.interpreter": [
        "${workspaceFolder}/.venv/bin/python"
    ],
    "pylint.args": [
        "--enable=F,E,E1101",
        "--disable=C0111,E0401,C,W,E1205",
        "--max-line-length=120",
        "--load-plugins",
        "pylint_pydantic,pylint_per_file_ignores"
    ],
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.autoFormatStrings": true,
    "python.analysis.autoImportCompletions": true,
    "python.analysis.inlayHints.functionReturnTypes": true,
    "python.analysis.inlayHints.variableTypes": true,
    "python.analysis.inlayHints.callArgumentNames": "all",
    "python.terminal.activateEnvInCurrentTerminal": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/pycache": true
    },
    // Editor settings for Python files
    "editor.formatOnSave": true,
    "python.pythonPath": "${workspaceFolder}/.venv/bin/python",
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.analysis.inlayHints.pytestParameters": true,
    "python.analysis.diagnosticSeverityOverrides": {
        "reportUnusedImport": "none",
        "reportMissingImports": "error",
        "reportImportCycles": "error",
        "reportUnusedVariable": "none",
        "reportMissingTypeStubs": "none",
        "reportUnknownMemberType": "none",
        "reportUnusedFunction": "warning",
        "reportUnusedClass": "warning",
        "reportIncompatibleMethodOverride": "none",
        "reportGeneralTypeIssues": "information"
    },
    "notebook.formatOnSave.enabled": false,
    "[python]": {
        "editor.formatOnSave": false,
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.tabSize": 4,
        "editor.formatOnPaste": false,
        "editor.formatOnType": false
    },
    "[makefile]": {
        "editor.formatOnSave": true,
        "editor.tabSize": 4
    },
    "editor.inlineSuggest.showToolbar": "onHover",
    "editor.renderWhitespace": "all",
    "python.analysis.packageIndexDepths": [
        {
            "name": "langchain",
            "depth": 3,
            "includeAllSymbols": true
        },
        {
            "name": "langgraph",
            "depth": 3,
            "includeAllSymbols": true
        },
        {
            "name": "langchain_core",
            "depth": 3,
            "includeAllSymbols": true
        },
        {
            "name": "langchain_community",
            "depth": 3,
            "includeAllSymbols": true
        },
        {
            "name": "discord",
            "depth": 3,
            "includeAllSymbols": true
        },
        {
            "name": "discord.ext.test",
            "depth": 5,
            "includeAllSymbols": true
        },
        {
            "name": "dpytest",
            "depth": 5,
            "includeAllSymbols": true
        },
        {
            "name": "gallery_dl",
            "depth": 5,
            "includeAllSymbols": true
        },
        {
            "name": "loguru",
            "depth": 5,
            "includeAllSymbols": true
        }
    ],
    "python.analysis.extraPaths": [
        "."
    ],
    "python.analysis.completeFunctionParens": true,
    "python.analysis.indexing": true,
    "python.languageServer": "Pylance",
    "python.analysis.importFormat": "absolute",
    "python.analysis.stubPath": "${workspaceFolder}/typings",
    "python.analysis.autoSearchPaths": true,
    "python.analysis.diagnosticMode": "openFilesOnly",
    "python.analysis.includeAliasesFromUserFiles": true,
    "python.analysis.inlayHints.parameterNames": true,
    "python.analysis.inlayHints.parameterNamesStyle": "long",
    "python.analysis.inlayHints.callArgumentNamesStyle": "long",
    "python.analysis.enableEditableInstalls": true,
    "editor.semanticHighlighting.enabled": true,
    "workbench.editorAssociations": {
        "*.mdc": "default",
    },
    // SOURCE: https://github.com/allthingslinux/tux/blob/7a7cd918d1c96ef11a8e65e11fee2bd8c692df67/.vscode/settings.json
    "yaml.customTags": [
        "!ENV scalar",
        "!ENV sequence",
        "!relative scalar",
        "tag:yaml.org,2002:python/name:material.extensions.emoji.to_svg",
        "tag:yaml.org,2002:python/name:material.extensions.emoji.twemoji",
        "tag:yaml.org,2002:python/name:pymdownx.superfences.fence_code_format",
        "tag:yaml.org,2002:python/name:mermaid2.fence_mermaid_custom",
        "tag:yaml.org,2002:python/object/apply:pymdownx.slugs.slugify mapping"
    ],
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true
}"""

    # Expected output - properly formatted JSON5
    expected_output = """{
  "[makefile]": {
    "editor.formatOnSave": true,
    "editor.tabSize": 4,
  },
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnPaste": false,
    "editor.formatOnSave": false,
    "editor.formatOnType": false,
    "editor.tabSize": 4,
  },
  "[yaml]": {
    "editor.formatOnPaste": false,
    "editor.formatOnSave": false,
    "editor.formatOnType": false,
    "editor.tabSize": 2,
  },
  "editor.formatOnSave": true,
  "editor.inlineSuggest.showToolbar": "onHover",
  "editor.renderWhitespace": "all",
  "editor.semanticHighlighting.enabled": true,
  "files.associations": {
    "*.cheat": "markdown",
    "*.just": "just",
    "Makefile.ci": "makefile",
    "pyproject.toml*": "toml",
  },
  "files.exclude": {
    "**/*.pyc": true,
    "**/__pycache__": true,
    "**/pycache": true,
  },
  "files.insertFinalNewline": true,
  "files.trimTrailingWhitespace": true,
  "json.schemas": [
    {
      fileMatch: [
        "Taskfile.yml",
      ],
      url: "./hack/schemas/taskfile.json",
    },
  ],
  "notebook.formatOnSave.enabled": false,
  "pylint.args": [
    "--enable=F,E,E1101",
    "--disable=C0111,E0401,C,W,E1205",
    "--max-line-length=120",
    "--load-plugins",
    "pylint_pydantic,pylint_per_file_ignores",
  ],
  "pylint.interpreter": [
    "${workspaceFolder}/.venv/bin/python",
  ],
  "python.analysis.autoFormatStrings": true,
  "python.analysis.autoImportCompletions": true,
  "python.analysis.autoSearchPaths": true,
  "python.analysis.completeFunctionParens": true,
  "python.analysis.diagnosticMode": "openFilesOnly",
  "python.analysis.diagnosticSeverityOverrides": {
    reportGeneralTypeIssues: "information",
    reportImportCycles: "error",
    reportIncompatibleMethodOverride: "none",
    reportMissingImports: "error",
    reportMissingTypeStubs: "none",
    reportUnknownMemberType: "none",
    reportUnusedClass: "warning",
    reportUnusedFunction: "warning",
    reportUnusedImport: "none",
    reportUnusedVariable: "none",
  },
  "python.analysis.enableEditableInstalls": true,
  "python.analysis.extraPaths": [
    ".",
  ],
  "python.analysis.importFormat": "absolute",
  "python.analysis.includeAliasesFromUserFiles": true,
  "python.analysis.indexing": true,
  "python.analysis.inlayHints.callArgumentNames": "all",
  "python.analysis.inlayHints.callArgumentNamesStyle": "long",
  "python.analysis.inlayHints.functionReturnTypes": true,
  "python.analysis.inlayHints.parameterNames": true,
  "python.analysis.inlayHints.parameterNamesStyle": "long",
  "python.analysis.inlayHints.pytestParameters": true,
  "python.analysis.inlayHints.variableTypes": true,
  "python.analysis.packageIndexDepths": [
    {
      depth: 3,
      includeAllSymbols: true,
      name: "langchain",
    },
    {
      depth: 3,
      includeAllSymbols: true,
      name: "langgraph",
    },
    {
      depth: 3,
      includeAllSymbols: true,
      name: "langchain_core",
    },
    {
      depth: 3,
      includeAllSymbols: true,
      name: "langchain_community",
    },
    {
      depth: 3,
      includeAllSymbols: true,
      name: "discord",
    },
    {
      depth: 5,
      includeAllSymbols: true,
      name: "discord.ext.test",
    },
    {
      depth: 5,
      includeAllSymbols: true,
      name: "dpytest",
    },
    {
      depth: 5,
      includeAllSymbols: true,
      name: "gallery_dl",
    },
    {
      depth: 5,
      includeAllSymbols: true,
      name: "loguru",
    },
  ],
  "python.analysis.stubPath": "${workspaceFolder}/typings",
  "python.analysis.typeCheckingMode": "basic",
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.languageServer": "Pylance",
  "python.pythonPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvInCurrentTerminal": true,
  "workbench.editorAssociations": {
    "*.mdc": "default",
  },
  "yaml.customTags": [
    "!ENV scalar",
    "!ENV sequence",
    "!relative scalar",
    "tag:yaml.org,2002:python/name:material.extensions.emoji.to_svg",
    "tag:yaml.org,2002:python/name:material.extensions.emoji.twemoji",
    "tag:yaml.org,2002:python/name:pymdownx.superfences.fence_code_format",
    "tag:yaml.org,2002:python/name:mermaid2.fence_mermaid_custom",
    "tag:yaml.org,2002:python/object/apply:pymdownx.slugs.slugify mapping",
  ],
  "yaml.schemas": {
    "hack/schemas/mkdocs-material/schema.json": "mkdocs.yml",
    "https://taskfile.dev/schema.json": "**/Taskfile.yml",
  },
}
"""

    # Test the formatting
    result = _get_pretty_format(
        input_json5, indent=2, ensure_ascii=False, sort_keys=True, top_keys=[]
    )

    # Normalize whitespace for comparison
    expected_lines = [line.rstrip() for line in expected_output.strip().split("\n")]
    result_lines = [line.rstrip() for line in result.strip().split("\n")]

    # Print diff for debugging if test fails
    if expected_lines != result_lines:
        print("Expected:")
        for i, line in enumerate(expected_lines, 1):
            print(f"{i:3}: {line}")
        print("\nActual:")
        for i, line in enumerate(result_lines, 1):
            print(f"{i:3}: {line}")
        print("\nDifferences:")
        max_lines = max(len(expected_lines), len(result_lines))
        for i in range(max_lines):
            exp_line = expected_lines[i] if i < len(expected_lines) else "<missing>"
            res_line = result_lines[i] if i < len(result_lines) else "<missing>"
            if exp_line != res_line:
                print(f"Line {i+1}: expected '{exp_line}' got '{res_line}'")

    assert expected_lines == result_lines


def test_unquoted_keys_in_nested_objects():
    """Test that valid identifier keys are unquoted in nested objects."""

    input_json5 = """{
    "schemas": [
        {
            "fileMatch": ["*.json"],
            "url": "schema.json"
        }
    ]
}"""

    result = _get_pretty_format(
        input_json5, indent=2, ensure_ascii=False, sort_keys=True, top_keys=[]
    )

    # Should have unquoted keys for valid identifiers
    assert "fileMatch: [" in result
    assert 'url: "schema.json"' in result
    assert "schemas: [" in result  # schemas is a valid identifier, should be unquoted


def test_trailing_commas():
    """Test that trailing commas are added consistently."""

    input_json5 = """{
    "array": [
        "item1",
        "item2"
    ],
    "object": {
        "key": "value"
    }
}"""

    result = _get_pretty_format(
        input_json5, indent=2, ensure_ascii=False, sort_keys=True, top_keys=[]
    )

    # Should have trailing commas
    assert '"item1",' in result
    assert '"item2",' in result
    assert 'key: "value",' in result


def test_mixed_quoted_unquoted_keys():
    """Test handling of keys that need quotes vs those that don't."""

    input_json5 = """{
    "valid-identifier": "value1",
    "invalid.key": "value2",
    "123key": "value3",
    "valid_identifier": "value4",
    "$validKey": "value5"
}"""

    result = _get_pretty_format(
        input_json5, indent=2, ensure_ascii=False, sort_keys=True, top_keys=[]
    )

    # Keys that are valid identifiers should be unquoted
    assert '$validKey: "value5"' in result
    assert 'valid_identifier: "value4"' in result

    # Keys that are not valid identifiers should be quoted
    assert '"123key": "value3"' in result
    assert '"invalid.key": "value2"' in result
    assert '"valid-identifier": "value1"' in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
