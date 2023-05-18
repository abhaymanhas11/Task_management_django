from django.urls import path,include
from apps.todo import views
from apps.user import urls
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register("task-manager",views.TaskManagerAPI,basename="task-manager")
router.register("comment",views.CommentAPI,basename="comment")
router.register("feed-back",views.FeedbackAPI,basename="feed-back")
router.register("add-content",views.AllContentAPI,basename="add-content")
router.register("view-content",views.ViewContent,basename="view-content")

urlpatterns = [
    path("dashboard", views.FetchTask.as_view(), name="dashboard"),
    path("delete/<int:id>/", views.DeleteTask, name="deletetask"),
    path("task-details/<int:id>/", views.TaskDetails.as_view(), name="viewdetails"),
    path("task-details/<int:id>/comment", views.AddComment.as_view(), name="comments"),
    path("rating/<int:id>/",
        views.Rating.as_view(template_name="todo/viewdetails.html"),
        name="rate",
    ),
    path("addtask", views.AddTask.as_view(), name="addtask"),
    path("task-details/<int:id>/content", views.Contents.as_view(), name="addcontent"),
    path(
        "editcontent/<int:draft_id>/", views.EditContent.as_view(), name="editcontent"
    )
    # path('view-content/', views.ViewContent.as_view({'get':'list'}), name='view-content'),
    # path('view-content/<int:pk>/', views.ViewContent.as_view({'get':'retrieve'}), name='view-content'),
]+router.urls
