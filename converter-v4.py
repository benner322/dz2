from lark import Lark, Transformer, Visitor
import argparse
import math
import json

# Грамматика для варианта 4
GRAMMAR = r"""
    start: (var_decl | key_value)*

    // Константы
    var_decl: "var" NAME value

    // Пары ключ-значение
    key_value: NAME ":" value

    // Значения
    value: number
         | array
         | const_expr

    // Числа в научной нотации
    number: SCI_NUMBER

    // Массивы
    array: "[" (value)* "]"

    // Константные выражения (постфиксная форма)
    const_expr: "${" expr_items "}"
    expr_items: (NAME | number | OPERATOR | FUNCTION)*

    // Токены
    NAME: /[a-zA-Z][a-zA-Z0-9]*/
    SCI_NUMBER: /[+-]?\d+\.?\d*[eE][+-]?\d+/
    OPERATOR: "+"
    FUNCTION: "pow" | "max"

    // Игнорируем пробелы
    %ignore /\s+/
"""


class MyTransformer(Transformer):
    def start(self, items):
        result = {}
        for item in items:
            if item is not None:
                if isinstance(item, tuple) and len(item) == 2:
                    key, value = item
                    result[key] = value
        return result

    def var_decl(self, items):
        name, value = items
        return ("var", name, value)

    def key_value(self, items):
        key, value = items
        return (key, value)

    def value(self, items):
        return items[0]

    def number(self, items):
        num_str = str(items[0])
        if 'e' in num_str.lower():
            return float(num_str)
        return float(num_str)

    def array(self, items):
        return list(items)

    def const_expr(self, items):
        return ("expr", items[0])

    def expr_items(self, items):
        return list(items)

    def NAME(self, token):
        return str(token)

    def SCI_NUMBER(self, token):
        return str(token)

    def OPERATOR(self, token):
        return str(token)

    def FUNCTION(self, token):
        return str(token)


class Interpreter(Visitor):
    def __init__(self):
        self.variables = {}
        self.result = {}

    def var_decl(self, tree):
        _, name, value = tree.children
        self.variables[str(name)] = self._eval_value(value)

    def key_value(self, tree):
        key, value = tree.children
        self.result[str(key)] = self._eval_value(value)

    def _eval_value(self, value_node):
        value = value_node.children[0] if hasattr(value_node, 'children') else value_node

        if isinstance(value, tuple) and value[0] == 'expr':
            return self._eval_expr(value[1])
        elif isinstance(value, list):
            return [self._eval_item(item) for item in value]
        return value

    def _eval_item(self, item):
        if isinstance(item, tuple) and item[0] == 'expr':
            return self._eval_expr(item[1])
        return item

    def _eval_expr(self, expr_items):
        stack = []

        for item in expr_items:
            if isinstance(item, str):
                # Проверяем, является ли это переменной
                if item in self.variables:
                    stack.append(self.variables[item])
                # Проверяем операторы и функции
                elif item == '+':
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a + b)
                elif item == 'pow':
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(math.pow(a, b))
                elif item == 'max':
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(max(a, b))
                else:
                    # Пробуем преобразовать в число
                    try:
                        stack.append(float(item))
                    except:
                        stack.append(item)

        return stack[0] if stack else None


def parse_config(text):
    parser = Lark(GRAMMAR, parser='lalr')
    tree = parser.parse(text)

    transformer = MyTransformer()
    transformed = transformer.transform(tree)

    interpreter = Interpreter()
    interpreter.visit(tree)

    return interpreter.result


def generate_xml(data, indent=2):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<config>']

    def add_item(key, value, level=1):
        indent_str = ' ' * (level * indent)

        if isinstance(value, list):
            lines.append(f'{indent_str}<{key}>')
            for item in value:
                lines.append(f'{indent_str}  <item>{item}</item>')
            lines.append(f'{indent_str}</{key}>')
        else:
            lines.append(f'{indent_str}<{key}>{value}</{key}>')

    for key, value in data.items():
        add_item(key, value)

    lines.append('</config>')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Конвертер учебного конфигурационного языка в XML')
    parser.add_argument('input', help='Входной файл')
    parser.add_argument('-o', '--output', required=True, help='Выходной XML файл')

    args = parser.parse_args()

    # Чтение входного файла
    with open(args.input, 'r', encoding='utf-8') as f:
        content = f.read()

    # Парсинг конфигурации
    try:
        config_data = parse_config(content)

        # Генерация XML
        xml_content = generate_xml(config_data)

        # Запись в файл
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(xml_content)

        print(f"Конфигурация успешно преобразована в {args.output}")

    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        exit(1)


if __name__ == '__main__':
    main()