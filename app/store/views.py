import re
from django.shortcuts import render

from .models import NavigationLink, Banner

#navlinks

navigation_links = NavigationLink.objects.all() 


def mobile(request):
    """Return True if the request comes from a mobile device."""

    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False

def homePage(request):
    if request.method == 'GET':
        # home page baner slides
        banners = Banner.objects.all()

        context={
            'navigation_links':navigation_links,
            'banners':banners
        }
        return render(request, 'store/index.html', context=context)