from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),

    path('teaser/', views.teaser_page, name='teaser_page'),
    path('teaser/create/', views.create_teaser_item, name='create_teaser'),
    path('teaser/edit/<int:pk>/', views.edit_teaser_item, name='edit_teaser'),
    path('teaser/delete/<int:pk>/', views.delete_teaser_item, name='delete_teaser'),

    path('catalog/', views.catalog_page, name='catalog_page'),
    path('catalog/delete/<int:item_id>/', views.delete_catalog_item, name='delete_catalog_item'),
    path('catalog/<int:item_id>/', views.catalog_detail, name='catalog_detail'),

    path('social/', views.social, name='social'),
    path('rules/', views.rules, name='rules'),
    path('how-to-order/', views.how_to_order, name='how_to_order'),
    
    path('feedback/', views.feedback_view, name='feedback'),
    path('admin-home/', views.admin_home_view, name='admin_home'),
    path('feedback/thank-you/', views.feedback_thankyou, name='feedback_thankyou'),
]