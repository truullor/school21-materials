# DSB5 — Рациональный подход к написанию кода

Полный справочник по всем темам DSB5. Читай по порядку или ищи нужное.

---

## Общая идея проекта

DSB5 учит писать код, который работает **быстрее и экономит память**. Каждое упражнение — это бенчмарк: ты сравниваешь два способа решения одной задачи и смотришь, какой быстрее. Инструмент — `timeit`.

Ключевой принцип: **не все способы равны**. Цикл,列表 включения, map, filter, reduce — все решают похожую задачу, но с разной скоростью.

---

## Глава 1. List Comprehensions (списковые включения)

### Что это
Списковое включение — это сокращённая запись цикла `for` + `append`. Вместо 4 строк — одна.

### Синтаксис
```python
# Обычный цикл
result = []
for x in emails:
    if "gmail" in x:
        result.append(x)

# Списковое включение
result = [x for x in emails if "gmail" in x]
```

### Формула
```python
[выражение for переменная in итерируемое if условие]
```

### Когда использовать
- Нужно преобразовать список → список
- Нужно отфильтровать элементы
- Логика простая (одно-два условия)

### Когда НЕ использовать
- Сложная логика ( больше 2 `if` ) — цикл читабельнее
- Нужен `break` / `continue` — list comprehension не поддерживает
- Нужен `else` — только `if` (для `else` используй тернарник: `x if условие иначе y`)

### Примеры

```python
# Удвоить каждое число
squares = [x**2 for x in range(10)]

# Чётные числа
evens = [x for x in range(20) if x % 2 == 0]

# Gmail-адреса
gmails = [e for e in emails if "gmail" in e]

# Преобразование строк в числа
numbers = [int(x) for x in ["1", "2", "3"]]

# Вложенный list comprehension (матрица)
matrix = [[i*3 + j + 1 for j in range(3)] for i in range(3)]
# [[1,2,3], [4,5,6], [7,8,9]]

# Тернарник внутри list comprehension
labels = ["чёт" if x % 2 == 0 else "нечёт" for x in range(5)]
# ['чёт', 'нечёт', 'чёт', 'нечёт', 'чёт']
```

### Скорость
List comprehension быстрее цикла с `append` потому что:
- `append` — это поиск метода + вызов (каждый раз)
- List comprehension оптимизирован внутри CPython на C-уровне

---

## Глава 2. Map

### Что это
`map()` применяет функцию к каждому элементу итерируемого объекта. Возвращает **итератор** (не список!).

### Синтаксис
```python
map(функция, итерируемое)
```

### Примеры
```python
# Удвоить числа
numbers = [1, 2, 3]
doubled = map(lambda x: x * 2, numbers)
print(list(doubled))  # [2, 4, 6]

# Строки → числа
str_nums = ["1", "2", "3"]
nums = list(map(int, str_nums))  # [1, 2, 3]

# С��ом лямбдой — Gmail
gmails = list(map(lambda e: e if "gmail" in e else None, emails))
gmails = [e for e in gmails if e]  # убрать None
```

### map vs list comprehension
```python
# map + lambda
list(map(lambda x: x**2, range(10)))

# list comprehension
[x**2 for x in range(10)]
```

**Обычно list comprehension быстрее**, потому что `lambda` — это вызов функции на каждой итерации. Если функция уже определена (`def`), `map` может быть быстрее.

### Важно: map возвращает итератор!
```python
m = map(str, [1, 2, 3])
print(m)      # <map object at 0x...> — не список!
print(list(m))  # ['1', '2', '3']
```

---

## Глава 3. Filter

### Что это
`filter()` отфильтровывает элементы по условию. Функция должна возвращать `True`/`False`.

### Синтаксис
```python
filter(функция, итерируемое)
```

### Примеры
```python
# Чётные числа
evens = list(filter(lambda x: x % 2 == 0, range(20)))

# Gmail
gmails = list(filter(lambda e: "gmail" in e, emails))

# Непустые строки
words = ["hello", "", "world", "  ", "python"]
non_empty = list(filter(None, words))  # ['hello', 'world', 'python']
```

### filter vs list comprehension
```python
# filter
list(filter(lambda x: x > 0, numbers))

# list comprehension
[x for x in numbers if x > 0]
```

**List comprehension обычно быстрее** (нет накладных расходов на вызов lambda). Но `filter` читабельнее для простых случаев.

### Фишка: `filter(None, iterable)` — убирает falsy-значения
```python
list(filter(None, [0, 1, False, True, "", "hello", None]))
# [1, True, "hello"]
```

---

## Глава 4. Reduce

### Что это
`reduce()` последовательно применяет функцию к элементам, сворачивая список в одно значение.

### Синтаксис
```python
from functools import reduce
reduce(функция, итерируемое, начальное_значение)
```

### Как работает
```
reduce(f, [a, b, c, d]) = f(f(f(a, b), c), d)
```

### Примеры
```python
from functools import reduce

# Сумма
reduce(lambda a, b: a + b, [1, 2, 3, 4])  # 10

# Произведение
reduce(lambda a, b: a * b, [1, 2, 3, 4])  # 24

# Максимум
reduce(lambda a, b: a if a > b else b, [3, 1, 4, 1, 5])  # 5

# Сумма квадратов (задание ex03)
reduce(lambda acc, i: acc + i*i, range(1, 6), 0)  # 55

# Склейка строк
reduce(lambda a, b: a + " " + b, ["hello", "world", "!"])  # "hello world !"
```

### reduce vs цикл
```python
# Цикл
total = 0
for i in range(1, 6):
    total += i * i

# Reduce
from functools import reduce
total = reduce(lambda acc, i: acc + i*i, range(1, 6), 0)
```

**Цикл обычно быстрее** для простых сумм, потому что `reduce` + `lambda` — это вызовы функции на каждой итерации. Но `reduce` может быть полезен для сложных свёрток.

### Начальное значение
```python
reduce(lambda a, b: a + b, [1, 2, 3])         # 6
reduce(lambda a, b: a + b, [1, 2, 3], 10)     # 16 (10 + 1 + 2 + 3)
reduce(lambda a, b: a + b, [], 0)              # 0 (без начального — ошибка!)
```

---

## Глава 5. Counter (collections)

### Что это
`Counter` — словарь подсчёта. Считает количество вхождений каждого элемента. Быстрее самописного цикла.

### Синтаксис
```python
from collections import Counter
```

### Примеры
```python
from collections import Counter

# Подсчёт слов
words = ["hello", "world", "hello", "python", "hello"]
c = Counter(words)
print(c)  # Counter({'hello': 3, 'world': 1, 'python': 1})

# Числа
nums = [1, 2, 2, 3, 3, 3]
c = Counter(nums)
print(c[2])  # 2

# Топ-10
top10 = c.most_common(10)

# Обновление
c.update([1, 1, 1])
```

### Counter vs самописный цикл
```python
# Самописный
def count_manual(lst):
    d = {}
    for x in lst:
        d[x] = d.get(x, 0) + 1
    return d

# Counter
def count_counter(lst):
    return Counter(lst)
```

**Counter быстрее** потому что написан на C внутри CPython.

### Интересные методы
```python
c = Counter(a=4, b=2, c=0, d=-2)

c.most_common(2)     # [('a', 4), ('b', 2)]
c.elements()         # итератор: ['a', 'a', 'a', 'a', 'b', 'b']
c.total()            # сумма всех значений: 4
c.subtract({"a": 1}) # вычитание: Counter({'a': 3, 'b': 2, ...})
c + Counter(a=1)     # сложение: Counter({'a': 5, 'b': 2, ...})
```

---

## Глава 6. Генераторы (generators)

### Что это
Генератор — функция с `yield` вместо `return`. Возвращает значения **по одному**, не храня всё в памяти.

### Синтаксис
```python
def my_generator():
    yield 1
    yield 2
    yield 3

gen = my_generator()
print(next(gen))  # 1
print(next(gen))  # 2
print(next(gen))  # 3
# next(gen) → StopIteration
```

### Генераторное выражение
```python
# List comprehension — хранит всё в памяти
squares_list = [x**2 for x in range(1_000_000)]

# Generator expression — хранит только текущий элемент
squares_gen = (x**2 for x in range(1_000_000))

# Разница
import sys
print(sys.getsizeof(squares_list))  # ~8 MB
print(sys.getsizeof(squares_gen))   # ~200 байт!
```

### Зачем нужны
1. **Экономия памяти** — не хранит весь список, генерирует по одному
2. **Ленивые вычисления** — вычисляет только когда нужен следующий элемент
3. **Потоковая обработка** — можно читать файл построчно без загрузки всего файла

### Файловый генератор (ex05)
```python
# Обычный подход — загружает ВЕСЬ файл в память
def read_all(path):
    with open(path) as f:
        return f.readlines()  # список всех строк

# Генератор — читает по одной строке
def read_generator(path):
    with open(path) as f:
        for line in f:
            yield line  # отдаёт одну строку, ждёт
```

### Разница в памяти
```
ordinary.py:  Peak Memory Usage = 2.114 GB
generator.py: Peak Memory Usage = 0.005 GB
```

Файл ratings.csv = 678 MB. `readlines()` загружает его целиком + overhead на список → 2 GB. Генератор хранит только одну строку → 5 MB.

### Потребление времени
Генератор **медленнее** по времени (9 сек vs 5 сек), потому что каждое обращение к `yield` — это приостановка и возобновление функции. Но экономия памяти критична для больших данных.

---

## Глава 7. timeit — замер времени

### Что это
`timeit` — модуль для точного замера времени выполнения кода. Запускает код многократно и усредняет.

### Синтаксис
```python
import timeit

# Одна строка
timeit.timeit('sum(range(100))', number=10000)

# Функция
def my_func():
    return [x**2 for x in range(100)]

timeit.timeit(my_func, number=10000)
```

### Важные параметры
```python
timeit.timeit(
    stmt="код",       # что замерять (строка или callable)
    setup="импорты",  # что выполнить один раз перед замером
    number=1000000    # сколько раз выполнить
)
```

### Пример в контексте DSB5
```python
import timeit

emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
          'anna@live.com', 'philipp@gmail.com'] * 5

# Цикл
def with_loop():
    result = []
    for e in emails:
        if "gmail" in e:
            result.append(e)
    return result

# List comprehension
def with_listcomp():
    return [e for e in emails if "gmail" in e]

# Замер
loop_time = timeit.timeit(with_loop, number=90_000_000)
lc_time = timeit.timeit(with_listcomp, number=90_000_000)

if lc_time <= loop_time:
    print("It is better to use a list comprehension")
else:
    print("It is better to use a loop")
print(f"{lc_time} vs {loop_time}")
```

---

## Глава 8. sys.getsizeof — замер памяти

### Что это
`sys.getsizeof()` возвращает размер объекта в байтах.

### Примеры
```python
import sys

# Список
lst = [1, 2, 3, 4, 5]
sys.getsizeof(lst)          # 104 байта (header списка)

# Словарь
d = {"a": 1, "b": 2}
sys.getsizeof(d)            # 232 байта

# Генератор
g = (x for x in range(1000))
sys.getsizeof(g)            # 200 байт (всегда одинаковый)
```

### Важно: getsizeof НЕ считает вложенные объекты!
```python
lst = [[1, 2], [3, 4], [5, 6]]
sys.getsizeof(lst)           # 88 байт (только список)
sys.getsizeof(lst[0])        # 56 байт (только первый подсписок)
# Общий размер = 88 + 56*3 + размеры чисел
```

Для полного размера нужна рекурсивная функция.

---

## Глава 9. resource (Linux) — замер памяти процесса

### Что это
`resource.getrusage()` — возвращает статистику использования ресурсов процесса (Linux/macOS).

### Пример
```python
import resource

def get_memory_usage():
    """Возвращает память в МБ"""
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return usage.ru_maxrss / 1024  # KB → MB

def get_cpu_time():
    """Возвращает время CPU в секундах"""
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return usage.ru_utime + usage.ru_stime  # user + system time
```

### Вывод в гигабайтах (как в README)
```python
import resource

usage = resource.getrusage(resource.RUSAGE_SELF)
peak_memory_gb = usage.ru_maxrss / (1024 * 1024)  # bytes → GB
cpu_time = usage.ru_utime + usage.ru_stime

print(f"Peak Memory Usage = {peak_memory_gb:.3f} GB")
print(f"User Mode Time + System Mode Time = {cpu_time:.2f}s")
```

---

## Глава 10. Итоговая шпаргалка

| Инструмент | Зачем | Быстрее чем |
|---|---|---|
| List comprehension | Фильтрация/преобразование | Цикл + append |
| map + готовая функция | Преобразование | List comprehension (иногда) |
| filter | Фильтрация | — |
| reduce | Свёртка в одно значение | Цикл (для сумм) |
| Counter | Подсчёт уникальных | Самописный dict |
| Generator | Экономия памяти | readlines() |
| timeit | Замер времени | time.time() (точнее) |

### Приоритет оптимизации
1. **Алгоритм** — O(n²) → O(n) важнее любого трюка
2. **Структуры данных** — set вместо list для поиска
3. **Встроенные функции** — Counter, sorted, sum вместо自己写的
4. **List comprehensions** — вместо циклов + append
5. **Генераторы** — вместо списков при больших данных
