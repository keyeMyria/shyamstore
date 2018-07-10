from django.shortcuts import render
from app_category.serializers import *
from rest_framework.generics import*
from rest_framework.response import Response

# Create your views here.
class CategoriesListReadView(ListAPIView):
    queryset = AppCategories.objects.filter(is_deleted=False)
    serializer_class = CategoriesListSerializer
    # def get_queryset(self):
    #     print(self.queryset.query) 829855
class CategoryByIdReadView(RetrieveAPIView):
    queryset = AppCategories.objects.filter(is_deleted=False)
    serializer_class = CategoriesListSerializer

    # def retrieve(self, request, *args, **kwargs):
    #     category_id = self.kwargs['pk']
    #     self.queryset = AppCategories.objects.filter(pk= category_id)
    #     serializer = CategoriesListSerializer(self.queryset, many=True)
    #     return Response(serializer.data)