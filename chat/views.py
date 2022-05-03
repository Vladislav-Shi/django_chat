from django.shortcuts import render, redirect
from .models import ChatModel, MessageModel, ChatUser
from django.views.generic.edit import CreateView
from .forms import RegisterForm, AddChatForm
from django.contrib.auth import login
from django.urls import reverse_lazy

# Create your views here.


def index(request):
    '''
    Страничка выбора комнаты, тут будет список комнат, а также возможность
    создать свою
    '''
    if not request.user.is_authenticated:
        return redirect('/signup/?m=1')
    message = ''
    if request.method == 'POST':
        # если пользователь создает чат
        add_form = AddChatForm(request.POST)
        if add_form.is_valid():
            user = ChatUser.objects.get(username=request.user.username)
            user.chat.add(add_form.save())
            # user.save()
            return redirect('/chat/' + str(add_form.cleaned_data['slug']) + '/')
        else:
            message = 'Чат уже существует или неверные значения полей'
    add_form = AddChatForm()
    user_chats = ChatUser.objects.get(username=request.user.username)
    user_chats = user_chats.chat.all()
    print(user_chats)
    context = {'user_chats': user_chats, 'form': add_form, 'message': message}
    return render(request, 'chat/index.html', context=context)


def room(request, room_name):
    if not request.user.is_authenticated:
        return redirect('/signup/?m=1')
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


class RegisterView(CreateView):
    '''
    Класс выводящий страницу регистрации
    '''
    model = ChatUser
    form_class = RegisterForm
    template_name = 'auth/signup.html'
    next_page = 'chat:index'
    success_url = reverse_lazy('chat:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # для того чтобы сообщить о том что был редирект со страницы чатов
        if 'm' in self.request.GET and self.request.GET['m'] == '1':
            context['message'] = 'Для перехода в выбор чата нужно быть авторизированным!'
        return context

    def form_valid(self, form):
        form.clean_password2()
        instance = form.save(commit=False)
        instance.set_password(form.cleaned_data['password1'])
        instance.save()
        login(self.request, instance)  # выполняет сразу же авторизацию
        return super().form_valid(form)
