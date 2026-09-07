# DSB5 — Ревью и полное объяснение всех заданий

> Для проверки кода и подготовки к защите. Все 6 упражнений: ex00–ex05.

---

## Часть 1. Ревью кода (что проверено и исправлено)

### Соответствие README — итоговая таблица

| Задание | Статус | Что проверено |
|---|---|---|
| ex00 — List Comprehensions | ✅ прошло | файл `benchmark.py`, импорт `timeit`, 25 e-mail, 2 функции, вывод |
| ex01 — Map | ✅ прошло | файл `benchmark.py`, импорт `timeit`, 3 функции, вывод |
| ex02 — Filter | ✅ прошло | файл `benchmark.py`, импорты `timeit`+`sys`, 4 функции, аргументы CLI |
| ex03 — Reduce | ✅ прошло | файл `benchmark.py`, импорты `timeit`+`sys`+`reduce`, 3 аргумента |
| ex04 — Counter | ✅ прошло | файл `benchmark.py`, импорты `timeit`+`random`+`Counter`, 1М элементов |
| ex05 — Генератор | ✅ прошло | файлы `ordinary.py`+`generator.py`, импорты `sys`+`resource` |

### Что исправлено

| Файл | Исправление |
|---|---|
| ex01/benchmark.py | `run_benckmark` → `run_benchmark` (2 места) |
| ex01/benchmark.py | «it is better to use a map» → «It is better to use a map» (регистр как в README) |
| ex02/benchmark.py | добавлен шебанг `#!/usr/bin/env python3` |
| ex04/benchmark.py | добавлен шебанг `#!/usr/bin/env python3` |
| ex05/ordinary.py | добавлен шебанг + `chmod +x` |
| ex05/generator.py | добавлен шебанг + `chmod +x` |
| ex00–ex04 | `chmod +x` для запуска через `./` |

### Результаты запусков

```
ex02: $ ./benchmark.py filter 1000000        → 2.69s
ex03: $ ./benchmark.py loop 1000000          → (мало аргументов — выход, как задумано)
ex04: $ ./benchmark.py
      my function: 1.0222239
      Counter: 0.6481395
      my top: 1.0196757
      Counter's top: 0.6138841
ex05: $ ./generator.py ratings.csv            → Peak Memory Usage = 0.011 GB
      $ ./ordinary.py ratings.csv             → Peak Memory Usage = 2.060 GB
```

**Разница памяти ex05 — 187 раз (2.06 GB против 0.011 GB)** — генератор экономит память.

---

## Часть 2. Общий принцип DSB5

Все задания — это **бенчмарки**: решаешь одну задачу разными инструментами и через `timeit` смотришь, какой быстрее. Идея: Python-разработчик должен знать встроенные инструменты и понимать, когда что использовать.

| Задание | Инструмент | Зачем |
|---|---|---|
| ex00 | list comprehension | преобразование/фильтрация списка |
| ex01 | map | применить функцию к элементам |
| ex02 | filter | отфильтровать по условию |
| ex03 | reduce | свернуть список в одно значение |
| ex04 | Counter | быстрый подсчёт частот + топ |
| ex05 | генератор | экономия памяти на больших данных |

---

## ex00 — List Comprehensions

**Задача:** сравнить цикл + append против спискового включения.

```python
def gmail_loop(emails):
    result = []
    for e in emails:                # идём по каждому элементу
        if "gmail" in e:            # если адрес содержит "gmail"
            result.append(e)        # добавляем в результат
    return result

def gmail_listcomp(emails):
    return [e for e in emails if "gmail" in e]  # та же логика в одну строку
```

**Замер:**
```python
time_loop = timeit.timeit(lambda: gmail_loop(emails), number=90000000)
```
`timeit` запускает функцию 90_000_000 раз и возвращает суммарное время. `lambda:` нужна, чтобы передать аргумент `emails`.

**Вывод** — сравниваем, какая быстрее, печатаем оба времени по возрастанию:
```python
if time_listcomp < time_loop:
    print("it is better to use a list comprehension")
else:
    print("it is better to use a loop")
times = sorted([time_loop, time_listcomp])   # sort: маленькое → большое
print(f"{times[0]} vs {times[1]}")
```

**Почему listcomp быстрее:** CPython компилирует его в один оптимизированный байткод на C-уровне, без вызова `append()` на каждой итерации.

---

## ex01 — Map

**Задача:** добавить третий способ — `map()` — и сравнить с первыми двумя.

```python
def run_map(emails):
    result = list(map(lambda i: i if "gmail" in i else None, emails))
    return [mail for mail in result if mail]
```

Разбор:
- `map(функция, список)` применяет функцию к каждому элементу.
- Лямбда `lambda i: i if "gmail" in i else None` — возвращает email, если он gmail, иначе `None`.
- `list(...)` — превращает результат map (это итератор!) в список.
- `[mail for mail in result if mail]` — отбрасывает `None`.

**Почему такой изврат:** `map` сам по себе *не фильтрует* — он только *преобразует*. Поэтому не-gmail превращаем в `None`, а потом вторым включением выкидываем.

**Вывод:** цепочка if/elif определяет победителя, печатаем 3 времени.

---

## ex02 — Filter

**Задача:** добавить `filter()` и **сменить интерфейс**: скрипт принимает имя функции и число вызовов аргументами.

```python
def gmail_filter():
    return list(filter(lambda e: "gmail" in e, emails))
```

`filter(функция, список)` **сам отбрасывает** элементы, для которых функция вернула ложь. `"gmail" in e` — условие. `list()` забирает результат (filter — итератор). Для фильтрации это чаще всего самый честный инструмент.

```python
functions = {
    "loop": gmail_loop,
    "list_comprehension": gmail_listcomp,
    "map": gmail_map,
    "filter": gmail_filter,
}
```

**Интерфейс через argv:**
```python
if len(sys.argv) < 3:      # слишком мало аргументов → выход
    sys.exit()
func_name = sys.argv[1]    # например "filter"
number = int(sys.argv[2])  # например 10000000
if func_name not in functions:
    sys.exit()
result = timeit.timeit(functions[func_name], number=number)
print(result)
```

`sys.argv` — список аргументов командной строки. `argv[0]` = имя скрипта, `argv[1]` = имя функции, `argv[2]` = число. Функцию достаём из словаря по имени.

Запуск: `$ ./benchmark.py filter 10000000` → выводит только время.

---

## ex03 — Reduce

**Задача:** сравнить сумму квадратов двумя способами: цикл vs `reduce()`.

```python
from functools import reduce

def sum_loop(n):
    total = 0
    for i in range(1, n + 1):   # 1..n включительно
        total += i * i          # накапливаем квадраты
    return total

def sum_reduce(n):
    return reduce(lambda acc, i: acc + i*i, range(1, n + 1), 0)
```

**Как работает reduce:** сводит последовательность к одному значению:
```
reduce(f, [1,2,3], 0) = f(f(f(0, 1), 2), 3)
                      = (((0 + 1²) + 2²) + 3²)
```
- `acc` — накопленное значение (аккумулятор)
- `i` — текущий элемент
- начальное значение `0`

**Почему `from functools import reduce`:** `reduce` исключили из встроенных в Python 3 — теперь живёт в модуле `functools`.

```python
def run():
    functions[func_name](n)    # обёртка без аргументов, чтобы timeit мог вызвать
result = timeit.timeit(run, number=number)
```

Три аргумента: `func_name`, `number`, `n`. Запуск: `$ ./benchmark.py reduce 10000000 5`.

**Важно для защиты:** задание НЕ требует, чтобы reduce был быстрее. Оно просто сравнивает. loop обычно выигрывает (меньше накладных расходов, чем reduce+lambda).

---

## ex04 — Counter

**Задача:** посчитать частоту чисел в списке из 1М элементов самописной функцией vs `Counter`.

```python
from collections import Counter

# Самописный подсчёт
def count_manual(lst):
    d = {}
    for x in lst:
        d[x] = d.get(x, 0) + 1   # если ключа нет → 0, прибавляем 1
    return d

# Самописный топ-10
def top10_manual(lst):
    d = count_manual(lst)
    sorted_items = sorted(d.items(), key=lambda x: x[1], reverse=True)
    return sorted_items[:10]      # первые 10 после сортировки по убыванию
```

- `d.get(x, 0)` — вернуть значение по ключу `x`, а если ключа нет — `0`. Идиома подсчёта.
- `sorted(..., key=lambda x: x[1], reverse=True)` — сортируем пары `(число, количество)` по значению убывающе.

```python
# Counter версии
def count_counter(lst):
    return Counter(lst)                  # сам всё посчитает

def top10_counter(lst):
    return Counter(lst).most_common(10)  # готовый топ
```

```python
# Генерация данных
data = [random.randint(0, 100) for _ in range(1_000_000)]
```

**Замер:** `timeit(lambda: count_manual(data), number=10)` — 10 прогонов по 1М элементов.

**Вывод:** 4 строки — ручной счёт, Counter, ручной топ, Counter топ. Counter быстрее, потому что написан на C.

---

## ex05 — Генератор

**Задача:** прочитать большой файл `ratings.csv` (678 MB) двумя способами и сравнить **память**.

**ordinary.py** — всё в память:
```python
def read_all(path):
    with open(path) as f:
        return f.readlines()   # ЧИТАЕТ ВСЕ СТРОКИ В СПИСОК
```

**generator.py** — по одной строке:
```python
def read_generator(path):
    with open(path) as f:
        for line in f:
            yield line        # отдаёт ОДНУ строку и замирает
```

**Ключевое отличие:**
- `readlines()` → список всех строк → ~700+ MB в памяти → итог **2.06 GB**
- `yield` → функция становится генератором: каждая строка обрабатывается и забывается → **0.011 GB**

**Почему `yield`:** при вызове функции с `yield` тело не исполняется сразу. Каждый `next()`/итерация запускает функцию до следующего `yield`, возвращает значение и *приостанавливается* — не храня всё в памяти.

**Замер памяти:**
```python
import resource
usage = resource.getrusage(resource.RUSAGE_SELF)   # статистика о процессе
peak_gb = usage.ru_maxrss / (1024 * 1024)          # KB → GB (пик памяти)
cpu_time = usage.ru_utime + usage.ru_stime         # user + system время
print(f"Peak Memory Usage = {peak_gb:.3f} GB")
print(f"User Mode Time + System Mode Time = {cpu_time:.2f}s")
```

**Цикл с `pass`** — просто прогнать данные, ничего с ними не делая. Нужен для честного замера.

---

## Часть 3. Шпаргалка на защиту

### Вопросы-ловушки

1. **Почему listcomp быстрее цикла?** — CPython компилирует в оптимизированный байткод на C-уровне, без вызова `append()` на каждой итерации.
2. **map vs list comprehension — что быстрее?** — С готовой функцией (`str`, `int`) `map` быстрее (вызов C-функции напрямую). С `lambda` — listcomp обычно быстрее (меньше накладных).
3. **Почему filter?** — `filter` сам отбрасывает элементы по условию, не нужно превращать в `None` и убирать.
4. **Почему `from functools import reduce`?** — `reduce` перенесли из встроенных в модуль `functools` в Python 3.
5. **Что возвращает map/filter?** — Итератор, а не список. Нужен `list()`.
6. **Почему Counter быстрее ручной функции?** — Написан на C в CPython. Плюс `most_common()` — готовая реализация топа.
7. **Зачем генератор, если он может быть медленнее по времени?** — Экономия памяти критична для больших данных. Генератор вычисляет и хранит только один элемент за раз.
8. **`sys.exit()` при неверных аргументах** — скрипт корректно завершается без ошибки.

### Сравнение скорости (ориентир)

| Метод | Относительная скорость |
|---|---|
| map + готовая функция | 1x (быстрее всего) |
| List comprehension | 1.1x |
| filter + lambda | 1.3x |
| Цикл + append | 1.5x |
| reduce + lambda | 1.8x |
| map + lambda | 2x |

Зависит от задачи и машины — всегда замеряй сам.