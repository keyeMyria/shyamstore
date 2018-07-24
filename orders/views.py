from django.shortcuts import render
from rest_framework.generics import*
from orders.serializers import *
from rest_framework.views import *
from rest_framework import filters

class OrdersCreateView(ListCreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


class OrdersDetailsReadView(ListAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersFullDetailsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('customer__id',)

    def get_queryset(self):
        if self.kwargs:
            order_id = self.kwargs['pk']
            if order_id:
                queryset = Orders.objects.filter(pk=order_id)
        else:
            queryset = Orders.objects.all()
        return queryset

class CancelOrderView(RetrieveUpdateAPIView):
    queryset = Orders.objects.all()
    serializer_class = CancelOrderSerializer

class CancelOrderByOrderDetailsIdView(RetrieveUpdateAPIView):
    queryset = OrderDetails.objects.all()
    serializer_class = CancelOrderByProductIdSerializer