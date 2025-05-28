test:
	python -m pytest test_pretty_format_json5.py -v

fix:
	pre-commit run -a --show-diff-on-failure

smoke-test:
	python pretty_format_json5.py .vscode/settings.json
