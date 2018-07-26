from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from orders.models import *


class OrderDetailsSerializer(ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = "__all__"



class OrdersSerializer(ModelSerializer):
    order_details = OrderDetailsSerializer(many=True)

    class Meta:
        model = Orders
        fields = ['id','customer','price','is_paid','order_details']

    def create(self, validated_data):
        order_detail_list =[]
        order_details = validated_data.pop("order_details")
        add_order = Orders.objects.create(**validated_data)
        for order_detail in order_details:
            unit_price= order_detail['unit_price']
            IGST = order_detail['IGST'] if order_detail['IGST'] else 0
            CGST = order_detail['CGST']if order_detail['CGST'] else 0
            quant = order_detail['quantity']if order_detail['quantity'] else 1
            GST = IGST+CGST
            total = unit_price*quant+order_detail['packaging_cost']+GST
            add_order_details = OrderDetails.objects.create(order_id=add_order.id,GST=GST,total_cost= total,**order_detail)
            order_detail_list.append(add_order_details)
        response_data = {'id':add_order.id,
                         'customer':add_order.customer,
                         'is_paid':add_order.is_paid,
                         'price':add_order.price,
                         'order_details':order_detail_list
                         }

        return response_data



class OrdersFullDetailsSerializer(ModelSerializer):
    order_details = OrderDetailsSerializer(many=True)
    # order_details = serializers.SerializerMethodField()
    # def get_order_details(self, id):
    #     qs = OrderDetails.objects.filter(is_active=True, order_id=id)
    #     serializer = OrderDetailsSerializer(instance=qs, many=True)
    #     print('serializer.data::', serializer.data)
    #     return serializer.data

    # print('order_details::', order_details)
    class Meta:
        model = Orders
        fields = ['id','customer_details','price','is_paid','created_at','order_details']




class CancelOrderSerializer(ModelSerializer):
    class Meta:
        model= Orders
        fields=['id']

    def update(self, instance, validated_data):
        instance.is_active=False
        instance.save()
        order_id=instance.id
        if order_id:
            order_details_data = OrderDetails.objects.filter(order_id=order_id)
            for order_data in order_details_data:
                order_data.is_active=False
                order_data.save()
        return instance

class CancelOrderByProductIdSerializer(ModelSerializer):

    class Meta:
        model=OrderDetails
        fields=['id']
    def update(self, instance, validated_data):
        instance.is_active = False
        order_id = instance.order_id
        instance.save()
        order_details_data = OrderDetails.objects.filter(order_id=order_id,is_active=True)
        price_list = [od_data.total_cost for od_data in order_details_data]
        total_price = 0
        for price in price_list:
            if price:
                total_price += price
        order_data = Orders.objects.filter(pk = order_id)
        for data in order_data:
            data.price = total_price
            data.save()
        return instance

class AppOrdersCountSerializer(ModelSerializer):
    class Meta:
        model = Orders
        fields = ['id','order_count']