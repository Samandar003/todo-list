from distutils.log import Log
from unicodedata import name
from django.urls import path
# from .views import 
from .views import Task_list, Task_detailAPIView, TaskList
from .views import (
  TaskList, TaskDetail,
  TaskCreate, TaskUpdate, 
  TaskDelete, CustomLoginView,
  LogoutView,
  Register,
)


urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', TaskList.as_view(), name='tasks'),
    # path('tasks/<int:pk>/', Task_detailAPIView.as_view(), name='task_detail')
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('create-task/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
  
]

