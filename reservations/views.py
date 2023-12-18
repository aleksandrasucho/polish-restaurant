from django.views import View
from django.shortcuts import render
from django.views import generic

class HomeView(generic.TemplateView):
    """
    View for the home page.
    """
    template_name = 'base.html'
    
    def get(self, request):
        return render(request, 'base.html', {})
    
class MenuView(generic.TemplateView):
    template_name = 'menu.html'
    
    def get(self, request):
        return render(request, 'menu.html')

#def home(request):
#   return render(request, 'base.html', {})

#def menu(request):
#   return render(request, 'menu.html')