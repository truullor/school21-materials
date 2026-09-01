# DSB5 — Фишки, советы и интересные факты

## Интересные факты

### 1. List comprehension и CPython
CPython (стандартная реализация Python) оптимизирует list comprehension на C-уровне. Внутри генератор создаёт специальный bytecode, который работает быстрее обычного цикла + append. Это не просто синтаксический сахар — это **реальное ускорение**.

### 2. map может быть быстрее list comprehension
Когда ты передаёшь **готовую функцию** (не lambda), `map` иногда быстрее list comprehension:
```python
# Быстрее с map
list(map(str, range(10000)))

# Медленнее с list comprehension
[str(x) for x in range(10000)]
```
Потому что `map` вызывает C-функцию `str` напрямую, а list comprehension создаёт额外ный frame для каждой итерации.

### 3. filter(None, ...) — трюк с пустыми значениями
`filter(None, iterable)` убирает все "пустые" значения: `0`, `False`, `None`, `""`, `[]`, `()`, `{}`.
```python
list(filter(None, [0, 1, False, True, "", "hello", None]))
# → [1, True, "hello"]
```

### 4. Counter хранит данные на C-уровне
`collections.Counter` написан на C в CPython, поэтому он быстрее любого самописного подсчёта через dict. Разница может быть 10x.

### 5. Генератор = ленивые вычисления
Генератор НЕ вычисляет значения заранее. Он вычисляет их **только когда ты просишь**:
```python
def gen():
    print("Computing 1")
    yield 1
    print("Computing 2")
    yield 2

g = gen()
print("Before next")
next(g)  # → "Computing 1" → 1
# "Before next" напечатался ПЕРВЫМ!
```

### 6. Генераторное выражение vs list comprehension по памяти
```python
import sys
import dis

# List comprehension
lst = [x**2 for x in range(1000000)]
sys.getsizeof(lst)  # 8,448,728 байт (~8 MB)

# Generator expression
gen = (x**2 for x in range(1000000))
sys.getsizeof(gen)  # 208 байт
```
Разница в **40,000 раз**!

### 7. timeit запускает код million раз
По умолчанию `timeit` запускает код **1,000,000 раз** и выбирает лучшее время из 3 попыток. Это нужно для точности — одна итерация может быть неточной из-за шума ОС.

### 8. Python vs C: почему циклы медленные
Каждая итерация `for` в Python — это:
- Проверка условия
- Вызов `__next__()` итератора
- Присваивание переменной
- Вызов `__contains__()` для `if`
- Вызов `append()` для списка

В C-реализации list comprehension всё это — один bytecode `LIST_APPEND`, без额外ных вызовов методов.

---

## Советы для бенчмарков

### 1. Не используй time.time() для бенчмарков
```python
# ПЛОХО — не точное
import time
start = time.time()
# ... код ...
end = time.time()
print(end - start)

# ХОРОШО — точное
import timeit
print(timeit.timeit(код, number=10000))
```

`time.time()` зависит от системных часов, может прыгать. `timeit` использует `time.perf_counter()` (высокоточный таймер) и запускает много раз для точности.

### 2. Запускай функцию, а не строку
```python
# Медленнее (парсинг строки каждый раз)
timeit.timeit('[x**2 for x in range(100)]', number=10000)

# Быстрее (функция уже скомпилирована)
def comp():
    return [x**2 for x in range(100)]
timeit.timeit(comp, number=10000)
```

### 3. Не мери время одного запуска
```python
# ПЛОХО
result = my_function()  # один замер — неточно

# ХОРОШО
time = timeit.timeit(my_function, number=100000)
```

### 4. Сортируй результаты
```python
times = sorted([loop_time, lc_time, map_time])
print(f"{times[0]} vs {times[1]} vs {times[2]}")
```

---

## Фишки для скриптов DSB5

### 1. sys.argv проверка
```python
import sys

if len(sys.argv) < 3:
    print("Usage: ./benchmark.py <function_name> <number>")
    sys.exit(1)

func_name = sys.argv[1]
number = int(sys.argv[2])
```

### 2. Словарь функций вместо if/elif
```python
def loop(): ...
def listcomp(): ...
def map_func(): ...

functions = {
    "loop": loop,
    "list_comprehension": listcomp,
    "map": map_func,
}

if func_name in functions:
    result = timeit.timeit(functions[func_name], number=number)
```

### 3. Память в гигабайтах
```python
import resource
usage = resource.getrusage(resource.RUSAGE_SELF)
peak_gb = usage.ru_maxrss / (1024 * 1024)  # KB → MB → GB
```

### 4. CPU время
```python
import resource
usage = resource.getrusage(resource.RUSAGE_SELF)
cpu_time = usage.ru_utime + usage.ru_stime  # user + system
```

### 5. Вывод в формате README
```python
print(f"Peak Memory Usage = {peak_gb:.3f} GB")
print(f"User Mode Time + System Mode Time = {cpu_time:.2f}s")
```

---

## Типичные ошибки

### 1. Забыл `list()` для map/filter
```python
# ОШИБКА — возвращает объект map, не список
result = map(str, [1, 2, 3])
print(result)  # <map object at 0x...>

# ПРАВИЛЬНО
result = list(map(str, [1, 2, 3]))
```

### 2. Забыл `from functools import reduce`
```python
# ОШИБКА — reduce не встроенная функция
result = reduce(lambda a, b: a + b, [1, 2, 3])

# ПРАВИЛЬНО
from functools import reduce
result = reduce(lambda a, b: a + b, [1, 2, 3])
```

### 3. lambda в map/filter замедляет
```python
# МЕДЛЕННО
list(map(lambda x: x**2, range(1000)))

# БЫСТРЕЕ (готовая функция)
list(map(pow, range(1000), [2]*1000))
# или просто
[x**2 for x in range(1000)]
```

### 4. reduce без начального значения
```python
# ОШИБКА — пустой iterable без начального значения
reduce(lambda a, b: a + b, [])

# ПРАВИЛЬНО
reduce(lambda a, b: a + b, [], 0)
```

### 5. Генератор — один раз
```python
# Генератор можно пройти ТОЛЬКО ОДИН раз
gen = (x**2 for x in range(10))
list(gen)  # [0, 1, 4, ...]
list(gen)  # [] — пустой! Генератор исчерпан

# Решение — пересоздать
gen = (x**2 for x in range(10))
```

---

## Сравнение скорости (ориентир)

| Метод | Относительная скорость |
|---|---|
| map + готовая функция | 1x (быстрее всего) |
| List comprehension | 1.1x |
| filter + lambda | 1.3x |
| Цикл + append | 1.5x |
| reduce + lambda | 1.8x |
| map + lambda | 2x |

Зависит от задачи и данных! Всегда замеряй сам.
