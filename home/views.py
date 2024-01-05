from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product
from . import tasks
from django.contrib import messages
from django.shortcuts import render, redirect


class HomeView(View):
    def get(self, request):
        products= Product.objects.filter(available= True)
        return render(request, 'home/home.html', {'products': products})


class ProductDetailView(View):
    def get(self, request, slug):
        product= get_object_or_404(Product, slug= slug)
        return render(request, 'home/product_detail.html', {'product': product})


class BucketHome(View):
    bucket_template= 'home/bucket.html'
 
    def get(self, request):
        objects= tasks.all_bucket_objects_task()
        return render(request, self.bucket_template, {'objects': objects})


class DeleteBucketObj(View): 
    def get(self, request, key):
        tasks.delete_bucket_object_task(key)
        messages.success(request, "your object will be delete soon", 'info')
        return redirect('home:bucket')
    