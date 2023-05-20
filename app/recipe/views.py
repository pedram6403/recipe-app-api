from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Tag , Ingredient, Recipe
from recipe import serializers


class BaseReciprAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """base class viewsetfor user own recipe attrebute"""
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """return objects related to user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
    
    def perform_create(self, serializer):
        """save object"""
        serializer.save(user=self.request.user)

class TagViewSet(BaseReciprAttrViewSet):
    """Manage tags in the database"""

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    
class IngredientViewSet(BaseReciprAttrViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeVeiwSet(viewsets.ModelViewSet):
    """manage recipe end point"""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """return objects related to user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """reuen aproperiat serializer clsaa"""
        if self.action == 'retrive':
            return serializers.RecipeDetailSerielizer
        
        return self.serializer_class
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
