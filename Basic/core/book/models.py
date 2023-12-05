from django.db import models
from django.contrib.auth.models import User

# models translate how our data going to look from python code to whatever DB understands
class Color(models.Model):
    color_name = models.CharField(max_length=100);
    
    def __str__(self):
        return self.color_name;

class Book(models.Model):
    title = models.CharField(max_length=200);
    pages = models.IntegerField();
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)
    published_date = models.DateField();
    quantity = models.IntegerField();
    color = models.ForeignKey(Color, null=True, blank=True, on_delete=models.CASCADE, related_name='color')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    
    """
    # related_name='books'
    # now you can access all books related to specific user
    # user = User.objects.get(username="username")
    # user.books.all()
    """
    
    def __str__(self):
        return self.title;
    
    def discount(self):
        return float(10/100);  # in %

    @property
    def sale_price(self):
        return float("%.2f" %(float(self.price)*self.discount()))