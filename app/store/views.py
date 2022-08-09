from django.shortcuts import render


def homePage(request):
    if request.method == 'GET':
        return render(request, 'store/index.html')