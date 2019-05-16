
from mail_forward_flask.message_tools import convert_html_to_text


def test_convert_snippet():
    html = "<h1>Your Bill</h1><p>$10</p>"
    expected_text = """# Your Bill

$10

"""
    as_text = convert_html_to_text(html)
    assert expected_text == as_text

def test_convert_page():

    html = """<html>
                <body>
                <div>
                <p>
                    Some text
                    <span>more text</span>
                    even more text
                </p>
                <ul>
                    <li>list item</li>
                    <li>yet another list item</li>
                </ul>
                </div>
                <p>Some other text</p>
                <ul>
                    <li>list item</li>
                    <li>yet another list item</li>
                </ul>
                <body>
                <html>"""

    expected_text = """Some text more text even more text

  * list item
  * yet another list item

Some other text

  * list item
  * yet another list item

"""
    as_text = convert_html_to_text(html)
    assert expected_text == as_text
