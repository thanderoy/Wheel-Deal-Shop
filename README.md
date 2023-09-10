# 🛞 Wheel-Deal-Shop

> Wheel Deal Shop specializes in selling high-quality wheels and rims, offering a diverse selection to enhance your vehicle's performance and style. Explore our range for the perfect fit.

This is a fully featured online shop. Features implemented are listed below.

## Features

- Functional Models with Function-Based Views and Intuitive Forms.
- Session based Cart functionality.
- Asynchronouus tasks implemented using Celery and RabbitMQ for emailing customers.
- Online payemnt integration with Stripe APIs and webhooks.
- Dynamic invoice/receipt generation.
- Coupon/Discount system integrated with Stripe.
- Products recommendations engine implemented using Redis based on previous purchases.

## Future Enhancements.

- Better user interface. I do backend but would be nice to dabble on FrontEnd.


## Running Locally

1. Start app server -> ```python manage.py runserver```
2. Start rabbitmq server -> ```docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672
rabbitmq:management```
3. Start Celery Worker -> ```celery -A config worker -l info```
4. Start Local Stripe server -> ```stripe listen --forward-to localhost:8000/payment/webhook/```
