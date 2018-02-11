from django.utils import timezone
from django.shortcuts import redirect
from blog.models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
import requests
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm

# Опять же, спасибо django за готовую форму аутентификации.
from django.contrib.auth.forms import AuthenticationForm

# Функция для установки сессионного ключа.
# По нему django будет определять, выполнил ли вход пользователь.
from django.contrib.auth import login

from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout


class LogoutView(View):
    @staticmethod
    def get(request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/")


class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "blog/login.html"

    # В случае успеха перенаправим на главную.
    success_url = "/post"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "blog/register.htm"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)
# end class


def hex2(n):
    h = hex(n)
    m = h[2:4]
    if len(m) < 2:
        m = '0' + m
    return m


def post_main(request):
    return render(request, 'blog/index.html', {'':''})


def post_url(request,pk):
    h=requests.head(pk)
    hh=h.headers;
    #hh=hh.replace("`","'");
    sz=hh['content-length'];
    h=''; 
    for i in hh : h=h+i+'|'+hh[i]+'\n';
    s='' 
    if int(sz)<300000: 
       x=requests.get(pk)
       xc=x.content;
       for i in xc: s=s+'%'+hex2(i);
    return render(request, 'blog/url.js', {'header1':h,'content1':s})


def post_any(request,pk):
    return render(request, 'blog/'+pk, {'':''})


def post_list(request):
    posts = Post.objects.order_by('edit_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_detail2(request, pk, ps):
    if ps != "123456789": pk = 0
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail2.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
# dump(request.data)
            k = len(Post.objects.all())
            if k > 0:
                p = Post.objects.filter(pk=k)[0]  # last record
               # print('p='+p.title)

               # print('='+form.fields)
                #if p.title == request.POST.title and p.text == request.POST.text:
                #    return redirect('post_list')
            # endif
            post = form.save(commit=False)
            post.author = request.user
            post.edit_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
        # endif
    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})
    # end if


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.edit_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})