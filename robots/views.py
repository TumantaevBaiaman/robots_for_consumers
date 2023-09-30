from datetime import datetime, timedelta

import openpyxl
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from robots.models import Robot


class GenerateExcelReportView(View):
    def get(self, request):
        # Определите дату начала и конца последней недели
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        # Получаем данные о количестве роботов из базы данных
        robot_models = Robot.objects.filter(created__gte=start_date, created__lte=end_date).values('model').distinct()

        # Проверьте, есть ли данные за последнюю неделю
        if not robot_models:
            error_message = 'Данные за последнюю неделю не найдены.'
            return JsonResponse({'error': error_message}, status=404)

        # Создаем новую книгу Excel
        workbook = openpyxl.Workbook()

        # Создаем страницу (лист) для каждой модели
        for robot_model in robot_models:
            model_name = robot_model['model']
            worksheet = workbook.create_sheet(title=model_name)  # Создаем лист с именем модели
            self.add_headers(worksheet)  # Добавляем заголовки
            robot_data = self.get_robot_summary_data(model_name, start_date, end_date)  # Получаем данные для текущей модели
            self.fill_worksheet(worksheet, robot_data)  # Заполняем лист данными

        # Удаляем лист "Sheet", который создается автоматически, если не удален
        default_sheet = workbook['Sheet']
        workbook.remove(default_sheet)

        # Создаем HTTP-ответ с Excel-файлом для скачивания
        response = self.create_excel_response(workbook)

        return response

    def add_headers(self, worksheet):
        # Добавляем заголовки в первую строку
        worksheet.append(['Модель', 'Версия', 'Количество за неделю'])

    def get_robot_summary_data(self, model_name, start_date, end_date):
        # Получаем суммарные показатели количества роботов для данной модели
        return Robot.objects.filter(model=model_name, created__gte=start_date, created__lte=end_date).values('model', 'version').annotate(count=Count('serial'))

    def fill_worksheet(self, worksheet, data):
        # Заполняем лист данными из базы данных
        for item in data:
            model = item['model']
            version = item['version']
            count = item['count']
            worksheet.append([model, version, count])

    def create_excel_response(self, workbook):
        # Создаем HTTP-ответ с Excel-файлом для скачивания
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=robot_production_summary.xlsx'
        workbook.save(response)
        return response