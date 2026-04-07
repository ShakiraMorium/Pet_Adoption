from django.shortcuts import redirect, render


def api_root_view(request):
    return redirect('api-root')


def home(request):
    return render(request, 'core/home.html')