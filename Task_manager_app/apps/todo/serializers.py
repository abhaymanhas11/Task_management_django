from rest_framework import serializers
from apps.todo.models import TaskManager,Comment,Feedback,AddContent
from django.contrib.auth import get_user_model
from apps.utils.enum import TaskStatus
# from django.contrib.auth.models import User
User=get_user_model()
# from apps.user.models import User

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','first_name','email']


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=TaskManager
        fields=['id','title','description','assigned_to','status','estimated_time']



class AddContentSerializer(serializers.ModelSerializer):
    class Meta:
        model=AddContent
        fields=['id','task','content','is_draft']

    def validate_task(self, task):
        if task.status in  [TaskStatus.Submitted.value,TaskStatus.Approved.value]:
            raise serializers.ValidationError("You have  already  submiited your work ")
        return task


class AllTaskSerializer(serializers.ModelSerializer):
    assigned_to=Userserializer()
    taskcontent=AddContentSerializer(read_only=True,many=True)
    class Meta:
        model=TaskManager
        fields=['id','title','description','assigned_to','status','taskcontent','estimated_time']


class CommentSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=Comment
        fields=['id','task','body']

    def create(self, validated_data):
        user=self.context['request'].user
        validated_data['created_by']=user
        task=validated_data['task']
        if task.created_by!=user  and task.assigned_to!=user:
            raise serializers.ValidationError(" you are not eligible to perform comment on this task")
        feedback= super().create(validated_data)
        return feedback
        
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model=Feedback
        fields=['id','task','rating']

    def create(self, validated_data):
        user=self.context['request'].user
        validated_data['created_by']=user
        task=validated_data['task']
        if task.created_by!=user:
            raise serializers.ValidationError(" you are not eligible to perform feedback on this task")
        feedback= super().create(validated_data)
        return feedback
  



    