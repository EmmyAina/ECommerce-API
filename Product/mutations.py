from graphene_django import DjangoObjectType
import graphene

from Category.models import Category
from .models import Product
from .schema import ProductType

class CreateProductMutation(graphene.Mutation):
	class Arguments:
		product_name = graphene.String(required=True)
		product_price_ngn = graphene.Int(required=True)
		available_inventory = graphene.Int(required=True)
		product_description = graphene.String(required=True)
		category = graphene.Int(required=True)

	product = graphene.Field(ProductType)

	@classmethod
	def mutate(cls, root, info, product_name,product_price_ngn,available_inventory, product_description, category):
		category = Category.objects.filter(id=category).first()
		product = Product(product_description=product_description, 
		product_name=product_name, product_price_ngn=product_price_ngn, 
		category=category,  available_inventory=available_inventory)

		product.save()

		return CreateProductMutation(product=product)

class DeleteProductMutation(graphene.Mutation):
	class Arguments:
		id = graphene.Int(required=True)

	product = graphene.Field(ProductType)

	@classmethod
	def mutate(cls,root,info,id):
		product = Product.objects.get(id=id)
		product.delete()

		return
class Mutation(graphene.ObjectType):
	create_product = CreateProductMutation.Field()
	delete_product = DeleteProductMutation.Field()
	pass
