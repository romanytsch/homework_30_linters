"""
Заменим сообщение "The requested URL was not found on the server" на что-то более информативное.
Например, выведем список всех доступных страниц с возможностью перехода по ним.

Создайте Flask Error Handler, который при отсутствии запрашиваемой страницы будет выводить
список всех доступных страниц на сайте с возможностью перехода на них.
"""

from flask import Flask, render_template_string

app = Flask(__name__)

# Множество для хранения доступных endpoint'ов
allowed_endpoints = set()

def register_route(rule, **options):
    def decorator(f):
        endpoint = options.pop("endpoint", f.__name__)
        app.add_url_rule(rule, endpoint, f, **options)
        allowed_endpoints.add(endpoint)
        return f
    return decorator

@register_route('/dogs')
def dogs():
    return 'Страница с пёсиками'

@register_route('/cats')
def cats():
    return 'Страница с котиками'

@register_route('/cats/<int:cat_id>')
def cat_page(cat_id: int):
    return f'Страница с котиком {cat_id}'

@register_route('/index')
def index():
    return 'Главная страница'

@app.errorhandler(404)
def page_not_found(e):
    urls = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint in allowed_endpoints:
            # Отбираем только статические маршруты без параметров
            if '<' not in rule.rule and '>' not in rule.rule:
                urls.append(rule.rule)
    links_html = ''.join(f'<li><a href="{url}">{url}</a></li>' for url in sorted(urls))
    template = f'''
    <h1>404: Страница не найдена</h1>
    <p>Запрашиваемая страница не найдена. Вот список доступных страниц:</p>
    <ul>
        {links_html}
    </ul>
    '''
    return render_template_string(template), 404

if __name__ == '__main__':
    app.run(debug=True)
