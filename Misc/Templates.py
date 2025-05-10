from flask import render_template


class Template:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def render(self, **kwargs):
        kwargs.update(self.args)
        return render_template(self.name, **kwargs)


index = Template('index.html', {"title": 'Вешенбург'})
production = Template('production.html', {"title": 'Производство'})
about = Template('about.html', {"title": 'О нас'})
catalog = Template('catalog.html', {'title': 'Каталог'})
login = Template('login.html', {'title': 'Вход администратора'})
dashboard = Template('dashboard.html', {'title': 'Панель управления'})
catalog_edit = Template('catalog_edit.html', {'title': 'Редактор каталога'})
newProduct = Template('product_edit.html', {'title': 'Добавление продукта'})
about_product = Template('about_product.html', {'title': 'Информация о продукте'})
cart = Template('cart.html', {'title': 'Корзина'})
make_order = Template('make_order.html', {'title': 'Офромление заказа'})