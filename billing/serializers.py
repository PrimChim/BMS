from .models import Items, Bills, BillItems
from rest_framework import serializers

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'

class BillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bills
        fields = '__all__'

class BillItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillItems
        fields = '__all__'