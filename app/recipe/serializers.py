from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields=('id', 'name')
        read_only_fields = (id,)
        

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = (id,)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset= Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset= Tag.objects.all()
    )
    class Meta:
        model = Recipe
        fields = ('id', 'title', 'time_minute', 'price', 'link', 'ingredients', 'tags')
        read_only_fields = (id,)


class RecipeDetailSerielizer(RecipeSerializer):
    """serializer for recipe detail"""
    ingredients = IngredientSerializer(many=True, read_only=True)
    tag = TagSerializer(many=True, read_only=True)


class RecipeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'image')
        read_only_fields = ('id',)
        