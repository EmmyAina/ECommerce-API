def get_actual_total(user_cart):
	item_total = []
	for item in user_cart:
		item_total.append(
			item.product_total()
		)
	sub_total = sum(item_total)

	return sub_total

def get_discount_total(discount_percent, sub_total):
	discount_value = (discount_percent/100) * sub_total

	discount_total = sub_total - discount_value
	return discount_total
