from typing import Any
from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView,FormView
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.
class TaskList(LoginRequiredMixin,ListView):    #各クラスベースVIEWの第一引数に「LoginRequiredMixin」を渡せばよい
    model = Task
    #template_name = ".html"
    context_object_name="tasks" # リストの名前を変える（default:object_list →　tasks）
    #redirect_field_name = "login" # エラーになるため、settings.py で「login」を設定する　→LOGIN_URL = "login"
    def get_context_data(self, **kwargs) :  # オーバーライド
        context = super().get_context_data(**kwargs)
        
        #context['programing']='python' # キー＆値を追加する
        #print(context)
        
        context['tasks']=context['tasks'].filter(user=self.request.user)  # tasksをログインしているユーザーでフィルタリング
        
        serchInputText = self.request.GET.get("search") or "" # 検索する値を取得、または、検索値がない時は、空とする
        #print(serchInputText)
        if serchInputText:       # 検索文字でフィルタリング
            context['tasks']=context['tasks'].filter(title__icontains=serchInputText) # tasksをフィルタリング(__icontains)
            
        context['search']=serchInputText #検索文字を残す
        
        return context
          
    #queryset = Task.objects.all()
    #queryset = Task.objects.filter(id=1)
    #def get_context_data(self, **kwargs):
        #context = super(TaskList, self).get_context_data(**kwargs)
        #context['tasks'] = self.get_queryset()
        #return context
    
class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    #template_name = ".html"
    context_object_name="task" # リストの名前を変える（default:object →　task)
    
class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    #fields="__all__" #["user", "title", "description", "completed"]
    fields=["id", "title", "description", "completed"]    #userを特定するため、__all__としない
    success_url=reverse_lazy("tasks") # 作成後に遷移したいURLを返す
    
    def form_valid(self, form): # オーバーライド
        form.instance.user=self.request.user   # 今ログインしているユーザーを有効化する
        return super().form_valid(form)    
    
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields="__all__" #["id", "title", "description", "completed"]
    success_url=reverse_lazy("tasks") # 作成後に遷移したいURLを返す    
    
class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name="task"
    fields="__all__" #["id", "title", "description", "completed"]
    success_url=reverse_lazy("tasks") # 作成後に遷移したいURLを返す

class TaskListLoginView(LoginView):
    fields="__all__" #すべてのusers
    template_name="todoapp/login.html" # HTMLファイルのあるディレクトリの名前を変える（default:registration/login.html→todoapp/login.html）
    
    def get_success_url(self):    # get_success_url()はリダイレクト先を提供します
        return reverse_lazy("tasks") # トップページに遷移する
    
class RegisterTodoApp(FormView):
    template_name="todoapp/register.html"
    form_class=UserCreationForm    # Djangoで用意されているFormを使用する
    success_url=reverse_lazy("tasks")
    
    def form_valid(self, form):
        user=form.save()           #保存が必要
        if user is not None:       # ユーザーの認証
            login(self.request, user)
        return super().form_valid(form)