from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic import FormView, CreateView, UpdateView
from django.views import View
from apps.todo.models import TaskManager, Comment, Feedback, AddContent
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.todo.forms import CommentForm, AddContentform
from apps.utils.enum import TaskStatus
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from  apps.todo.serializers import AllTaskSerializer,CommentSerializer,FeedbackSerializer,AddContentSerializer,CreateTaskSerializer,Userserializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from apps.utils.permissions import TaskAddpermission,FeedbackPermission,AddContentPermission,ViewContentPermission
from rest_framework import status
from rest_framework.response import Response



class TaskManagerAPI(ModelViewSet):
    serializer_class=CreateTaskSerializer
    permission_classes=[TaskAddpermission]

    def perform_create(self, serializer):
        obj = serializer.save()
        obj.created_by=self.request.user
        obj.save()


    def get_serializer(self, *args, **kwargs):
        if self.request.method in ['POST','PATCH','PUT']:
            serializer_class=self.get_serializer_class()
        else:
            serializer_class= AllTaskSerializer
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args,**kwargs)
    
    def get_queryset(self):
    
        if self.request.user.is_superuser == True:
            return TaskManager.objects.all()
        elif self.request.user.is_staff == True:
            return TaskManager.objects.filter(created_by=self.request.user)
        else:
            data = TaskManager.objects.filter(assigned_to=self.request.user)
            return data
        

class CommentAPI(ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer

class FeedbackAPI(ModelViewSet):
    permission_classes=[FeedbackPermission]
    queryset=Feedback.objects.all()
    serializer_class=FeedbackSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        return queryset.filter(task__created_by=user)



class AllContentAPI(ModelViewSet):
    permission_classes=[AddContentPermission]
    queryset=AddContent.objects.all()
    serializer_class=AddContentSerializer

    def create(self, request, *args, **kwargs):
        serializer = AddContentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            is_draft, task, content = serializer.validated_data['is_draft'],serializer.validated_data['task'],serializer.validated_data['content']
            t = TaskManager.objects.filter(id = task.id).first()
            if t.status==TaskStatus.Assigned.value:
                if  AddContent.objects.filter(task_id=t.id).exists():
                    obj = AddContent.objects.filter(task_id=task).first()
                    if is_draft==False:
                        task = TaskManager.objects.filter(pk=obj.task.id).first()
                        task.status=TaskStatus.Submitted.value
                        task.save()
                    obj.content=content
                    obj.is_draft=is_draft
                    obj.save()
                else:
                    serializer.save(created_by=self.request.user)
            else:
                if AddContent.objects.filter(task_id=task, is_draft=True).exists():
                    obj=AddContent.objects.filter(task_id=task, is_draft=True).first()
                    if is_draft==False:
                        task = TaskManager.objects.filter(pk=obj.task.id).first()
                        task.status=TaskStatus.Submitted.value
                        task.save()
                    obj.content=content
                    obj.is_draft=is_draft
                    obj.save()
                else:
                    serializer.save(created_by=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        obj=AddContent.objects.filter(pk=self.kwargs['pk']).first()
        if serializer.validated_data['is_draft'] ==False:
            task = TaskManager.objects.filter(pk=obj.task.id).first()
            task.status=TaskStatus.Submitted.value
            task.save()
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        serializer.save()

    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
class ViewContent(ModelViewSet):
    permission_classes=[ViewContentPermission]
    queryset=AddContent.objects.all()
    serializer_class=AddContentSerializer
    http_method_names = ['get','delete']

    def get_queryset(self):
            list_content=[]
            task=TaskManager.objects.filter(created_by=self.request.user)
            l = []
            for i in task:
                l.append(i.id)       
            return AddContent.objects.filter(task_id__in=l)
 

#django--------------------------------------------------------------------------
# -----------------dashboard-------------------------------------------------
class FetchTask(LoginRequiredMixin, ListView):
    model = TaskManager
    template_name = "todo/index.html"
    context_object_name = "tasks"
    login_url = "/"

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            return TaskManager.objects.all()
        elif self.request.user.is_staff == True:
            return TaskManager.objects.filter(created_by=self.request.user)
        else:
            data = TaskManager.objects.filter(assigned_to=self.request.user)
            return data

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff or self.request.user.is_superuser == True:
            context["type"] = True
        else:
            context["type"] = False
        return context


# ---------------------task details-----------------------------------
class TaskDetails(LoginRequiredMixin, View):
    login_url = "/"

    def get(self, request, id):
        task_details = TaskManager.objects.get(pk=id)
        show_comments = Comment.objects.filter(task_id=id)
        drafts = AddContent.objects.filter(
            created_by=self.request.user, is_draft=True
        ).first()

        try:    
            rating = Feedback.objects.get(task_id=id)
            rating = rating.rating
        except:
            rating = 0
        context = {
            "comment": show_comments,
            "i": task_details,
            "user": request.user.is_staff or request.user.is_superuser,
            "rating": [i for i in range(rating)],
            "drafts": drafts,
        }
        return render(request, "todo/viewdetails.html", context)


# ------------------------comment-------------------------------------

class AddComment(LoginRequiredMixin, FormView):
    login_url = "/"
    form_class = CommentForm
    template_name = "todo/comments.html"

    def form_valid(self, form):
        task = TaskManager.objects.get(pk=self.kwargs["id"])
        comment = Comment(
            task=task,
            parent_comment=form.cleaned_data["parent_comment"],
            body=form.cleaned_data["body"],
            created_by=self.request.user,
        )
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("viewdetails", kwargs={"id": self.kwargs["id"]})


# ------------------delete task---------------------------------
@login_required
def DeleteTask(request, id):
    p = TaskManager.objects.get(pk=id)
    p.delete()
    return HttpResponseRedirect("/todo/dashboard")


# -----------------feedback---------------------------
class Rating(View):
    template_name = ""

    def get(self, request, id):
        return render(request, self.template_name)

    def post(self, request, id):
        task = TaskManager.objects.get(pk=id)
        rate = request.POST["r"]
        feedback = Feedback(task=task, rating=(int(rate) + 1))
        feedback.save()
        return HttpResponseRedirect("/todo/dashboard")
        # try:
        #    if Feedback.task.id:
                # print("this is thwe existed feedback id",Feedback.task.id)
                # rate = (int(rate) + 1)
                # my_object = Feedback.objects.get(task_id=id)
                # my_object.rating = rate
                # my_object.save()
        # except Exception as e:

# -------------------Add task--------------------------------
class AddTask(CreateView):
    model = TaskManager
    fields = [
        "created_by",
        "title",
        "description",
        "assigned_to",
        "status",
        "estimated_time",
    ]
    template_name = "todo/addtask.html"

    def get_initial(self) -> Dict[str, Any]:
        return {"created_by": self.request.user}

    def get_success_url(self):
        return reverse_lazy("dashboard")


# ---------------------------------add contents------------------
class Contents(View):
    def get(self, request, id):
        status=TaskManager.objects.get(id=id).status
        print(status)
        if status in [TaskStatus.Assigned.value, TaskStatus.Revision_Required.value]:
            content = AddContent.objects.filter(task_id=id, is_draft=True).first()
            if content:
                return redirect("editcontent", draft_id=content.id)
            else:
                form = AddContentform()
                return render(request, "todo/addcontent.html", {"form": form})
        return render(request,"todo/alert.html")

    def post(self, request, id):
        form = AddContentform(request.POST)
        task = TaskManager.objects.get(pk=id)
        if form.is_valid():
            is_draft = form.cleaned_data["is_draft"]
            if is_draft == False:
                task = TaskManager.objects.filter(pk=id).first()
                task.status=TaskStatus.Submitted.value
                task.save()
            content = form.save(commit=False)
            content.task = task
            content.created_by = self.request.user
            content.save()
        return redirect("viewdetails", id=id)


class EditContent(View):
    def get(self, request, draft_id):
        content = AddContent.objects.filter(
            id=draft_id, created_by=self.request.user, is_draft=True
        ).first()
        form = AddContentform(instance=content)
        return render(request, "todo/editcontent.html", {"form": form})

    def post(self, request, draft_id):
        content = AddContent.objects.filter(
            id=draft_id, created_by=self.request.user, is_draft=True
        ).first()
        form = AddContentform(request.POST, instance=content)
        id = content.task.id
        if form.is_valid():
            is_draft = form.cleaned_data["is_draft"]
            if is_draft == False:
                task = TaskManager.objects.filter(pk=id).first()
                task.status=TaskStatus.Submitted.value
                task.save()
            form.save()
        return redirect("viewdetails", id=id)
