# Democritus Html

[![PyPI](https://img.shields.io/pypi/v/d8s-html.svg)](https://pypi.python.org/pypi/d8s-html)
[![CI](https://github.com/democritus-project/d8s-html/workflows/CI/badge.svg)](https://github.com/democritus-project/d8s-html/actions)
[![Lint](https://github.com/democritus-project/d8s-html/workflows/Lint/badge.svg)](https://github.com/democritus-project/d8s-html/actions)
[![codecov](https://codecov.io/gh/democritus-project/d8s-html/branch/main/graph/badge.svg?token=V0WOIXRGMM)](https://codecov.io/gh/democritus-project/d8s-html)
[![The Democritus Project uses semver version 2.0.0](https://img.shields.io/badge/-semver%20v2.0.0-22bfda)](https://semver.org/spec/v2.0.0.html)
[![The Democritus Project uses black to format code](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://choosealicense.com/licenses/lgpl-3.0/)

Democritus functions<sup>[1]</sup> for working with HTML.

[1] Democritus functions are <i>simple, effective, modular, well-tested, and well-documented</i> Python functions.

We use `d8s` (pronounced "dee-eights") as an abbreviation for `democritus` (you can read more about this [here](https://github.com/democritus-project/roadmap#what-is-d8s)).

## Installation

```
pip install d8s-html
```

## Usage

You import the library like:

```python
from d8s_html import *
```

Once imported, you can use any of the functions listed below.

## Functions

  - ```python
    def html_text(html_content: StringOrBeautifulSoupObject) -> str:
        """."""
    ```
  - ```python
    def html_unescape(html_content: StringOrBeautifulSoupObject) -> str:
        """."""
    ```
  - ```python
    def html_escape(html_content: StringOrBeautifulSoupObject) -> str:
        """."""
    ```
  - ```python
    def html_to_markdown(html_content: StringOrBeautifulSoupObject, **kwargs) -> str:
        """Convert the html string to markdown."""
    ```
  - ```python
    def html_find_comments(html_content: StringOrBeautifulSoupObject) -> str:
        """Get a list of all of the comments in the html strings."""
    ```
  - ```python
    def html_soupify(html_string: str, parser: str = 'html.parser') -> bs4.BeautifulSoup:
        """Return an instance of beautifulsoup with the html."""
    ```
  - ```python
    def html_remove_tags(html_content: StringOrBeautifulSoupObject) -> bs4.BeautifulSoup:
        """."""
    ```
  - ```python
    def html_remove_element(html_content: StringOrBeautifulSoupObject, element_tag: str) -> bs4.BeautifulSoup:
        """."""
    ```
  - ```python
    def html_find_css_path(html_content: StringOrBeautifulSoupObject, css_path: str) -> ListOfBeautifulSoupTags:
        """Find the given css_path in the html_content."""
    ```
  - ```python
    def html_elements_with_class(
        html_content: StringOrBeautifulSoupObject, html_element_class: str
    ) -> ListOfBeautifulSoupTags:
        """Find all elements with the given class from the html string."""
    ```
  - ```python
    def html_elements_with_id(html_content: StringOrBeautifulSoupObject, html_element_id: str) -> ListOfBeautifulSoupTags:
        """Find all elements with the given html_element_id from the html_content."""
    ```
  - ```python
    def html_elements_with_tag(html_content: StringOrBeautifulSoupObject, tag: str) -> ListOfBeautifulSoupTags:
        """."""
    ```
  - ```python
    def html_headings_table_of_contents(html_content: StringOrBeautifulSoupObject) -> ListOfBeautifulSoupTags:
        """."""
    ```
  - ```python
    def html_headings_table_of_contents_string(
        html_content: StringOrBeautifulSoupObject, *, indentation: str = '  '
    ) -> str:
        """."""
    ```
  - ```python
    def html_headings(html_content: StringOrBeautifulSoupObject) -> ListOfBeautifulSoupTags:
        """."""
    ```
  - ```python
    def html_to_json(html_content: StringOrBeautifulSoupObject, *, convert_only_tables: bool = False):
        """Convert the html to json using https://gitlab.com/fhightower/html-to-json."""
    ```
  - ```python
    def html_soupify_first_arg_string(func):
        """Return a Beautiful Soup instance of the first argument (if it is a string)."""
    ```

## Development

👋 &nbsp;If you want to get involved in this project, we have some short, helpful guides below:

- [contribute to this project 🥇][contributing]
- [test it 🧪][local-dev]
- [lint it 🧹][local-dev]
- [explore it 🔭][local-dev]

If you have any questions or there is anything we did not cover, please raise an issue and we'll be happy to help.

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and Floyd Hightower's [Python project template](https://github.com/fhightower-templates/python-project-template).

[contributing]: https://github.com/democritus-project/.github/blob/main/CONTRIBUTING.md#contributing-a-pr-
[local-dev]: https://github.com/democritus-project/.github/blob/main/CONTRIBUTING.md#local-development-
