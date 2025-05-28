from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import TeaserItem, CatalogItem, Feedback, CATEGORY_CHOICES
from .forms import TeaserItemForm, FeedbackForm
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from .utils import transfer_expired_teasers

def is_admin(user):
    return user.is_staff

def home(request):
    feedbacks = Feedback.objects.all().order_by('-created_at') if request.user.is_superuser else None
    return render(request, 'main/home.html', {'feedbacks': feedbacks})


def contact(request):
    return render(request, 'main/contact.html')

def about(request):
    return render(request, 'main/about.html')

def login_view(request):
    if request.method == 'POST':
        if 'visit_without_login' in request.POST:
            return redirect('home')

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user and user.is_staff:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'main/login.html', {'error': 'Invalid credential or not admin'})
        
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def teaser_page(request):
    transfer_expired_teasers()
    teasers = TeaserItem.objects.filter(Available__gte=timezone.now()).order_by('Available')
    paginator = Paginator(teasers, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/teaser.html', {
        'teasers': teasers,
        'page_obj': page_obj,
        })

@login_required
@user_passes_test(is_admin)
def create_teaser_item(request):
    if request.method == 'POST':
        form = TeaserItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('teaser_page')
    else:
        form = TeaserItemForm()
    return render(request, 'crud/teaser_create.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_teaser_item(request, pk):
    teaser = get_object_or_404(TeaserItem, pk=pk)
    if request.method == 'POST':
        form = TeaserItemForm(request.POST, request.FILES, instance=teaser)
        if form.is_valid():
            form.save()
            return redirect('teaser_page')
    else:
        form = TeaserItemForm(instance=teaser)
    return render(request, 'crud/teaser_edit.html', {'form': form, 'teaser': teaser})

@login_required
@user_passes_test(is_admin)
def delete_teaser_item(request, pk):
    teaser = get_object_or_404(TeaserItem, pk=pk)
    if request.method == 'POST':
        teaser.delete()
        return redirect('teaser_page')
    return render(request, 'crud/teaser_confirm_delete.html', {'teaser': teaser})

def catalog_page(request):
    query = request.GET.get('q')
    category = request.GET.get('category')

    items = TeaserItem.objects.all()

    if query:
        items = items.filter(
            Q(title__icontains=query) | 
            Q(seller_name__icontains=query)
        )

    if category in dict(CATEGORY_CHOICES):
        items = items.filter(category=category)

    items = items.order_by('-created_at')

    paginator = Paginator(items, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    bags = TeaserItem.objects.filter(category='bags')
    tops = TeaserItem.objects.filter(category='tops')
    dresses = TeaserItem.objects.filter(category='dress')
    bottoms = TeaserItem.objects.filter(category='bottom')

    transfer_expired_teasers()

    return render(request, 'home/catalog.html', {
        'page_obj': page_obj,
        'query': query,
        'category_choices': CATEGORY_CHOICES,
        'selected_category': category,
        'bags': bags,
        'tops': tops,
        'dresses': dresses,
        'bottoms': bottoms,
    })

def catalog_detail(request, item_id):
    item = get_object_or_404(TeaserItem, id=item_id)
    return render(request, 'home/catalog_detail.html', {'item': item})

@login_required
@user_passes_test(is_admin)
def delete_catalog_item(request, item_id):
    item = get_object_or_404(TeaserItem, id=item_id)
    item.delete()
    return redirect('catalog_page')

def social(request):
    return render(request, 'home/social.html')

def rules(request):
    return render(request, 'home/rules.html')

def how_to_order(request):
    return render(request, 'home/how_to_order.html')

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            if request.user.is_authenticated:
                feedback.user = request.user
            feedback.save()
            return redirect('feedback_thankyou')
    else:
        form = FeedbackForm()
    return render(request, 'home/feedback.html', {'form': form})

@login_required
def admin_home_view(request):
    if request.user.is_superuser:  # admin only
        feedbacks = Feedback.objects.all().order_by('-created_at')
        return render(request, 'home/admin_home.html', {'feedbacks': feedbacks})
    else:
        return redirect('home')  # prevent access by normal users
    
def feedback_thankyou(request):
    return render(request, 'main/feedback_thankyou.html')
