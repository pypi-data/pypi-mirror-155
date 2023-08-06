import bs4
import pytest

from d8s_html import (
    html_to_markdown,
    html_unescape,
    html_escape,
    html_to_json,
    # html_find_xpath,
    html_headings,
    html_headings_table_of_contents_string,
    html_remove_tags,
    html_text,
    html_soupify,
    html_remove_element,
    html_soupify_first_arg_string,
)


def test_html_text_1():
    url = 'https://hightower.space/projects/one-million-api/'
    result = html_text(url)
    assert 'OneMillion API' in result
    assert '<script src="https://oss.maxcdn.com/html' not in result

    s = '''<script>blah</script><p>foo <a href="bingo">bar</a></p>'''
    result = html_text(s)
    assert result == 'foo bar'


def test_html_remove_tags_1():
    s = '<a href="https://hightower.space">foo</a>'
    result = html_remove_tags(s)
    assert result == 'foo'

    s = '<a href="https://hightower.space>">foo</a>'
    result = html_remove_tags(s)
    assert result == 'foo'

    url = 'https://hightower.space/projects/one-million-api/'
    result = html_remove_tags(url)
    assert 'OneMillion API' in result
    assert 'Nov 23, 2018' in result
    assert (
        '<img src="https://hightower.space/img/projects/onemillion-api.png" alt="" class="img-responsive">'
        not in result
    )


def test_html_remove_element_1():
    s = '<a href="https://hightower.space">foo</a>'
    result = html_remove_element(s, 'a')
    assert str(result) == ''

    s = '<a href="https://hightower.space">foo</a><p>bar</p>'
    result = html_remove_element(s, 'a')
    assert str(result) == '<p>bar</p>'

    # test immutability
    import sys

    # this is necessary for the test to pass
    sys.setrecursionlimit(3000)
    url = 'https://hightower.space/projects/one-million-api/'
    soup = html_soupify(url)
    original_li_count = len(soup('li'))
    result = html_remove_element(soup, 'li')
    subsequent_li_count = len(soup('li'))
    assert original_li_count == subsequent_li_count


def test_html_headings_table_of_contents_string_1():
    s = '<h1>Foo</h1><h3>Bar</h3>'
    result = html_headings_table_of_contents_string(s)
    print(result)
    assert (
        result
        == '''Foo
  Bar'''
    )

    s = '<h1>Foo</h1><h3>Bar</h3><h1>Buzz</h1>'
    result = html_headings_table_of_contents_string(s)
    print(result)
    assert (
        result
        == '''Foo
  Bar
Buzz'''
    )


def test_html_headings_1():
    s = '</pre></ul><p><hr><h3>Announced Prefixes</h3><ul><pre>'
    h3 = bs4.element.Tag(name='h3')
    h3.string = 'Announced Prefixes'
    result = html_headings(s)
    assert result == [h3]

    s = '<h1>Foo</h1><h3>Bar</h3><h1>Buzz</h1>'
    h1a = bs4.element.Tag(name='h1')
    h1a.string = 'Foo'
    h3 = bs4.element.Tag(name='h3')
    h3.string = 'Bar'
    h1b = bs4.element.Tag(name='h1')
    h1b.string = 'Buzz'
    result = html_headings(s)
    assert result == [h1a, h3, h1b]


# @pytest.mark.network
# def test_html_find_xpath_1():
#     from networking import get

#     url = 'http://spam-report.email'
#     html_string = get(url)
#     elements = html_find_xpath(html_string, '//*[@id="emailrecentlist"]/a')
#     assert len(elements) == 30


def test_html_to_markdown_1():
    assert html_to_markdown("<p>Test</p>") == 'Test\n\n'
    # make sure kwargs are passed into the html_2_text module properly
    assert html_to_markdown("<p>Test</p>", bodywidth=0) == 'Test\n'
    assert html_to_markdown("<h1>Bingo</h1><p>Test</p>") == '# Bingo\n\nTest\n\n'


def test_html_unescape():
    assert html_unescape('&lt;test&gt;') == '<test>'
    assert html_unescape('my cat &amp; dog') == 'my cat & dog'


def test_html_escape():
    assert html_escape('<test>') == '&lt;test&gt;'
    assert html_escape('my cat & dog') == 'my cat &amp; dog'


def test_html_text_1():
    assert html_text('<p>Testing<p>') == 'Testing'
    assert html_text('<h1>Bingo</h1>\n<p>Testing<p>') == 'Bingo \n Testing'


def test_html_to_json():
    html_string = """<head>
        <title>Test site</title>
        <meta charset="UTF-8"></head>"""

    output = html_to_json(html_string)
    print("output {}".format(output))
    assert output == {'head': [{'title': [{'_value': 'Test site'}], 'meta': [{'_attributes': {'charset': 'UTF-8'}}]}]}

    html_string = """<h1>Bingo</h1><table class="table table-striped table-bordered table-hover">
        <tr>
            <th>#</th>
            <th>Malware</th>
            <th>MD5</th>
            <th>Date Added</th>
        </tr>
        <tr>
            <td>25548</td>
            <td><a href="/stats/DarkComet/">DarkComet</a></td>
            <td><a href="/config/034a37b2a2307f876adc9538986d7b86">034a37b2a2307f876adc9538986d7b86</a></td>
            <td>July 9, 2018, 6:25 a.m.</td>
        </tr>
        <tr>
            <td>25547</td>
            <td><a href="/stats/DarkComet/">DarkComet</a></td>
            <td><a href="/config/706eeefbac3de4d58b27d964173999c3">706eeefbac3de4d58b27d964173999c3</a></td>
            <td>July 7, 2018, 6:25 a.m.</td>
        </tr></table>
        <p>This is just a test <span style="color: red;">of the emergency systems</span></p>"""
    tables = html_to_json(html_string, convert_only_tables=True)
    print(tables)
    assert tables == [
        [
            {
                '#': '25548',
                'Malware': 'DarkComet',
                'MD5': '034a37b2a2307f876adc9538986d7b86',
                'Date Added': 'July 9, 2018, 6:25 a.m.',
            },
            {
                '#': '25547',
                'Malware': 'DarkComet',
                'MD5': '706eeefbac3de4d58b27d964173999c3',
                'Date Added': 'July 7, 2018, 6:25 a.m.',
            },
        ]
    ]


@html_soupify_first_arg_string
def html_soupify_first_arg_string_test_func_a(a):
    """."""
    return a


def test_html_soupify_first_arg_string_1():
    result = html_soupify_first_arg_string_test_func_a('<p>hello</p>')
    assert isinstance(result, bs4.BeautifulSoup)

    result = html_soupify_first_arg_string_test_func_a(1)
    assert isinstance(result, int)
