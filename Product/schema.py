from .models import Product
import graphene
from graphene_django import DjangoObjectType, DjangoListField

class ProductType(DjangoObjectType):
	class Meta:
		model = Product
		fields = "__all__"

class Query(graphene.ObjectType):
	all_products = graphene.List(ProductType)
	product = graphene.Field(ProductType,product_id=graphene.Int())

	def resolve_all_products(root, info):
		return Product.objects.all()

	def resolve_product(root, info, product_id):
		return Product.objects.filter(id=product_id).first()
