from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product
from . import tasks
from django.contrib import messages
from django.shortcuts import render, redirect
from utils import IsAdminUserMixin


class HomeView(View):
    def get(self, request):
        products= Product.objects.filter(available= True)
        return render(request, 'home/home.html', {'products': products})


class ProductDetailView(View):
    def get(self, request, slug):
        product= get_object_or_404(Product, slug= slug)
        return render(request, 'home/product_detail.html', {'product': product})


class BucketHome(IsAdminUserMixin, View):
    bucket_template= 'home/bucket.html'
 
    def get(self, request):
        objects= tasks.all_bucket_objects_task()
        return render(request, self.bucket_template, {'objects': objects})


class DeleteBucketObj(IsAdminUserMixin, View): 
    def get(self, request, key):
        tasks.delete_bucket_object_task(key)
        messages.success(request, "your object will be delete soon", 'info')
        return redirect('home:bucket')


class DownloadBucketObj(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.download_bucket_object_task(key)
        messages.success(request, "your object will be download soon", 'info')
        return redirect('home:bucket')
    

class UploadBucketObj(IsAdminUserMixin, View):
    def get(self, request):
        tasks.upload_bucket_object_task()
        messages.success(request, "your object will be upload soon", 'info')
        return redirect('home:bucket')
        