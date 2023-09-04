# 🛞 Wheel-Deal-Shop

## Running Locally

1. Start app server -> ```python manage.py runserver```
2. Start rabbitmq server -> ```docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672
rabbitmq:management```
3. Start Celery Worker -> ```celery -A config worker -l info```
4. Start Local Stripe server -> ```stripe listen --forward-to localhost:8000/payment/webhook/```
