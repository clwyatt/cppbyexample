from string import Template

if __name__ == "__main__":
    with open('examples.txt', 'r') as examples_file:
        examples = examples_file.read()

    ExampleListRender = ""
    for line in examples.split('\n'):
        line = line.strip()
        if len( line ) != 0:
            ExampleListRender = ExampleListRender + "<li>" + line + "</li>\n"

    with open('templates/index.tmpl', 'r') as content_file:
        content = content_file.read()

    s = Template(content)

    with open('public/index.html', 'w') as content_file:
        content_file.write( s.substitute(ExampleList=ExampleListRender) )
