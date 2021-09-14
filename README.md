# ECommerce-API [![ECommerce-API](https://github.com/AinaEmmanuel/ECommerce-API/actions/workflows/django.yml/badge.svg)](https://github.com/AinaEmmanuel/ECommerce-API/actions/workflows/django.yml)
Djano REST E-Commerce API with stripe payment integration
#### Functionalities
 - Product
 - Category
 - Cart
 - Discount
 - Authentication Sign up / sign in. JWT
 - Swagger DOCs
 - Stripe Payment

## Installation
##### Cloning & Virtual Environment
```
$ git clone https://github.com/AinaEmmanuel/ECommerce-API.git
$cd Ecommerce-APi
$ virtualenv myenv
$ source myenv/bin/activate
```

##### Setup .env
```
copy all variables from env_example.txt to .env and fill appropriately
```
## Devlopment Setup
```
$ docker-compose build
```

```
$ docker-compose exec app python manage.py migrate
```

```
$ docker-compose up
```
