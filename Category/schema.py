from graphene_django import DjangoObjectType
import graphene
from .models import Category

class CategoryType(DjangoObjectType):
	"""
	Retrieve Category Information
	"""
	class Meta:
		model = Category

class Query(graphene.ObjectType):
	"""
	Retrieve Category Information
	"""
	all_categories = graphene.List(CategoryType)
	category = graphene.Field(CategoryType, category_id=graphene.Int())

	def resolve_all_categories(root,info):
		"""
		Get all categories
		"""
		return Category.objects.all()

	def resolve_category(root, info, category_id):
		"""
		Get Category by ID
		"""
		return Category.objects.filter(id=category_id).first()

