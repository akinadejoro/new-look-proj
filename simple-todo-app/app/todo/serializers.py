from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    # deadline =serializers.DateField(format="%Y-%m-%d")
    class Meta:
        model = Todo
        fields = "__all__"