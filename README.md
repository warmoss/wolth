# solon

![PyPI version](https://img.shields.io/pypi/v/solon.svg)

solon is a useful toolkit.

* GitHub: https://github.com/warmoss/solon/
* PyPI package: https://pypi.org/project/solon/
* Created by: **[warmoss](https://audrey.feldroy.com/)** | GitHub https://github.com/warmoss | PyPI https://pypi.org/user/warmoss/
* Free software: MIT License

## Features

* TODO

## Documentation

Documentation is built with [Zensical](https://zensical.org/) and deployed to GitHub Pages.

* **Live site:** https://warmoss.github.io/solon/
* **Preview locally:** `just docs-serve` (serves at http://localhost:8000)
* **Build:** `just docs-build`

API documentation is auto-generated from docstrings using [mkdocstrings](https://mkdocstrings.github.io/).

Docs deploy automatically on push to `main` via GitHub Actions. To enable this, go to your repo's Settings > Pages and set the source to **GitHub Actions**.

## Development

To set up for local development:

```bash
# Clone your fork
git clone git@github.com:your_username/solon.git
cd solon

# Install in editable mode with live updates
uv tool install --editable .
uv tool install rust-just
winget install --id GitHub.cli
```

This installs the CLI globally but with live updates - any changes you make to the source code are immediately available when you run `solon`.

Run tests:

```bash
uv run pytest
```

Run quality checks (format, lint, type check, test):

```bash
just qa
```

## Author

solon was created in 2026 by warmoss.

Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.
