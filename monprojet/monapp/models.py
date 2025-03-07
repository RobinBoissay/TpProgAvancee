from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
PRODUCT_STATUS = (
    (0, 'Offline'),
    (1, 'Online'),
    (2, 'Out of stock')              
)
COMMANDE_STATUS = (
    (0, "Preaparing"),
    (1, "Done"),
    (2, "Received")
)
# Create your models here.
"""
    Status : numero, libelle
"""
class Status(models.Model):
    numero  = models.IntegerField()
    libelle = models.CharField(max_length=100)
          
    def __str__(self):
        return "{0} {1}".format(self.numero, self.libelle)

"""
Produit : nom, code, etc.
"""
class Product(models.Model):

    class Meta:
        verbose_name = "Produit"

    name          = models.CharField(max_length=100)
    code          = models.CharField(max_length=10, null=True, blank=True, unique=True)
    status        = models.SmallIntegerField(choices=PRODUCT_STATUS, default=0)
    date_creation = models.DateTimeField(blank=True, verbose_name="Date création") 
    stock         = models.IntegerField(default= 0 ,validators=[MinValueValidator(0)])


    def __str__(self):
        return "{0} {1}".format(self.name, self.code)
    

class Fournisseur(models.Model):
    
    class Meta:
        verbose_name = "Fournisseur"
    
    name        = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    

class ProductFournisseur(models.Model):

    class Meta:
        verbose_name = "ProduitFournisseur"

    product       = models.ForeignKey('Product', on_delete=models.CASCADE)
    fournisseur   = models.ForeignKey('Fournisseur', on_delete=models.CASCADE)
    price_ht      = models.DecimalField(max_digits=8, decimal_places=2,  null=True, blank=True, verbose_name="Prix unitaire HT")
    price_ttc     = models.DecimalField(max_digits=8, decimal_places=2,  null=True, blank=True, verbose_name="Prix unitaire TTC")

    def __str__(self):
        return self.product.name + " : " + self.fournisseur.name + " ;Prix ttc = " + str(self.price_ttc) + " ;Prix ht = "+str(self.price_ht)
    
class Commande(models.Model):

    class Meta:
        verbose_name = "Commande"

    commandeName = models.CharField(max_length=100)
    produitFournisseur = models.ForeignKey('ProductFournisseur', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    etatCommande = models.SmallIntegerField(choices=COMMANDE_STATUS, default=0)

    def save(self, *args, **kwargs):
        # Vérification de l'état précédent
        if self.pk:
            # On récupère l'état de la commande avant la modification
            old_etat = Commande.objects.get(pk=self.pk).etatCommande
        else:
            old_etat = None

        super(Commande, self).save(*args, **kwargs)  # On appelle d'abord la méthode save() pour sauvegarder la commande

        # Si l'état de la commande passe au troisième état (disons, etatCommande = 2)
        if old_etat != 2 and self.etatCommande == 2:
            # Incrémenter le stock du produit fournisseur associé

            produit = self.produitFournisseur.product
            self.produitFournisseur.product.stock += self.quantity
            self.produitFournisseur.product.save()
"""
    Déclinaison de produit déterminée par des attributs comme la couleur, etc.
"""
class ProductItem(models.Model):
    
    class Meta:
        verbose_name = "Déclinaison Produit"

    color   = models.CharField(max_length=100)
    code    = models.CharField(max_length=10, null=True, blank=True, unique=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    attributes  = models.ManyToManyField("ProductAttributeValue", related_name="product_item", null=True, blank=True)
       
    def __str__(self):
        return "{0} {1}".format(self.color, self.code)
    
class ProductAttribute(models.Model):
    """
    Attributs produit
    """
    
    class Meta:
        verbose_name = "Attribut"
        
    name =  models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class ProductAttributeValue(models.Model):
    """
    Valeurs des attributs
    """
    
    class Meta:
        verbose_name = "Valeur attribut"
        ordering = ['position']
        
    value              = models.CharField(max_length=100)
    product_attribute  = models.ForeignKey('ProductAttribute', verbose_name="Unité", on_delete=models.CASCADE)
    position           = models.PositiveSmallIntegerField("Position", null=True, blank=True)
     
    def __str__(self):
        return "{0} [{1}]".format(self.value, self.product_attribute)