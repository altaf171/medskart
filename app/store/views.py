from django.shortcuts import render

from .models import NavigationLink


def homePage(request):
    if request.method == 'GET':
        navigation_links = NavigationLink.objects.all()
        context={
            'navigation_links':navigation_links,
        }
        return render(request, 'store/index.html', context=context)