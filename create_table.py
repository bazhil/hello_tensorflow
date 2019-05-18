# import xlrd
# import xlwt
# import openpyxl
import xlsxwriter

# Создаем рабочую книгу и добавляем рабочую таблицу
workbook = xlsxwriter.Workbook('Employee_plans.xlsx')
worksheet = workbook.add_worksheet()

# Данные, которые нужно положить в таблицу
employee_data = (
    ['Название проекта', 'Руководитель', 'Дата сдачи план.', 'Дата сдачи факт.', 'Bart Simpson план.', 'Bart Simpson факт.',
     'Lisa Simpson план.', 'Lisa Simpson факт.', 'Gomer Simpson план.', 'Gomer Simpson факт.'],
    ['Проект1', 'Bart Simpson', '01.10.2018', '30.09.2018', '1', '3', '', '1', '2', '2'],
    ['Проект2', 'Lisa Simpson', '15.10.2018', '16.10.2018', '1', '1', '10', '9', '0', '2'],
    ['Проект3', 'Gomer Simpson', '15.01.2017', '16.10.2018', '1', '1', '10', '0', '0', '7']
)

# Добавляем форматирофание текста - стиль жирный
bold = workbook.add_format({'bold': True})

# Добавляем форматирование - формат дата
date = workbook.add_format({'num_format': 'DD.MM.YYYY'})

# Начало таблицы с отступом в одну ячейку и одну строку
row = 1
col = 1

# Итерируемся по данным employee_data и записываем их в таблицу ряд за рядом
for project_name, manager, date_plan, date_fact, emp1_plan, emp1_fact, emp2_plan, \
    emp2_fact, emp3_plan, emp3_fact in employee_data:
    worksheet.write(row, col, project_name)
    worksheet.write(row, col + 1, manager)
    worksheet.write(row, col + 2, date_plan, date)
    worksheet.write(row, col + 3, date_fact, date)
    worksheet.write(row, col + 4, emp1_plan, date)
    worksheet.write(row, col + 5, emp1_fact, date)
    worksheet.write(row, col + 6, emp2_plan, date)
    worksheet.write(row, col + 7, emp2_fact, date)
    worksheet.write(row, col + 8, emp3_plan, date)
    worksheet.write(row, col + 9, emp3_fact, date)
    row += 1

# закрываем рабочую книгу
workbook.close()

