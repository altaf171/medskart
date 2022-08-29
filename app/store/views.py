import imp
import re
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views.generic import DetailView

from . import ui_models

User = get_user_model()



class ProfilePage(DetailView):
    model: User



# def mobile(request):
# in future plan is to serve different pages for mobile devices
#     """Return True if the request comes from a mobile device."""

#     MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

#     if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
#         return True
#     else:
#         return False



def homePage(request):
    if request.method == 'GET':
        # home page baner slides
        banners = ui_models.Banner.objects.all()

        context={
            'request': request,
            'banners':banners
        }
        return render(request, 'store/index.html', context=context)