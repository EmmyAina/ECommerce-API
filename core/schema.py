from Product.schema import Query as product_query
from Category.schema import Query as category_query
import graphene


class Query(product_query, category_query):
	pass

schema = graphene.Schema(query=Query)
