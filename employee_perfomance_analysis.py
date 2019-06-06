import xlrd
import datetime
import os

file = 'Employee_plans.xlsx'

def three_emp_analysis(file):
    """
    Первая версия функции. Анализ файлов excel с тремя работниками.
    :param file:
    :return:
    """
    # Подключаем рабочую книгу, открываем таблицу на первом листе     
    workbook = xlrd.open_workbook(file)
    worksheet = workbook.sheet_by_index(0)
    # Определяем количество строк и столбцов     
    row_number, col_number = worksheet.nrows, worksheet.ncols

    # Определяем количество сотрудников по числу столбцов
    employees_amount = int((col_number - 4) / 2)

    # список сотрудников, которые есть на листе
    employees = []

    try:
        # наполняем список сотрудников
        for rownum in range(worksheet.nrows):
            row = worksheet.row_values(rownum)
            if rownum == 0:
                for i in range(col_number):
                    if i >= 4 and i % 2 == 0:
                        employees.append(row[i].replace(' план.', ''))

        # Получаем сообщения для вывода
        good_answer = 'Проект {} сдан в срок, руководитель {}. \n' + 'Сотрудник {} затратил дней - {}. Количество дней по плану - {}. \n' * len(employees)
        bad_answer = 'Проект {} не сдан в срок, руководитель {}. \n' + 'Сотрудник {} затратил дней - {}. Количество дней по плану - {}. \n' * len(employees)

        for rownum in range(worksheet.nrows):
            row = worksheet.row_values(rownum)
            if rownum > 0:
                project_info = []
                for i in range(len(row)):
                    project_info.append(row[i])

                # Получаем даты
                plan_date_day, plan_date_month, plan_date_year = int(project_info[2].split('.')[0]), int(project_info[2].split('.')[1]), int(project_info[2].split('.')[2])
                real_date_day, real_date_month, real_date_year = int(project_info[3].split('.')[0]), int(project_info[3].split('.')[1]), int(project_info[3].split('.')[2])
                plan_date = datetime.date(plan_date_year, plan_date_month, plan_date_day)
                real_date = datetime.date(real_date_year, real_date_month, real_date_day)

                # анализируем данные
                try:
                    if plan_date >= real_date:
                        print(good_answer.format(
                            project_info[0], project_info[1],
                            employees[0], project_info[5] or 'не указано', project_info[4] or 'не указано',
                            employees[1], project_info[7] or 'не указано', project_info[6] or 'не указано',
                            employees[2], project_info[9] or 'не указано', project_info[8] or 'не указано'))

                    elif plan_date < real_date:
                        print(bad_answer.format(
                            project_info[0], project_info[1],
                            employees[0], project_info[5] or 'не указано', project_info[4] or 'не указано',
                            employees[1], project_info[7] or 'не указано', project_info[6] or 'не указано',
                            employees[2], project_info[9] or 'не указано', project_info[8] or 'не указано'))
                except:
                    print('Ряд {} некорректно заполнен'.format(rownum))
    except:
        pass


if __name__ == '__main__':
    # добавляем рабочую директорию
    work_dir = os.getcwd()

    # анализируем файлы в директории
    for file in os.listdir(work_dir):
        if file.endswith('.xlsx'):
            try:
                print(file)
                three_emp_analysis(file)
            except:
                print('Возможно в файле более 3-х сотрудников')
