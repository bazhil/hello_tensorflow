import xlrd
import datetime
import os

# список проектов
projects = []

def read_xlsx(file):
    """
    Функция, которая читает excel-файл и собирает из него словарь с данными по каждому проекту
    :param file: excel-файл
    :return: список словарей с данными по проектам
    """
    # добавляем рабочую директорию
    work_dir = os.getcwd()

    # определяем рабочую книгу
    workbook = xlrd.open_workbook(file)

    # определяем рабочую таблицу
    worksheet = workbook.sheet_by_index(0)

    # определяем количество рядов и строк
    row_number, col_number = worksheet.nrows, worksheet.ncols

    # иницализируем пустой список, в который будем добавять имена сотрудников, которые есть на листе
    employees = []

    try:
        # наполняем список сотрудников
        for rownum in range(worksheet.nrows):
            row = worksheet.row_values(rownum)
            if rownum == 0:
                for i in range(col_number):
                    if i >= 4 and i % 2 == 0:
                        employees.append(row[i].replace(' план.', ''))

        # читаем файл и наполняем словарь данными
        for rownum in range(worksheet.nrows):
            if rownum > 0:
                row = worksheet.row_values(rownum)
                # инициализируем словарь для наполнения его данными
                project_info = {}
                # Получаем даты
                plan_date_day, plan_date_month, plan_date_year = int(row[2].split('.')[0]), int(row[2].split('.')[1]), int(
                    row[2].split('.')[2])
                real_date_day, real_date_month, real_date_year = int(row[3].split('.')[0]), int(row[3].split('.')[1]), int(
                    row[3].split('.')[2])
                plan_date = datetime.date(plan_date_year, plan_date_month, plan_date_day)
                real_date = datetime.date(real_date_year, real_date_month, real_date_day)

                # наполняем словарь данными
                for i in range(len(row)):
                    project_info['НазваниеПроекта'] = row[0]
                    project_info['СданВСрок'] = plan_date >= real_date
                    project_info['Руководитель'] = row[1]
                    project_info['ДатаСдачиПлан'] = row[2]
                    project_info['ДатаСдачиФакт'] = row[3]
                    project_info['Сотрудники'] = {}

                    # создаем итератор из фрагмента данных ряда
                    days = iter(row[4:])

                    # наполняем словарь данными сотрудников и создаем словарь с полями для данных о затрченными ими временем
                    # и заполняем их при помощи итератора
                    for employee in employees:
                        project_info['Сотрудники'][employee] = {}
                        project_info['Сотрудники'][employee]['КоличествоДнейПоПлану'] = str(days.__next__())
                        project_info['Сотрудники'][employee]['ЗатраченоДнейРеально'] = str(days.__next__())

                # добавляем наполненные словари в список проектов
                projects.append(project_info)
        return projects
    except:
        print('В работе функции \'read_xlsx()\' произошла ошибка. Возможно файл {} заполнен некорректно.'.format(file))

def sort_projects(projects):
    """
    Функция, которая сортирует массив projects по значению элемента 'СданВСрок'.
    :param projects: список со словарями с данными по проектам
    :return: упорядоченный список со словарями с данными по проектам
    """
    try:
        for project in projects:
            # перемещаем успешно сданные проекты в начало массива
            if project['СданВСрок'] == True:
                projects.insert(0, projects.pop(projects.index(project)))
        return projects
    except:
        print('В работе функции \'sort_projects()\' произошла ошибка')

def print_projects(projects):
    """
    Функция, которая анализирует успешность сотрудников и выводит информацию по проекту в понятном виде.
    :param projects: массив со словарями с данными по проектам
    :return:
    """
    try:
        for project in projects:
            if project['СданВСрок'] == True:
                print('Проект {} сдан в срок. Руководитель проекта {}. Дата сдачи - {}, дата сдачи по плану - {}. '.format(
                    project['НазваниеПроекта'], project['Руководитель'], project['ДатаСдачиФакт'], project['ДатаСдачиПлан']))
                for employee in project['Сотрудники']:
                    real_day_cost = project['Сотрудники'][employee]['ЗатраченоДнейРеально']
                    plan_day_cost = project['Сотрудники'][employee]['КоличествоДнейПоПлану']
                    if real_day_cost == '' or plan_day_cost == '':
                        print('Сотрудник {} - условно успешен (необходимо уточнить какое время он затратил на проект). '
                          'Затратил дней - {}. Количество дней по плану - {}.'.format(
                        employee, real_day_cost or 'не указано', plan_day_cost or 'не указано'))
                    elif real_day_cost != '0' and plan_day_cost == '0':
                        print('Сотрудник {} работал над проектом не смотря на отсутствие его в плане. Считается успешным,'
                              ' при условии, что его план выполнен. Затратил дней - {}. Количество дней по плану - {}.'.format(
                        employee, real_day_cost or 'не указано', plan_day_cost))
                    elif real_day_cost <= plan_day_cost:
                        print('Сотрудник {} - успешен. Затратил дней - {}. Количество дней по плану - {}.'.format(
                            employee, real_day_cost, plan_day_cost))
                    else:
                        print('Сотрудник {} - не успешен. Затратил дней - {}. Количество дней по плану - {}.'.format(
                            employee, real_day_cost, plan_day_cost))
            else:
                print('Проект {} не сдан в срок. Сотрудники его выполнявшие условно не успешны. Руководитель проекта {}. Дата сдачи - {}, дата сдачи по плану - {}. '.format(
                    project['НазваниеПроекта'], project['Руководитель'], project['ДатаСдачиФакт'], project['ДатаСдачиПлан']))
            print('\n')
    except:
        print('В работе функции \'print_projects()\' произошла ошибка')



if __name__ == '__main__':
    # добавляем рабочую директорию
    work_dir = os.getcwd()
    # анализируем файлы в директории
    for file in os.listdir(work_dir):
        if file.endswith('.xlsx'):
            try:
                read_xlsx(file)
            except:
                print('Возможно в файле {} что-то не так'.format(file))
    sort_projects(projects)
    print_projects(projects)
