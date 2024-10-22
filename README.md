# Quick and dirty code to scrape the online book for the computational physics course

This is useful, because it allows you to search for keywords for the whole book, which you cannot do in the website itself.

# Installation

Requires poetry.

To install poetry you require pipx

```bash
pip install pipx
pipx install poetry
```

Then you can install the project dependencies with

```bash
poetry install
```

# Setup

Requires a '.pass' file in the book folder, where your password for the online course website is stored

It may also require an 'images' folder in 'book'

# Usage

To run the code, change directory to the 'book' folder. Then run,

```bash
poetry run python main.py
```

This will create an html file that you can view in your browser.
