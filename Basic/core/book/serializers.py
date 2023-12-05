from rest_framework import serializers
from rest_framework.reverse import reverse

from book.models import Book, Color

from django.contrib.auth.models import User

class BookSerializers(serializers.Serializer):
    # this is gonna be defining in json response
    id = serializers.IntegerField(read_only=True);
    title = serializers.CharField(max_length=200);
    pages = serializers.IntegerField();
    quantity = serializers.IntegerField();
    published_date = serializers.DateField();
    
    def validate(self, data):
        special_characters = "!@#$%^&*()-+?_=,<>/."
        if data['title'] and any(v in special_characters for v in data['title']):
            raise serializers.ValidationError('No special characters allowed');
        
        if data['quantity'] and data['quantity'] < 0:
            raise serializers.ValidationError('No negative quantity value allowed');
        
        return data;
    
    # create method in order to create book in our DB
    # when we pass only data it passes through below funtion
    def create(self, validated_data):
        return Book.objects.create(**validated_data);
    
    # when we pass instance and data, it passes through below function
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title);
        instance.pages = validated_data.get('pages', instance.pages);
        instance.quantity = validated_data.get('quantity', instance.quantity);
        instance.published_date = validated_data.get('published_date', instance.published_date);
        instance.save();
        return instance;

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name'] # interseted in this fields not in id

class AuthorModelSerializer(serializers.ModelSerializer):
    # return string representation of current user's posts
    # posts = serializers.StringRelatedField(many=True)
    books = serializers.HyperlinkedRelatedField(many=True, view_name="book_detail", queryset=User.objects.all())
    
    class Meta:
        model = User
        fields = ['username', 'email', 'books']

class BookModelSerializers(serializers.ModelSerializer):
    color = ColorSerializer()
    author = AuthorModelSerializer()
    discount = serializers.SerializerMethodField()
    sale_price = serializers.SerializerMethodField()
    edit_url = serializers.SerializerMethodField();
    
    '''
        * to show only speicific field create another serializer and specify in it (color = ColorSerializer())
        [
            {
                "id": 1,
                "name": "John",
                "age": 69,
                "color": {
                    "color_name": "BLUE"
                },
            }
        ]
    '''
    
    color_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = '__all__'
        # depth = 1 # use when you have applied relationships and need actual data instead of id
        '''
            * without depth
            {
                "id": 1,
                "name": "John",
                "age": 69,
                "color": 2
            },
            
            * with depth
            {
                "id": 1,
                "name": "John",
                "age": 69,
                "color": {
                    "id": 2,
                    "color_name": "BLUE"
                }
            },
        '''
    
    # whenever you use SerializerMethodField, you need to add get_ prefix
    # whenever you make get request, data will be attached
    def get_color_info(self, obj):
        color_obj = Color.objects.get(id=obj.color.id);
        return { 'color_info': color_obj.color_name, 'hex': '#0000FF' }
        '''
        [
            {
                "id": 1,
                "name": "John",
                "age": 69,
                "color": {
                    "color_name": "BLUE"
                },
                "color_info": {
                    "color_name": "BLUE",
                    "hex": "#0x00"
                },
            },
            ...
        ]
        '''
    
    def get_discount(self, instance):
        if not hasattr(instance, 'id'):
            return None
        if not isinstance(instance, Book):
            return None
        return f"{instance.discount()*100}%"
    
    def get_sale_price(self, instance):
        if not hasattr(instance, 'id'):
            return None
        if not isinstance(instance, Book):
            return None
        return instance.sale_price
    
    def get_edit_url(self, instance):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("book_detail", kwargs={"pk": instance.pk}, request=request)   # (view-name, kwargs, request)
    
    # title validation
    def validate_title(self, title):
        special_characters = "!@#$%^&*()-+?_=,<>/."
        if title and any(v in special_characters for v in title):
            raise serializers.ValidationError('No special characters allowed');
        return title;