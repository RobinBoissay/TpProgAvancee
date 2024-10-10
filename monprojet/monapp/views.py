from django.forms import BaseModelForm
from django.shortcuts import render
from django.http import *
from monapp.models import Product, ProductAttributeValue, Status, ProductItem, ProductAttribute, Fournisseur
from django.views.generic import *

from monapp.froms import *

from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.core.mail import send_mail

from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

class HomeView(TemplateView):
    
    template_name = "monapp/home.html"
    def post(self, request, **kwargs):
        return render(request, self.template_name)
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['titreh1'] = "Hello DJANGO"
        return context
    
class AboutView(TemplateView):
    template_name = "monapp/home.html"
    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        texte = self.kwargs.get('param') or "Hello"
        context['titreh1'] = "About us..." + texte
        return context
    def post(self, request, **kwargs):
        return render(request, self.template_name)

class ProductListView(ListView):

    model = Product
    template_name = "monapp/list_products.html"
    context_object_name = "products"

    def get_queryset(self ) :
        return Product.objects.order_by("price_ttc")
    
    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des produits"
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "monapp/detail_product.html"
    context_object_name = "product"
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail produit"
        return context
    

def ContactView(request):
    titreh1 = "Contact us !"
    if request.method=='POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            send_mail(
            subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MonProjet Contact Us form',
            message=form.cleaned_data['message'],
            from_email=form.cleaned_data['email'],
            recipient_list=['admin@monprojet.com'],)
        return redirect('email-sent')
    else:
        form = ContactUsForm()
    return render(request, "monapp/contact.html",{'titreh1':titreh1, 'form':form})

def EmailSent(request) :
    titreh1 = " Email correctement envoyé "
    return render(request,"monapp/emailSent.html",{'titreh1':titreh1})


class ConnectView(LoginView):
    template_name = 'monapp/login.html'
    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'monapp/home.html',{'titreh1':"hello "+username+", you're connected"})
        else:
            return render(request, 'monapp/register.html')
        


class RegisterView(TemplateView):
    template_name = 'monapp/register.html'
    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        mail = request.POST.get('mail', False)
        password = request.POST.get('password', False)
        user = User.objects.create_user(username, mail, password)
        user.save()
        if user is not None and user.is_active:
            return render(request, 'monapp/login.html')
        else:
            return render(request, 'monapp/register.html')
        
class DisconnectView(TemplateView):
    template_name = 'monapp/logout.html'
    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name)
    


# def ProductCreate(request):
#         if request.method == 'POST':
#             form = ProductForm(request.POST)
#             if form.is_valid():
#                 product = form.save()
#                 return redirect('product-detail', product.id)
#         else:
#             form = ProductForm()
#         return render(request, "monapp/new_product.html", {'form': form})

class ProductCreateView(CreateView):
    model = Product
    form_class=ProductForm
    template_name = "monapp/new_product.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('product-detail', product.id)
    

class ProductUpdateView(UpdateView):
    model = Product
    form_class=ProductForm
    template_name = "monapp/update_product.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('product-detail', product.id)
    

class ProductDeleteView(DeleteView):
    model = Product
    template_name = "monapp/delete-product.html"
    success_url = reverse_lazy('product-list')


def band_delete(request, id):
    prdct = Product.objects.get(id=id) # nécessaire pour GET et pour POST
    if request.method == 'POST':
    # supprimer le produit de la base de données
        prdct.delete()
        # rediriger vers la liste des produit
        return redirect('product-list')
    # pas besoin de « else » ici. Si c'est une demande GET, continuez simplement
    return render(request, 'monapp/prodcut-delete.html', {'object': prdct})

# def ProductUpdate(request, id):
#     prdct = Product.objects.get(id=id)
#     if request.method == 'POST':
#         form = ProductForm(request.POST, instance=prdct)
#         if form.is_valid():
#             # mettre à jour le produit existant dans la base de données
#             form.save()
#             # rediriger vers la page détaillée du produit que nous venons de mettre à jour
#             return redirect('product-detail', prdct.id)
#     else:
#         form = ProductForm(instance=prdct)
#     return render(request,'monapp/product-update.html', {'form': form})


class ProductItemListView(ListView):

    model = ProductItem
    template_name = "monapp/list_productsItem.html"
    context_object_name = "products"

    def get_queryset(self ) :
        return ProductItem.objects.order_by("color")
    
    def get_context_data(self, **kwargs):
        context = super(ProductItemListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des items produits"
        return context


class ProductItemDetailView(DetailView):
    model = ProductItem
    template_name = "monapp/detail_productItem.html"
    context_object_name = "product"
    def get_context_data(self, **kwargs):
        context = super(ProductItemDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail produit item"
        return context

class ProductItemCreateView(CreateView):
    model = ProductItem
    form_class= ProductItemForm
    template_name = "monapp/new_productItem.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('productItem-detail', product.id)
    

class ProductItemUpdateView(UpdateView):
    model = ProductItem
    form_class=ProductItemForm
    template_name = "monapp/update_productItem.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('productItem-detail', product.id)
    

class ProductItemDeleteView(DeleteView):
    model = ProductItem
    template_name = "monapp/delete-productItem.html"
    success_url = reverse_lazy('productItem-list')


def band_delete(request, id):
    prdct = ProductItem.objects.get(id=id) # nécessaire pour GET et pour POST
    if request.method == 'POST':
    # supprimer le produit de la base de données
        prdct.delete()
        # rediriger vers la liste des produit
        return redirect('productItem-list')
    # pas besoin de « else » ici. Si c'est une demande GET, continuez simplement
    return render(request, 'monapp/prodcutItem-delete.html', {'object': prdct})








class ProductAttributeListView(ListView):
    model = ProductAttribute
    template_name = "monapp/list_productsAttribute.html"
    context_object_name = "product"
    def get_queryset(self ):
        return ProductAttribute.objects.all()
    def get_context_data(self, **kwargs):
        context = super(ProductAttributeListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des attributs"
        return context


class ProductAttributeDetailView(DetailView):
    model = ProductAttribute
    template_name = "monapp/detail_productAttribute.html"
    context_object_name = "product"
    def get_context_data(self, **kwargs):
        context = super(ProductAttributeDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail attribut"
        context['values']= ProductAttributeValue.objects.filter(product_attribute=self.object).order_by('position')
        return context

class ProductAttributeCreateView(CreateView):
    model = ProductAttribute
    form_class= ProductAttributeForm
    template_name = "monapp/new_productAttribute.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('productAttribute-detail', product.id)
    

class ProductAttributeUpdateView(UpdateView):
    model = ProductAttribute
    form_class=ProductAttributeForm
    template_name = "monapp/update_productAttribute.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('productAttribute-detail', product.id)
    

class ProductAttributeDeleteView(DeleteView):
    model = ProductAttribute
    template_name = "monapp/delete-productAttribute.html"
    success_url = reverse_lazy('productAttribute-list')


def band_delete(request, id):
    prdct = ProductAttribute.objects.get(id=id) # nécessaire pour GET et pour POST
    if request.method == 'POST':
    # supprimer le produit de la base de données
        prdct.delete()
        # rediriger vers la liste des produit
        return redirect('productAttribute-list')
    # pas besoin de « else » ici. Si c'est une demande GET, continuez simplement
    return render(request, 'monapp/prodcutAttribute-delete.html', {'object': prdct})



class FournisseurCreateView(CreateView):
    model = Fournisseur
    form_class= FournisseurForm
    template_name = "monapp/new_fournisseur.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('fournisseur-detail', product.id)
    

class FournisseurDetailView(DetailView):
    model = Fournisseur
    template_name = "monapp/detail_fournisseur.html"
    context_object_name = "fournisseur"
    def get_context_data(self, **kwargs):
        context = super(FournisseurDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail Fournisseur"
        return context
    

class FournisseurListView(ListView):
    model = Fournisseur
    template_name = "monapp/list_fournisseur.html"
    context_object_name = "fournisseur"
    def get_queryset(self ):
        return Fournisseur.objects.all()
    def get_context_data(self, **kwargs):
        context = super(FournisseurListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des Fournisseurs"
        return context
    

class FournisseurUpdateView(UpdateView):
    model = Fournisseur
    form_class=FournisseurForm
    template_name = "monapp/update_fournisseur.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('fournisseur-detail', product.id)
    

class FournisseurDeleteView(DeleteView):
    model = Fournisseur
    template_name = "monapp/delete_fournisseur.html"
    success_url = reverse_lazy('fournisseur-list')