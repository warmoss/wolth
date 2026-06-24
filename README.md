# solan

![PyPI version](https://img.shields.io/pypi/v/solan.svg)

Solan is a useful toolkit.

* GitHub: https://github.com/warmoss/solan/
* PyPI package: https://pypi.org/project/solan/
* Created by: **[warmoss](https://audrey.feldroy.com/)** | GitHub https://github.com/warmoss | PyPI https://pypi.org/user/warmoss/
* Free software: MIT License

## Features

* TODO

## Documentation

Documentation is built with [Zensical](https://zensical.org/) and deployed to GitHub Pages.

* **Live site:** https://warmoss.github.io/solan/
* **Preview locally:** `just docs-serve` (serves at http://localhost:8000)
* **Build:** `just docs-build`

API documentation is auto-generated from docstrings using [mkdocstrings](https://mkdocstrings.github.io/).

Docs deploy automatically on push to `main` via GitHub Actions. To enable this, go to your repo's Settings > Pages and set the source to **GitHub Actions**.

## Development

To set up for local development:

```bash
# Clone your fork
git clone git@github.com:your_username/solan.git
cd solan

# Install in editable mode with live updates
uv tool install --editable .
```

This installs the CLI globally but with live updates - any changes you make to the source code are immediately available when you run `solan`.

Run tests:

```bash
uv run pytest
```

Run quality checks (format, lint, type check, test):

```bash
just qa
```

## Author

solan was created in 2026 by warmoss.

Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.
