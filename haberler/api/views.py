from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view

from haberler.models import Makale
from haberler.api.serializers import MakaleSerializer
from rest_framework.views import APIView


class MakaleListAPIView(APIView):
    @staticmethod
    def get(request):
        makaleler = Makale.objects.filter(aktif=True)
        serializer = MakaleSerializer(makaleler, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MakaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MakaleDetailAPIView(APIView):
    @staticmethod
    def get_object(pk):
        makale = get_object_or_404(Makale, pk=pk)
        return makale

    def get(self, request, pk):
        makale = self.get_object(pk=pk)
        serializer = MakaleSerializer(makale)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        makale = self.get_object(pk=pk)
        serializer = MakaleSerializer(makale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        makale = self.get_object(pk=pk)
        makale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# function based views
# @api_view(['GET', 'POST'])
# def makale_list_create_api_view(request):
#     if request.method == 'GET':
#         makaleler = Makale.objects.filter(aktif=True)
#         serializer = MakaleSerializer(makaleler, many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = MakaleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         else:
#             return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def makale_detail_api_view(request, pk):
#     try:
#         makale = Makale.objects.get(pk=pk)
#     except Makale.DoesNotExist:
#         return Response({'errors': {
#             'code': 404,
#             'message': f'belirtilen id ({pk}) ile makale bulunamadı.'
#         }}, status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = MakaleSerializer(makale)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#     elif request.method == 'PUT':
#         serializer = MakaleSerializer(makale, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         makale.delete()
#         return Response(data={'islem': {
#             'code': 204,
#             'message': f'({pk}) id li makale silindi.'
#         }}, status=status.HTTP_204_NO_CONTENT)
