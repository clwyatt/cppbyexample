from string import Template
import re, os, shutil

from pygments import highlight
from pygments.lexers import CppLexer
from pygments.formatters import HtmlFormatter

from utils import pairwise

def convert_name_to_file(name, extension = ''):
    return name.lower().replace(' ', '-') + extension

def render_index(examples):
    ExampleListRender = ""
    for line in examples.split('\n'):
        line = line.strip()
        linkname = convert_name_to_file(line, '.html')
        if len( line ) != 0:
            ExampleListRender = ExampleListRender + '<li><a href="' + linkname + '">' + line + '</a></li>\n'

    with open('templates/index.tmpl', 'r') as content_file:
        content = content_file.read()

    s = Template(content)

    with open('public/index.html', 'w') as content_file:
        content_file.write( s.substitute(ExampleList=ExampleListRender) )


def extract_example_blocks(example_name):
    path = os.path.join("examples",
                        convert_name_to_file(example_name),
                        convert_name_to_file(example_name, ".cc"))

    with open(path, 'r') as example_file:
        example = example_file.read()

    block = [True,'']
    blocks = []
    for line in example.split('\n'):
        comment = (re.search('^//', line.strip() ) != None)

        if block[0] and comment:
            block[1]+=' '
            block[1]+=line.strip()[2:]
            continue

        if block[0] and not comment:
            blocks.insert(len(blocks), tuple(block))
            block[0] = False
            block[1] = line
            continue

        if not block[0] and not comment:
            block[1]+='\n'
            block[1]+=line
            continue

        if not block[0] and comment:
            blocks.insert(len(blocks), tuple(block))
            block[0] = True
            block[1] = line.strip()[2:]
            continue

    blocks.insert(len(blocks), tuple(block))
    return blocks

def render_examples(examples):
    for current, nextup in pairwise( examples.split('\n') ):
        current = current.strip()
        if len( current ) != 0:
            blocks = extract_example_blocks(current)

            BlockRender = ""
            count = 0
            for flag, value in blocks:
                if(count == 0):
                    BlockRender += '<tr>\n'
                if(count == 2):
                    BlockRender += '</tr>\n'
                    count = 0
                if flag:
                    BlockRender += '<td class="doc">\n'
                    BlockRender += value
                    BlockRender += '\n</td>\n'
                    count += 1
                else:
                    BlockRender += '<td class="code"><pre class="code">\n'
                    BlockRender += highlight(value, CppLexer(), HtmlFormatter())
                    BlockRender += '</pre>\n</td>\n'
                    count += 1

        NextRender = ''
        if nextup != None:
            next_html_name = convert_name_to_file(nextup.strip(), '.html')
            NextRender = '<p>Next example: <a href="' + next_html_name + '">' + nextup + '</a></p>'

        with open('templates/example.tmpl', 'r') as template_file:
            content = template_file.read()

        s = Template(content)

        html_name = os.path.join('public', convert_name_to_file(current, '.html'))
        with open(html_name, 'w') as output_file:
            output_file.write( s.substitute(Block=BlockRender, ExampleName=current, NextBlock=NextRender) )

if __name__ == "__main__":

    # recreate public directory
    pwd = os.getcwd()
    public_dir = os.path.join(pwd, 'public')
    template_dir = os.path.join(pwd, 'templates')
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    os.mkdir(public_dir)
    shutil.copy(os.path.join(template_dir, 'site.css'), public_dir)

    with open('examples.txt', 'r') as examples_file:
        examples = examples_file.read()

    examples = os.linesep.join([s for s in examples.splitlines() if s])

    render_index(examples)
    render_examples(examples)
