from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from .serializers import BoardSerializer
from .models import Board
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend

'''
class BoardList(APIView):

    def get(self, request, format=None):  # 모든 게시판
        try:
            boardlists = Board.objects.all()
            serializer = BoardSerializer(boardlists, many=True)
            # 리스트로 반환하는 boardlists
            return Response(serializer.data)
        except AttributeError as e:
            print(e)
            return Response("message: error")

    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def filter_school_id(self, queryset):
        filtered_queryset = filters.NumberFilter(field_name='school_id_id')
        return filtered_queryset

    class Meta:
        model = Board
        fields = ['name', 'school_id']



class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    queryset = Board.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BoardFilter

