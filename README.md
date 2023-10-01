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

Requirements
- Redis
- Docker + Docker Compose


Having satisfied the above requirements, run ```docker compose up --build```