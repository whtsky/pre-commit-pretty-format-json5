from setuptools import setup


setup(
    name="pretty_format_json5",
    version="0.0.1",
    py_modules=["pretty_format_json5"],
    install_requires=["json5==0.9.5"],
    entry_points={
        "console_scripts": ["pretty-format-json5=pretty_format_json5:main"],
    },
)
