# loads navigation list form database

from .ui_models import NavigationLink 

def get_navigation_links(request):
    """
    context processor to get navigation links from database

    """
    navlinks = NavigationLink.objects.all()

    return {"navlinks": navlinks}