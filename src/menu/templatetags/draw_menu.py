from django import template
from src.menu.models import MenuItem
from django.db.models import Q, Subquery
from django.utils.safestring import mark_safe
from collections import deque
from operator import or_, and_
from functools import reduce
import re

register = template.Library()


def serializer(menu_items: deque[MenuItem], level: int):
    menu_html = ['<ul  class="nav flex-column" style="padding-left:10px">']
    prev_level = -1
    for menu_item in menu_items:
        if prev_level < menu_item.level:
            menu_html.append('<ul style="padding-left:15px">')
        elif prev_level > menu_item.level:
            menu_html.append('</ul>')
            menu_html.append('</li>')
        else:
            menu_html.append('</li>')
        menu_html.append(f'<li><a href={menu_item.url(level)}>{menu_item}</a>')
        prev_level = menu_item.level
    menu_html.append('</li>')
    menu_html.append('</ul>')
    return '\n'.join(menu_html)


@register.simple_tag
def draw_menu(path: str):
    menu_path = list(filter(bool, re.findall(r'[^/]+', path)[::-1]))
    query = [Q(**{'parent__' * ind + 'name': name}) for ind, name in enumerate(menu_path)]
    parents = [('parent__' * ind).rstrip('__') for ind in range(1, len(menu_path))]
    menu_subquery = MenuItem.objects.select_related(*parents).filter(reduce(and_, query))
    level = len(menu_path) - 1
    menu_items_list = []
    for menu_item in range(level):
        menu_items_list += [Q(parent__pk__in=Subquery(menu_subquery.values(('parent__' * menu_item) + 'pk')))]
    menu_items_list += [Q(level=0)]
    menu_items_list = MenuItem.objects.select_related('parent').filter(reduce(or_, menu_items_list)).all()
    menu_items = deque()
    menu_items_list = sorted(menu_items_list, key=lambda x: (x.level, x.pk), reverse=True)
    parent_ind = None
    for menu_item in menu_items_list:
        if (
                parent_ind is None or
                menu_item == parent_ind or
                menu_items[0].level == menu_item.level and
                menu_items[0].pk > menu_item.pk
        ):
            menu_items.appendleft(menu_item)
            parent_ind = menu_item.parent
        else:
            menu_items.append(menu_item)
    return mark_safe(serializer(menu_items, level))
