from flask import render_template


class Template:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def render(self):
        return render_template(self.name, **self.args)


index = Template('index.html', {"title": 'Вешенбург'})
production = Template('production.html', {"title": 'Производство'})
about = Template('about.html', {"title": 'О нас'})
buy = Template('catalog.html', {'title': 'Каталог'})
