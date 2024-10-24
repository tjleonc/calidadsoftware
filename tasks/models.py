from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Item(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='productos/', null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Estrellas de 1 a 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reseña de {self.author} para {self.item}'
    
class CarroCompra(models.Model):
    codigo = models.AutoField(primary_key=True,null=False)
    email = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    producto = models.ForeignKey(Item, on_delete=models.PROTECT, null=False)
    cantidad = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(999)],null=False)  

class Pedido(models.Model):
    nro_pedido= models.AutoField(primary_key=True,null=False)
    total_pedido = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(999999999999)],null=False)
    email=models.ForeignKey(User,on_delete=models.PROTECT)    
    fecha_pedido = models.DateField(null=False)
    direccion_pedido = models.CharField(max_length=500, null=True)

class ProductoCarro(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    codigo_producto = models.ForeignKey(Item,on_delete=models.PROTECT, related_name = 'producto')
    codigo_pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT, related_name='pedido')
    cantidad = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(250)])  

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} bought {self.item.name}'