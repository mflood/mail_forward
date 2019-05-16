
from mail_forward_flask.message_tools.html_converter import HtmlConverter


def test_simple_function():
    t = HtmlConverter()
    e = t.return_string()
    assert "elephant" == e
