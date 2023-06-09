from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from item.models import Item
from .models import Conversation
from .forms import ConversationMessageForm
# Create your views here.

@login_required
def new_conversation(request, item_pk):
    # اول حاجه جبنا المنتج 
    item = get_object_or_404(Item, pk=item_pk)

    # لو المالك للمنتج هو الشخص المسجل روح للداشبورد
    if item.created_by == request.user:
        return redirect('dashboard:index')
    
    # هاتلي المحادثات اللي بالاسم والايدي 
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    # لو فيه محادثة ادخل عليها باسمها
    if conversations:
        return redirect('conversation:detail', pk=conversations.first().id)

    # لو هوا كتب حاجه في المحادثة الجديدة
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            # لو كتب محادثة هتنشئها في الادمن
            conversation = Conversation.objects.create(item=item)
            # ضفلي اسم اللي بعث الرسالة
            conversation.members.add(request.user)
            # ضفلي اسم اللي اتبعتله الرسالة
            conversation.members.add(item.created_by)
            conversation.save()

            # قبل ماتحفظ الفورم
            conversation_message = form.save(commit=False)
            # قبل ماتحفظ الفورم ضيف الكونفرزاشن
            conversation_message.conversation = conversation
            # وضيف اللي عمل الكونفرزاشن الجديدة 
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('item:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new.html',{'form' : form})


@login_required
def inbox(request):
    # هاتلي المحادثات اللي كتبها الشخص المسجل
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html', {
        'conversations' : conversations,
    })


@login_required
def detail(request, pk):
    # فلتر بالاي دي وهاتلي المحادثة اللي رقمها كذا
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)
    
    # لو كتب حاجه ثاني في المحادثة
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        # احفظ اللي كتبه وضفلي المعلومات في قاعدة البيانات اللي هيا المحادثة واللي عملها
        conversation_message = form.save(commit=False)
        conversation_message.conversation = conversation
        conversation_message.created_by = request.user
        conversation_message.save()

        # احفظ كل المعلومات دي في المحادثة اللي جبناها بالرقم
        conversation.save()

        return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation' : conversation,
        'form' : form,
    })
