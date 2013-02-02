from pygments import highlight
from pygments.lexers import CppLexer
from pygments.formatters import HtmlFormatter

code = 'int main()\n{\nreturn 0;\n}\n'
print highlight(code, CppLexer(), HtmlFormatter())
print HtmlFormatter().get_style_defs('.highlight')
