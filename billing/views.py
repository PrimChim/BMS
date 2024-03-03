from django.shortcuts import render, redirect
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Items, Bills, BillItems
from users.models import Customer
from .serializers import ItemsSerializer, BillsSerializer, BillItemsSerializer
from django.contrib.auth.decorators import login_required

def create_bill(request):
    if request.method == 'POST':
        customer_email = request.POST.get('customer-email')
        customer_id = Customer.objects.get(email=customer_email).id

        items = request.POST.getlist('item-name')
        quantities = request.POST.getlist('item-quantity')
        prices = request.POST.getlist('item-total')
        total = 0
        
        for i in range(len(items)):
            total += int(prices[i])
        bill = Bills(total_price=total, customer_id=customer_id)
        bill.save()

        for i in range(len(items)):
            item = Items.objects.get(name=items[i])
            bill_item = BillItems(quantity=quantities[i], bill=bill, item=item)
            bill_item.save()
        return render(request, 'billing/create-bill.html')
    return render(request, 'billing/create-bill.html')

@api_view(['GET','POST'])
@login_required
def view_bills(request):

    # POST request
    if request.method == 'POST':
        bill_id = int(request.data.get('bill-id'))
        try:
            bill = Bills.objects.get(id=bill_id)
            bill_items = BillItems.objects.filter(bill_id=bill)
            serializer = BillItemsSerializer(bill_items, many=True)
            return Response(serializer.data)
        except Bills.DoesNotExist:
            return Response({'message':'Bill not found'}, status=status.HTTP_404_NOT_FOUND)

    # GET request
    bills = Bills.objects.all()
    serializer = BillsSerializer(bills, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_items(request):
    serializer = ItemsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@login_required
def get_items(request):
    items = Items.objects.all()
    serializer = ItemsSerializer(items, many=True)
    return Response(serializer.data)