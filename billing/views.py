from django.shortcuts import render, redirect
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Items, Bills, BillItems
from users.models import Customer
from .serializers import ItemsSerializer, BillsSerializer, BillItemsSerializer
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# billing API views

@api_view(['POST'])
@login_required
def create_bill_api(request):
    if request.method == 'POST':
        data = request.data
        print(data)
        customer_email = request.data.get('customer-email')
        customer_id = Customer.objects.get(email=customer_email).id

        items = request.data.get('items')
        quantities = request.data.get('quantity')
        total = request.data.get('total')
        total = int(total)

        bill = Bills(total_price=total, customer_id=customer_id)
        bill.save()

        for i in range(len(items)):
            item = Items.objects.get(name=items[i])
            bill_item = BillItems(quantity=quantities[i], bill=bill, item=item)
            bill_item.save()
        return Response({'message':'Bill Created Successfully!!!'}, status=status.HTTP_201_CREATED)
    return Response({'message' : 'Unsupported method used!!!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@login_required
def view_bills(request, id=None):

    page = request.GET.get('page')
    all_bills = request.GET.get('all')

    if request.method == 'POST':
        bills = Bills.objects.filter(status='cancelled')
        serializer = BillsSerializer(bills, many=True)
        for data in serializer.data:
            data['invoice_date'] = data['invoice_date'].split('T')[0]
        return Response(serializer.data)

    # get bill details
    if id is not None:
        bill_id = id
        try:
            bill = Bills.objects.get(id=bill_id)
            bill_items = BillItems.objects.filter(bill_id=bill)
            serializer = BillItemsSerializer(bill_items, many=True)
            for data in serializer.data:
                item_id = data['item']
                item = Items.objects.get(id=item_id)
                item_name = item.name
                data['item'] = item_name
                price = item.price
                data['price'] = price
            customer = Customer.objects.filter(id=bill.customer_id).first()
            billing_details = {
                'total' : bill.total_price,
                'billed_to' : customer.name,
                'invoice_date' : bill.invoice_date,
                'customer_pan' : customer.pan,
                'bill_status' : 'cancelled' if bill.status == 'cancelled' else 'regular'
            }
            data = serializer.data

            data.append(billing_details)
            return Response(data)
        except Bills.DoesNotExist:
            return Response({'message':'Bill not found'}, status=status.HTTP_404_NOT_FOUND)

    # GET request
    bills = Bills.objects.filter(status='regular')
    serializer = BillsSerializer(bills, many=True)
    for data in serializer.data:
        data['invoice_date'] = data['invoice_date'].split('T')[0]

    if all_bills:
        return Response(serializer.data, status=status.HTTP_200_OK)

    paginator = Paginator(serializer.data, 5)
    page_obj = []
    if page is not None:
        page_obj = paginator.page(page).object_list
    else:
        page_obj = paginator.page(1).object_list
    page_obj.append(paginator.num_pages)
    return Response(page_obj, status=status.HTTP_200_OK)

# delete bill
@api_view(['GET', 'POST'])
@login_required
def cancel_bill(request, id):
    if request.method == 'GET':
        try:
            bill = Bills.objects.get(id=id)
            bill.status = 'cancelled'
            bill.save()
            return Response({'message':'Bill Cancelled Successfully!!!'}, status=status.HTTP_200_OK)
        except Bills.DoesNotExist:
            return Response({'error':'Bill not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        try:
            bill = Bills.objects.get(id=id)
            bill.status = 'regular'
            bill.save()
            return Response({'message':'Bill Restored Successfully!!!'}, status=status.HTTP_200_OK)
        except Bills.DoesNotExist:
            return Response({'error':'Bill not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error':'Unsupported method used!!!'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_items(request):
    serializer = ItemsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': 'Item successfully added!!!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@login_required
def get_items(request):
    search = request.GET.get('search')
    page = request.GET.get('page')
    if search is not None:
        items = Items.objects.filter(name__contains=search)
        serializer = ItemsSerializer(items, many=True)

        paginator = Paginator(serializer.data, 5)

        if page is not None:
            page_obj = paginator.page(page).object_list
            page_obj.append(paginator.num_pages)
            return Response(page_obj, status=status.HTTP_200_OK)
        
        page_obj = paginator.page(1).object_list
        page_obj.append(paginator.num_pages)
        return Response(page_obj, status=status.HTTP_200_OK)

    items = Items.objects.all()
    serializer = ItemsSerializer(items, many=True)

    paginator = Paginator(serializer.data, 5)
    if page is not None:
        page_obj = paginator.page(page).object_list
        page_obj.append(paginator.num_pages)
        return Response(page_obj, status=status.HTTP_200_OK)

    page_obj = paginator.page(1).object_list
    page_obj.append(paginator.num_pages)
    return Response(page_obj, status=status.HTTP_200_OK)

# billing frontend views

@login_required
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
        return render(request, 'billing/create-bill.html',{'message':'Bill Created Successfully!!!'})
    return render(request, 'billing/create-bill.html')

@login_required
def dashboard(request):
    return render(request, 'billing/dashboard.html')

@login_required
def view_bills_frontend(request):
    return render(request, 'billing/view-bills.html')

@login_required
def items_frontend(request):
    return render(request, 'billing/items.html')