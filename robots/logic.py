
from django.core.mail import send_mail


# Создайте функцию для отправки письма
from customers.models import Customer
from orders.models import Order


def send_notification_email(robot):
    subject = "Робот в наличии"
    message = f"Добрый день!\n\nНедавно вы интересовались нашим роботом модели {robot.model}, версии {robot.version}.\nЭтот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами."
    from_email = "your_email@example.com"
    orders = Order.objects.filter(robot_serial=robot.serial)
    recipient_list = [order.customer.email for order in orders]

    send_mail(subject, message, from_email, recipient_list)