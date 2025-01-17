from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.response import Response
from .serializers import BoardSerializer
from .models import Board
from rest_framework import viewsets
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend

'''
class BoardList(APIView):

    def get(self, request, format=None):  
        try:
            board_list = Board.objects.all()
            serializer = BoardSerializer(board_list, many=True)
            return Response(serializer.data)
        except AttributeError as e:
            print(e).
            return Response("message: error")

    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class BoardDetail(APIView):
    def get(self, request, pk):
        try:
            board = Board.objects.get(id=pk)
            serializer = BoardSerializer(board)
            return Response(serializer.data, status=201)
        except ObjectDoesNotExist as e:
            print(e)
            return Response({"message: error"})

    def delete(self, request, pk):
        try:
            board = Board.objects.get(id=pk)
            board.delete()
            return Response(status=200)
        except ObjectDoesNotExist as e:
            print(e)
            return Response({"message: not exist"})
'''


class BoardFilter(FilterSet):
    name = filters.CharFilter(field_name='name')
    school_id = filters.NumberFilter(method='filter_school_id')

    def filter_school_id(self, queryset, name, value):
        return queryset.filter(**{
            name: value,
        })

    class Meta:
        model = Board
        fields = ['name', 'school_id']


class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    queryset = Board.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BoardFilter
