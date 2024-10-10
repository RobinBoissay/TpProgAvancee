from django.urls import path
from . import views
from django.views.generic import *

urlpatterns = [
    path('login/', views.ConnectView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.DisconnectView.as_view(), name='logout'),
    path('contact/', views.ContactView, name='contact'),
    path('email-sent/', views.EmailSent, name = 'email-sent'),
    path("home", views.AboutView.as_view(template_name="monapp/home.html"), name="home"),
    path("home/<param>", views.AboutView.as_view(template_name="monapp/home.html")),
    path("product/<int:pk>" ,views.ProductDetailView.as_view(), name="product-detail"),
    path("product/<int:pk>/update/",views.ProductUpdateView.as_view(), name="product-update"),
    path("product/list",views.ProductListView.as_view(),name="product-list"),
    path("product/add/",views.ProductCreateView.as_view(), name="product-add"),
    path("product/<pk>/delete/",views.ProductDeleteView.as_view(), name="product-delete"),

    path("productItem/<int:pk>" ,views.ProductItemDetailView.as_view(), name="productItem-detail"),
    path("productItem/<int:pk>/update/",views.ProductItemUpdateView.as_view(), name="productItem-update"),
    path("productItem/list",views.ProductItemListView.as_view(),name="productItem-list"),
    path("productItem/add/",views.ProductItemCreateView.as_view(), name="productItem-add"),
    path("productItem/<pk>/delete/",views.ProductItemDeleteView.as_view(), name="productItem-delete"),

    path("productAttribute/<int:pk>" ,views.ProductAttributeDetailView.as_view(), name="productAttribute-detail"),
    path("productAttribute/<int:pk>/update/",views.ProductAttributeUpdateView.as_view(), name="productAttribute-update"),
    path("productAttribute/list",views.ProductAttributeListView.as_view(),name="productAttribute-list"),
    path("productAttribute/add/",views.ProductAttributeCreateView.as_view(), name="productAttribute-add"),
    path("productAttribute/<pk>/delete/",views.ProductAttributeDeleteView.as_view(), name="productAttribute-delete"),

    path("fournisseur/add/",views.FournisseurCreateView.as_view(), name="fournisseur-add"),
    path("fournisseur/<int:pk>" ,views.FournisseurDetailView.as_view(), name="fournisseur-detail"),
    path("fournisseur/list",views.FournisseurListView.as_view(),name="fournisseur-list"),
    path("fournisseur/<pk>/delete/",views.FournisseurDeleteView.as_view(), name="fournisseur-delete"),
    path("fournisseur/<int:pk>/update/",views.FournisseurUpdateView.as_view(), name="fournisseur-update"),

    ]
