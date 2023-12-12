from django.shortcuts import redirect, render

from .models import MenuItem


def redirect_to_trailing_slash(request, path):
    return redirect(f'/{path}/')


def index(request):
    if not request.path.strip('/'):
        first_menu = MenuItem.objects.filter(level=0).first()
        return redirect(f'/{first_menu.name}/')
    context = {'path': request.path}
    return render(request, 'index.html', context)
