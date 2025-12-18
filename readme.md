# Конвертер конфигурационного языка (Вариант 4)

## Описание
Инструмент командной строки для преобразования текста из учебного конфигурационного языка в XML. Использует библиотеку Lark для синтаксического разбора.

## Особенности языка (Вариант 4)
- Числа в научной нотации: `1.5e2`, `-3.14e-10`
- Массивы без запятых: `[значение значение значение]`
- Константы: `var имя значение`
- Выражения: `${имя 1 +}` (постфиксная форма)
- Функции: `pow()`, `max()`, `+`

## Установка
```bash
pip install -r requirements.txt
```

## Использование
```bash
python converter-v4.py входной_файл.conf -o выходной_файл.xml
```

### Примеры
```bash
python converter-v4.py example1-physics.conf -o physics.xml
python converter-v4.py example2-finance.conf -o finance.xml
python converter-v4.py example3-game.conf -o game.xml
```

### Тестовый файл
```bash
python converter-v4.py test_expr.conf -o test.xml
```

## Запуск тестов
```bash
python test_converter-v4.py
```

## Пример входного файла
```conf
var a 10
var b 20
sum: ${a b +}
numbers: [1 2 3]
```

## Пример выходного файла (XML)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<config>
  <sum>30</sum>
  <numbers>
    <item>1</item>
    <item>2</item>
    <item>3</item>
  </numbers>
</config>
```

## Файлы проекта
- `converter-v4.py` - основной скрипт
- `test_converter-v4.py` - тесты
- `requirements.txt` - зависимости
- `example1-physics.conf` - пример: физический эксперимент
- `example2-finance.conf` - пример: финансовая модель
- `example3-game.conf` - пример: игровой движок
- `test_expr.conf` - тестовый файл с выражениями

## Требования
- Python 3.6+
- Библиотека Lark (`pip install lark`)
