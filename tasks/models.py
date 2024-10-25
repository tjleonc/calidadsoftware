from django.db import models
from django.contrib.auth.models import User



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
    
class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Carrito de {self.usuario.username}'
    
    @property # Propiedad que calcula el total del carrito
    def total(self):
        return sum(item.subtotal for item in self.items.all())

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'{self.item.name} x {self.cantidad}'
    
    @property
    def subtotal(self):
        return self.item.price * self.cantidad

# Modelo para la orden de compra
class Orden(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through='OrdenItem')
    fecha = models.DateTimeField(auto_now_add=True)
    pagado = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Orden de {self.usuario.username} - {self.fecha.strftime("%Y-%m-%d")}'
    
# Relación entre orden y item
class OrdenItem(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.cantidad} de {self.item.name} en {self.orden}'

