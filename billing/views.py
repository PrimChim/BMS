from django.shortcuts import render, redirect
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Items, Bills, BillItems, Business
from users.models import Customer
from .serializers import ItemsSerializer, BillsSerializer, BillItemsSerializer
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse

import nepali_datetime as ndt
from fpdf import FPDF

# billing API views

@api_view(['POST'])
@login_required
def create_bill_api(request):
    if request.method == 'POST':
        data = request.data
        customer_email = request.data.get('customer-email')
        customer_id = Customer.objects.get(email=customer_email).id

        items = request.data.get('items')
        quantities = request.data.get('quantity')
        total = request.data.get('total')
        date = request.data.get('bill-date')
        print(date)

        # convert date to english date from nepali date
        date = ndt.datetime.strptime(date, '%Y-%m-%d').to_datetime_date()

        tax_amount = request.data.get('tax-amount')

        total = float(total)

        # get the last bill number and increment it by 1
        last_bill = Bills.objects.last()
        if last_bill is None:
            bill_no = 1
        else:
            bill_no = last_bill.bill_no + 1

        bill = Bills(total_price=total, customer_id=customer_id, tax_amount=tax_amount, invoice_date=date, bill_no=bill_no)
        bill.save()

        for i in range(len(items)):
            item = Items.objects.get(name=items[i])
            item.stock -= int(quantities[i])
            item.save()
            bill_item = BillItems(quantity=quantities[i], bill=bill, item=item)
            bill_item.save()
        return Response({'success':'Bill Created Successfully!!!'}, status=status.HTTP_201_CREATED)
    return Response({'error' : 'Unsupported method used!!!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@login_required
def view_bills(request, id=None):

    page = request.GET.get('page')
    all_bills = request.GET.get('all')
    customer_pan = request.GET.get('customer_pan')

    customer = Customer.objects.filter(pan=customer_pan).first()

    if customer is not None:
        bills = Bills.objects.filter(customer_id=customer.id)
        serializer = BillsSerializer(bills, many=True)
        for data in serializer.data:
            gregorian_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

            # Convert the Gregorian date to a Nepali date object
            nepali_date = ndt.date.from_gregorian_date(gregorian_date)

            # Assign the Nepali date back to the data dictionary
            data['invoice_date'] = nepali_date

            data['invoice_date'] = ndt.datetime.strptime(data['invoice_date'], '%Y-%m-%d').to_nepali_date()
            data['invoice_date'] = data['invoice_date'].split('T')[0]
            data['customer_name'] = customer.name
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        data['customer_name'] = Customer.objects.get(id=data['customer_id']).name

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

import datetime
def generate_pdf(id):

    bill = Bills.objects.get(id=id)
    bill_items = BillItems.objects.filter(bill_id=bill)
    items = []
    for item in bill_items:
        item_data = {
            'item_name' : item.item.name,
            'quantity' : item.quantity,
            'unit_price' : item.item.price
        }
        items.append(item_data)

    business = Business.objects.first()

    invoice_data = {
        'invoice_number' : bill.bill_no,
        'customer_name' : Customer.objects.get(id=bill.customer_id).name,
        'items' : items
    }

    date = bill.invoice_date
    date = str(date).split(' ')[0]

    year = int(date.split('-')[0])
    month = int(date.split('-')[1])
    day = int(date.split('-')[2])
    print(date)

    invoice_date_nepali = ndt.date.from_datetime_date(datetime.date(year, month, day))

    pdf = FPDF()
    pdf.add_page()

    # Set font
    pdf.set_font("Arial", size=12)

    # Print invoice header
    pdf.cell(200, 10, txt="===================================================================================", ln=True, align='C')
    pdf.cell(200, 10, txt="            INVOICE", ln=True, align='C')
    pdf.cell(200, 10, txt="===================================================================================", ln=True, align='C')

    # Print business details
    pdf.cell(200, 10, txt=f"Business Name: {business.name}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Address: {business.address}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Phone: {business.phone}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Email: {business.email}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Website: {business.website}", ln=True, align='L')
    pdf.cell(200, 10, txt="-------------------------------------------------------------------------------------", ln=True, align='C')

    pdf.cell(200, 10, txt=f"Invoice Number: {invoice_data['invoice_number']}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Invoice Date: {invoice_date_nepali}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Customer Name: {invoice_data['customer_name']}", ln=True, align='L')
    pdf.cell(200, 10, txt="-------------------------------------------------------------------------------------", ln=True, align='C')

    # Print items table
    pdf.cell(0, 10, txt="  Item Name     |  Quantity  |  Unit Price  |  Amount  ", ln=True, align='L')
    pdf.cell(0, 10, txt="-------------------------------------------------------------------------------------", ln=True, align='L')
    total_amount = 0
    for item in invoice_data['items']:
        amount = item['quantity'] * item['unit_price']
        total_amount += amount
        pdf.cell(0, 10, txt=f"{item['item_name']:15} | {item['quantity']:10} | {item['unit_price']:12} | {amount:8}", ln=True, align='L')

    # Print total amount
    pdf.cell(200, 10, txt="-------------------------------------------------------------------------------------", ln=True, align='C')
    # tax amount
    pdf.cell(200, 10, txt=f"Tax Amount: {bill.tax_amount}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Total Amount: {total_amount}", ln=True, align='L')
    pdf.cell(200, 10, txt="===================================================================================", ln=True, align='C')

    # Output PDF as bytes
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_bytes

# generate pdf
@api_view(['GET'])
@login_required
def generate_invoice(request, id):
    pdf_bytes = generate_pdf(id)

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=invoice.pdf'

    return response

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

def calculate_pre_tax_price(price):
    return round(price / (1 + (13/100)),2)

@api_view(['POST'])
@login_required
def add_items(request):
    data = request.data
    copy_data = data.copy()
    copy_data['price'] = calculate_pre_tax_price(float(copy_data['price']))
    serializer = ItemsSerializer(data=copy_data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': 'Item successfully added!!!'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Error while uploading item!!!'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@login_required
def get_items(request):
    search = request.GET.get('search')
    page = request.GET.get('page')
    item_id = request.GET.get('id')
    items_all = request.GET.get('all')
    if items_all:
        items = Items.objects.all()
        serializer = ItemsSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if item_id is not None:
        item = Items.objects.get(id=item_id)
        serializer = ItemsSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

@api_view(['POST'])
@login_required
def update_item(request, id):
    try:
        item = Items.objects.get(id=id)

        data = request.data
        copy_data = data.copy()

        if float(item.price) != float(copy_data['price']):
            copy_data['price'] = calculate_pre_tax_price(float(copy_data['price']))

        serializer = ItemsSerializer(instance=item, data=copy_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':'Item updated successfully!!!'}, status=status.HTTP_200_OK)
        return Response({'error': 'An error occured while updating item!!!'}, status=status.HTTP_400_BAD_REQUEST)
    except Items.DoesNotExist:
        return Response({'error':'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        
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

# admin login required
@login_required
def business_settings(request):
    return render(request, 'billing/business-settings.html')