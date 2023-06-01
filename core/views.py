from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from django.views.generic.edit import FormView
from core.forms import RegisterForm, NewsForm, DiscussionForm, UserUpdateForm, ProfileUpdateForm
from core.models import Post, News, Comment


# Create your views here.
class TitleMixin:
    title = None

    def get_title(self):
        return self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_title()
        return context


class NewsList(TitleMixin, ListView):
    model = News
    template_name = 'core/home_page.html'
    context_object_name = 'news'
    title = 'Wingman'


class NewsDetail(TitleMixin, DetailView):
    model = News
    template_name = 'core/news_detail.html'
    context_object_name = 'news_detail'
    title = "Новость"


class NewsCreate(TitleMixin, LoginRequiredMixin, CreateView):
    model = News
    template_name = 'core/news_create.html'
    context_object_name = 'news_create'
    form_class = NewsForm
    success_url = reverse_lazy('core:home_page')
    title = "Добавление новости"


class NewsUpdate(TitleMixin, LoginRequiredMixin, UpdateView):
    model = News
    template_name = 'core/news_update.html'
    context_object_name = 'news_update'
    form_class = NewsForm
    success_url = reverse_lazy('core:home_page')
    title = "Редактирование новости"


#    def form_valid(self, form):
#        messages.success(self.request, "Новость была обновлена успешно")
#        return super(NewsUpdate, self).form_valid(form)

#    def get_queryset(self):
#        base_qs = super(NewsUpdate, self).get_queryset()
#        return base_qs.filter(superuser=self.request.superuser)


class NewsDelete(TitleMixin, LoginRequiredMixin, DeleteView):
    model = News
    template_name = 'core/news_delete.html'
    context_object_name = 'news_delete'
    success_url = reverse_lazy('core:home_page')
    title = "Удаление новости"


#    def form_valid(self, form):
#        messages.success(self.request, "Новость была удалена успешно")
#        return super(NewsDelete, self).form_valid(form)

#    def get_queryset(self):
#        base_qs = super(NewsDelete, self).get_queryset()
#        return base_qs.filter(user=self.request.user)


class PostListView(TitleMixin, LoginRequiredMixin, ListView):
    model = Post
    template_name = 'core/posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    title = 'Обсуждения'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.get_queryset().count()
        return context


class PostCreateView(TitleMixin, LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'topic', 'caption', 'image']
    success_url = reverse_lazy('core:posts')
    title = "Добавление обсуждения"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(TitleMixin, LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'core/post_update.html'
    context_object_name = 'post_update'
    form_class = DiscussionForm
    success_url = reverse_lazy('core:posts')
    title = "Обновление обсуждения"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def only_author(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(TitleMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'core/post_delete.html'
    context_object_name = 'post_delete'
    success_url = reverse_lazy('core:posts')
    title = "Удаление обсуждения"

    def only_author(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required
def post_like(request):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=request.POST.get('post_id'))
        is_liked = False
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            is_liked = False
        else:
            post.likes.add(request.user)
            is_liked = True

        return HttpResponseRedirect(post.get_absolute_url())


@login_required
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    comment.delete()
    messages.success(request, f'Комментарий удалён!')
    return redirect(comment.post.get_absolute_url())


class LoginUser(TitleMixin, LoginView):
    redirect_authenticated_user = True
    template_name = 'core/login.html'
    context_object_name = 'login'
    title = 'Авторизация'

    def get_success_url(self):
        return reverse_lazy('core:home_page')

    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя или пароль')
        return self.render_to_response(self.get_context_data(form=form))


@login_required
def delete_user(request):
    context = {'title': 'Удаление аккаунта'}
    return render(request, 'core/delete_user.html', context)


@login_required
def delete_user_confirm(request):
    context = {}
    if request.user.is_authenticated:
        username = request.user.username
    try:
        u = User.objects.get(username=username)
        u.delete()
        context['msg'] = 'Аккаунт удалён'
    except User.DoesNotExist:
        context['msg'] = 'Аккаунта не существует'
    except Exception as e:
        context['msg'] = e.message

    messages.success(request, f' {username} account is deleted !')
    return redirect('core:home_page')


class RegisterView(TitleMixin, FormView):
    redirect_authenticated_user = True
    template_name = 'core/register.html'
    form_class = RegisterForm
    context_object_name = 'register'
    success_url = reverse_lazy('core:home_page')
    title = 'Регистрация'

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)


@login_required
def profile(request):
    if request.method == 'POST':
        uform = UserUpdateForm(request.POST, instance=request.user)
        pform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
    else:
        uform = UserUpdateForm(instance=request.user)
        pform = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'uform': uform,
        'pform': pform,
        'title': 'Обновить профиль'}
    return render(request, 'core/profile.html', context)

#    def form_valid(self, form):
#        messages.success(self.request, "Обсуждение было удалено успешно")
#        return super(DiscussionDelete, self).form_valid(form)

#    def get_queryset(self):
#        base_qs = super(DiscussionDelete, self).get_queryset()
#        return base_qs.filter(superuser=self.request.superuser)
