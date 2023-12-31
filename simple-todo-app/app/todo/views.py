from django.shortcuts import render

# Create your views here.
from django.http.response import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.response import Response
from datetime import datetime
from django.utils import timezone

class TodoAPIView(APIView):

    # READ a single Todo
    def get_object(self, pk):
        try:
            return Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if pk:
            data = self.get_object(pk)
            serializer = TodoSerializer(data)
        else:
            data = Todo.objects.all()

            serializer = TodoSerializer(data, many=True)


        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data

        data["deadline"] = datetime.strptime(data["deadline"], "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )
        serializer = TodoSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        response = Response()

        response.data = {
            'message': 'Todo Created Successfully',
            'data': serializer.data
        }

        return response

    def put(self, request, pk=None, format=None):
        todo_to_update = Todo.objects.get(pk=pk)

        data=request.data

        data["deadline"] = datetime.strptime(data["deadline"], "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )
        serializer = TodoSerializer(instance=todo_to_update,data=data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        response = Response()

        response.data = {
            'message': 'Todo Updated Successfully',
            'data': serializer.data
        }

        return response

    def delete(self, request, pk, format=None):
        todo_to_delete =  Todo.objects.get(pk=pk)

        todo_to_delete.delete()

        return Response({
            'message': 'Todo Deleted Successfully'
        })