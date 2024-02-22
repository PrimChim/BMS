from django.shortcuts import render, redirect

# Create your views here.

def create_bill(request):
    return render(request, 'billing/create-bill.html')