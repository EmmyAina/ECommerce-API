from Product.schema import Query as product_query
from Category.schema import Query as category_query

from Category.mutations import Mutation as category_mutation
from Product.mutations import Mutation as product_mutation
import graphene


class Query(product_query, category_query):
	pass


class Mutation(category_mutation, product_mutation):
	pass

schema = graphene.Schema(query=Query, mutation=Mutation)
