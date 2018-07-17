from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product

# Create your views here.
# class SearchProductView(ListView):
#     template_name = "../templates/search/view.html"

#     def get_queryset(self, *args, **kwargs):
#         request = self.request
#         # To see que url query parameters
#         print(request.GET)
#         # the GET second parameter is the default (if term does not exist)
#         query = request.GET.get('q', None)
#         if query is not None:
#             lookups = Q(title__icontains=query) | Q(description__icontains=query)
#             return Product.objects.filter(lookups).distinct()
#         # If query is None podemos mostrar otra cosa por defecto:
#         # return Product.objects.none()
#         # o mostramos los featured products:
#         return Product.objects.features()
#         '''
#         __icontains = field contains this term
#         __iexact = field is exactly this
#         '''

# Now moving the get_queryset method to the products model manager:
class SearchProductView(ListView):
    template_name = "../templates/search/view.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        print(request.GET)
        query = request.GET.get('q', None)
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.features()
