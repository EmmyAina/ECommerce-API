import graphene
from graphene_django import DjangoObjectType
from .models import Category
from .schema import CategoryType


class CreateCategoryMutation(graphene.Mutation):
	class Arguments:
		name = graphene.String(required=True)

	category = graphene.Field(CategoryType)
	@classmethod
	def mutate(cls,root,info,name):
		category = Category(category_name=name)
		category.save()

		return CreateCategoryMutation(category=category)

class UpdateCategoryMutation(graphene.Mutation):
	class Arguments:
		name = graphene.String(required=True)
		id = graphene.Int(required=True)
	category = graphene.Field(CategoryType)

	@classmethod
	def mutate(cla, root, info, name,id):
		category = Category.objects.get(id=id)
		category.category_name = name
		category.save()

		return UpdateCategoryMutation(category=category)


class DeleteCategoryMutation(graphene.Mutation):
	class Arguments:
		id = graphene.Int(required=True)
	category = graphene.Field(CategoryType)

	@classmethod
	def mutate(cla, root, info, id):
		category = Category.objects.get(id=id)
		category.delete()

		return

class Mutation(graphene.ObjectType):
	update_category = UpdateCategoryMutation.Field()
	create_category = CreateCategoryMutation.Field()
	delete_category = DeleteCategoryMutation.Field()

