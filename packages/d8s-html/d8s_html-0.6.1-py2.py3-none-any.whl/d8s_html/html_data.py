import collections
import functools
import html
from typing import Union, List

import bs4

from .html_data_temp_utils import (
    html_soupify_first_arg_string,
    copy_first_arg,
    stringify_first_arg,
    request_first_arg_url,
)


Heading = collections.namedtuple('Heading', ['heading', 'children'])
StringOrBeautifulSoupObject = Union[str, bs4.BeautifulSoup]
ListOfBeautifulSoupTags = List[bs4.element.Tag]


@request_first_arg_url
@html_soupify_first_arg_string
def html_text(html_content: StringOrBeautifulSoupObject) -> str:
    html_content = html_remove_element(html_content, 'script')
    html_content = html_remove_element(html_content, 'style')
    html_content = html_remove_element(html_content, 'head')

    text = ' '.join(html_content.findAll(text=True))
    return text


@stringify_first_arg
def html_unescape(html_content: StringOrBeautifulSoupObject) -> str:
    return html.unescape(html_content)


@stringify_first_arg
def html_escape(html_content: StringOrBeautifulSoupObject) -> str:
    return html.escape(html_content)


@request_first_arg_url
@stringify_first_arg
def html_to_markdown(html_content: StringOrBeautifulSoupObject, **kwargs) -> str:
    """Convert the html string to markdown."""
    import html2text

    markdown_creator = html2text.HTML2Text(**kwargs)
    return markdown_creator.handle(html_content)


@request_first_arg_url
@html_soupify_first_arg_string
def html_find_comments(html_content: StringOrBeautifulSoupObject) -> str:
    """Get a list of all of the comments in the html strings."""
    # credit: https://stackoverflow.com/questions/33138937/how-to-find-all-comments-with-beautiful-soup
    return html_content.find_all(string=lambda text: isinstance(text, bs4.Comment))


@request_first_arg_url
def html_soupify(html_string: str, parser: str = 'html.parser') -> bs4.BeautifulSoup:
    """Return an instance of beautifulsoup with the html."""
    return bs4.BeautifulSoup(html_string, parser)


@request_first_arg_url
@html_soupify_first_arg_string
def html_remove_tags(html_content: StringOrBeautifulSoupObject) -> bs4.BeautifulSoup:
    text = ' '.join(html_content.findAll(text=True))
    return text


@request_first_arg_url
@html_soupify_first_arg_string
@copy_first_arg
def html_remove_element(html_content: StringOrBeautifulSoupObject, element_tag: str) -> bs4.BeautifulSoup:
    """."""
    [s.extract() for s in html_content(element_tag)]
    return html_content


# def html_find_xpath(html_content: str, x_path: str):
#     """Find the given x_path in the html_content."""
#     from lxml.html.soupparser import fromstring

#     root = fromstring(html_content)
#     elements = root.xpath(x_path)
#     return elements


@request_first_arg_url
@html_soupify_first_arg_string
def html_find_css_path(html_content: StringOrBeautifulSoupObject, css_path: str) -> ListOfBeautifulSoupTags:
    """Find the given css_path in the html_content."""
    # TODO: make sure this css path is working: soup.select('#emailrecentlist > a:nth-child(1)') on http://spam-report.email
    # see: https://stackoverflow.com/questions/24720442/selecting-second-child-in-beautiful-soup-with-soup-select
    elements = html_content.select(css_path)
    return elements


@request_first_arg_url
@html_soupify_first_arg_string
def html_elements_with_class(
    html_content: StringOrBeautifulSoupObject, html_element_class: str
) -> ListOfBeautifulSoupTags:
    """Find all elements with the given class from the html string."""
    return html_content.findAll(attrs={'class': html_element_class})


@request_first_arg_url
@html_soupify_first_arg_string
def html_elements_with_id(html_content: StringOrBeautifulSoupObject, html_element_id: str) -> ListOfBeautifulSoupTags:
    """Find all elements with the given html_element_id from the html_content."""
    return html_content.findAll(attrs={'id': html_element_id})


@request_first_arg_url
@html_soupify_first_arg_string
def html_elements_with_tag(html_content: StringOrBeautifulSoupObject, tag: str) -> ListOfBeautifulSoupTags:
    """."""
    return html_content.findAll(tag)


@request_first_arg_url
@html_soupify_first_arg_string
def html_headings_table_of_contents(html_content: StringOrBeautifulSoupObject) -> ListOfBeautifulSoupTags:
    data = []
    headings = html_headings(html_content)

    # TODO: add comments here...
    for heading in headings:
        if data == []:
            data.append(Heading(heading=heading, children=[]))
        else:
            if heading.name <= data[-1].heading.name:
                data.append(Heading(heading=heading, children=[]))
            else:
                data[-1].children.append(Heading(heading=heading, children=[]))

    return data


def _html_headings_toc(heading_named_tuples: ListOfBeautifulSoupTags, indentation: str, level: int = 0) -> str:
    s = ''
    for i in heading_named_tuples:
        s += f'{indentation*level}{i.heading.text}\n'
        s += _html_headings_toc(i.children, indentation, level + 1)

    return s


@request_first_arg_url
@html_soupify_first_arg_string
def html_headings_table_of_contents_string(
    html_content: StringOrBeautifulSoupObject, *, indentation: str = '  '
) -> str:
    table_of_contents = html_headings_table_of_contents(html_content)
    s = _html_headings_toc(table_of_contents, indentation)
    return s.rstrip()


@request_first_arg_url
@html_soupify_first_arg_string
def html_headings(html_content: StringOrBeautifulSoupObject) -> ListOfBeautifulSoupTags:
    heading_tags = ('h1', 'h2', 'h3', 'h4', 'h5', 'h6')
    headings = html_elements_with_tag(html_content, heading_tags)

    return headings


@request_first_arg_url
@stringify_first_arg
def html_to_json(html_content: StringOrBeautifulSoupObject, *, convert_only_tables: bool = False):
    """Convert the html to json using https://gitlab.com/fhightower/html-to-json."""
    import html_to_json

    if convert_only_tables:
        return html_to_json.convert_tables(html_content)
    else:
        return html_to_json.convert(html_content)


def html_soupify_first_arg_string(func):
    """Return a Beautiful Soup instance of the first argument (if it is a string)."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        first_arg = args[0]
        other_args = args[1:]

        if isinstance(first_arg, str):
            first_arg_soup = html_soupify(first_arg)
            return func(first_arg_soup, *other_args, **kwargs)
        else:
            return func(*args, **kwargs)

    return wrapper
