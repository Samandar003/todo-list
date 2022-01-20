from datetime import datetime
from django.shortcuts import render, redirect
from .models import Task
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TaskSerializer
from rest_framework.generics import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class CustomLoginView(LoginView):
  template_name = 'todo/login.html'
  fields = '__all__'
  redirect_authenticated_user = True
  
  def get_success_url(self) -> str:
    return reverse_lazy('tasks')  

class Register(FormView):
  template_name = 'todo/register.html'
  form_class = UserCreationForm
  redirect_authenticated_user = True
  success_url = reverse_lazy('tasks')
  def form_valid(self, form):
    user = form.save()
    if user is not None:
      login(self.request, user)
    return super(Register, self).form_valid(form)
  def get(self, *args, **kwargs):
    if self.request.user.is_authenticated:
      return redirect('tasks')
    return super(Register, self).get(*args, **kwargs)

class TaskList(LoginRequiredMixin, ListView):
  model = Task
  context_object_name = 'tasks'
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['tasks'] = context['tasks'].filter(user=self.request.user)
      context['count'] = context['tasks'].filter(complete=False).count()
      
      search_input = self.request.GET.get('search_area') or ''
      if search_input:
        context['tasks'] = Task.objects.filter(title__contains=search_input)
      context['search_input'] = search_input
      return context 
        
        
  # template_name = 'todo/task_list.html'
  
  
class TaskDetail(DetailView):
  model = Task
  context_object_name = 'task'
  # template_name = 'todo/task_detail.html'
  
class TaskCreate(LoginRequiredMixin, CreateView):
  model = Task
  fields = ['title', 'description', 'complete']
  success_url = reverse_lazy('tasks')
  def form_valid(self, form):
     form.instance.user = self.request.user
     return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
  model = Task
  fields = ['title', 'description', 'complete']
  success_url = reverse_lazy('tasks')
  
class TaskDelete(LoginRequiredMixin, DeleteView):
  model = Task  
  context_object_name = 'task'
  success_url = reverse_lazy('tasks')
  
  

class Task_list(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer
  # authentication_classes = [TokenAuthentication,]
  # permission_classes = [IsAuthenticated,]
  
  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

class Task_detailAPIView(APIView):
  def get(self, request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(task)
    return Response(serializer.data)
  def put(self, request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(task, data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 
