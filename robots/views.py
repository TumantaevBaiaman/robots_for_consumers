from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .forms import RobotForm
import json

from .models import Robot


class CreateRobotView(View):

    def post(self, request, *args, **kwargs):
        # Распаковываем JSON-данные из запроса
        robot_data = json.loads(request.body)

        # Валидируем данные с использованием формы
        validation_result = self.validate_robot_data(robot_data)

        if not validation_result['is_valid']:
            # Если данные не прошли валидацию, возвращаем ошибки
            return JsonResponse({'error': validation_result['errors']}, status=400)

        # Получаем данные из валидированных данных
        serial = validation_result['serial']
        model = validation_result['model']
        version = validation_result['version']
        created = validation_result['created']

        # Создаем запись о роботе
        self.create_robot(serial, model, version, created)

        # Возвращаем успешный ответ
        return JsonResponse({'message': 'Запись о роботе успешно создана'}, status=201)

    def validate_robot_data(self, robot_data):
        """
        Валидация данных робота с использованием формы.
        """
        robot_form = RobotForm(robot_data)
        if not robot_form.is_valid():
            # Если данные не прошли валидацию, возвращаем ошибки
            return {'is_valid': False, 'errors': robot_form.errors}

        # Если данные прошли валидацию, извлекаем необходимые поля
        serial = robot_form.cleaned_data['model'] + "-" + robot_form.cleaned_data['version']
        model = robot_form.cleaned_data['model']
        version = robot_form.cleaned_data['version']
        created = robot_form.cleaned_data['created']

        return {'is_valid': True, 'serial': serial, 'model': model, 'version': version, 'created': created}

    def create_robot(self, serial, model, version, created):
        """
        Создание записи о роботе в базе данных.
        """
        robot = Robot(serial=serial, model=model, version=version, created=created)
        robot.save()