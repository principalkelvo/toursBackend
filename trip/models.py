from multiselectfield import MultiSelectField
from io import BytesIO #for image resizing
from PIL import Image
from django.core.files import File

from django.db import models



# Create your models here.
class Category(models.Model):
    name= models.CharField(max_length=255)
    slug= models.SlugField()

    class Meta:
        ordering = ('name',) #order by name
        
    def __str__(self): #change to string
            return self.name
        
    def get_absolute_url(self):
            return f'/{self.slug}/'

class Trip(models.Model):
     #creating the choices for status
    HIKING= 'hiking'
    BOAT_RIDING= 'Boat Riding'
    BOARD_GAMES= 'Board Games'
    BONFIRE= 'Bonfire'
    SWIMMING= 'Swimming'

    CHOICES_STATUS=(
        (HIKING,'hiking'),
        (BOAT_RIDING,'Boat Riding'),
        (BOARD_GAMES,'Board Games'),
        (BONFIRE,'Bonfire'),
        (SWIMMING,'Swimming'),
    )



    category = models.ForeignKey(Category, related_name='trips', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    rate= models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank= True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank= True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    activities = MultiSelectField(choices=CHOICES_STATUS)

    class Meta:
        ordering =('-date_added',) #sort by date #added negative to descending order

    def __str__(self): #change to string
            return self.name
        
    def get_absolute_url(self):
            return f'/{self.category.slug}/{self.slug}/'
        
    def get_image(self):
            if self.image:
                return 'https://traveltourskenya.herokuapp.com'+self.image.url
            return ''
        
    def get_thumbnail(self):
            if self.thumbnail:
                return 'https://traveltourskenya.herokuapp.com'+self.thumbnail.url
            else:
                if self.image:
                    self.thumbnail = self.make_thumbnail(self.image)
                    self.save
                    return 'https://traveltourskenya.herokuapp.com'+self.thumbnail.url
                else:
                    return ''
        
    def make_thumbnail(self,image,size= (300,300)):
            img = Image.open(image)
            img.convert('RGB')
            img.thumbnail(size)

            thumb_io = BytesIO()
            img.save(thumb_io,'JPEG', quality=85)
            thumbnail = File(thumb_io, name=image.name)

            return thumbnail