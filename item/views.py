from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Category, Item
from .forms import NewItemForm, EditItemForm

# Create your views here.
def items(request):
    search = request.GET.get('search' , '')
    categories = Category.objects.all()
    category_id = request.GET.get('category', 0)
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id = category_id)

    if search:
        # لو بحث هتعرض المنتجات اللي تحتوي علي الاسم
        items = items.filter(Q(name__icontains=search) | Q(desc__icontains=search))

    return render(request, 'item/items.html', {
        'items' : items,
        'search' : search,
        'categories' : categories,
        'category_id' : int(category_id)
        })

# --------------------------
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    # جلب المنتجات التي لها نفس الجاتيجوري وتكون غير مباعه مع عدم جلب المنج المفتوح حاليا 
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[:3]
    return render(request, 'item/detail.html', {'item' : item,'related_items' : related_items})

# -------------------
@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()
        
    return render(request, 'item/new.html', {
        'form' : form,
        'title' : 'New Item'
    })


# ----------------------
@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)
        
    return render(request, 'item/new.html', {
        'form' : form,
        'title' : 'Edit Item'
    })


@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()
    return redirect('dashboard:index')