# DSB5 — Примеры кода для каждого упражнения

Здесь готовые скрипты для каждого упражнения. Не копируй — разбирайся.

---

## ex00 — List Comprehensions

```python
import timeit

emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
          'anna@live.com', 'philipp@gmail.com'] * 5

def gmail_loop():
    result = []
    for e in emails:
        if "gmail" in e:
            result.append(e)
    return result

def gmail_listcomp():
    return [e for e in emails if "gmail" in e]

if __name__ == '__main__':
    loop_time = timeit.timeit(gmail_loop, number=90_000_000)
    lc_time = timeit.timeit(gmail_listcomp, number=90_000_000)

    if lc_time <= loop_time:
        print("it is better to use a list comprehension")
    else:
        print("it is better to use a loop")

    times = sorted([loop_time, lc_time])
    print(f"{times[0]} vs {times[1]}")
```

---

## ex01 — Map

```python
import timeit

emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
          'anna@live.com', 'philipp@gmail.com'] * 5

def gmail_loop():
    result = []
    for e in emails:
        if "gmail" in e:
            result.append(e)
    return result

def gmail_listcomp():
    return [e for e in emails if "gmail" in e]

def gmail_map():
    return list(map(lambda e: e if "gmail" in e else None, emails))
    # нужна фильтрация None, но для замера скорости — ок

if __name__ == '__main__':
    loop_time = timeit.timeit(gmail_loop, number=90_000_000)
    lc_time = timeit.timeit(gmail_listcomp, number=90_000_000)
    map_time = timeit.timeit(gmail_map, number=90_000_000)

    times = sorted([loop_time, lc_time, map_time])
    best = min(
        ("loop", loop_time),
        ("list comprehension", lc_time),
        ("map", map_time),
        key=lambda x: x[1]
    )
    print(f"it is better to use {best[0]}")
    print(f"{times[0]} vs {times[1]} vs {times[2]}")
```

---

## ex02 — Filter

```python
import timeit
import sys

emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
          'anna@live.com', 'philipp@gmail.com'] * 5

def gmail_loop():
    result = []
    for e in emails:
        if "gmail" in e:
            result.append(e)
    return result

def gmail_listcomp():
    return [e for e in emails if "gmail" in e]

def gmail_map():
    return list(map(lambda e: e if "gmail" in e else None, emails))

def gmail_filter():
    return list(filter(lambda e: "gmail" in e, emails))

functions = {
    "loop": gmail_loop,
    "list_comprehension": gmail_listcomp,
    "map": gmail_map,
    "filter": gmail_filter,
}

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit()

    func_name = sys.argv[1]
    number = int(sys.argv[2])

    if func_name not in functions:
        sys.exit()

    result = timeit.timeit(functions[func_name], number=number)
    print(result)
```

---

## ex03 — Reduce

```python
import timeit
import sys
from functools import reduce

def sum_loop(n):
    total = 0
    for i in range(1, n + 1):
        total += i * i
    return total

def sum_reduce(n):
    return reduce(lambda acc, i: acc + i*i, range(1, n + 1), 0)

functions = {
    "loop": sum_loop,
    "reduce": sum_reduce,
}

if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit()

    func_name = sys.argv[1]
    number = int(sys.argv[2])
    n = int(sys.argv[3])

    if func_name not in functions:
        sys.exit()

    def run():
        functions[func_name](n)

    result = timeit.timeit(run, number=number)
    print(result)
```

---

## ex04 — Counter

```python
import timeit
import random
from collections import Counter

def count_manual(lst):
    d = {}
    for x in lst:
        d[x] = d.get(x, 0) + 1
    return d

def top10_manual(lst):
    d = count_manual(lst)
    sorted_items = sorted(d.items(), key=lambda x: x[1], reverse=True)
    return sorted_items[:10]

def count_counter(lst):
    return Counter(lst)

def top10_counter(lst):
    return Counter(lst).most_common(10)

if __name__ == '__main__':
    data = [random.randint(0, 100) for _ in range(1_000_000)]

    manual_time = timeit.timeit(lambda: count_manual(data), number=10)
    counter_time = timeit.timeit(lambda: count_counter(data), number=10)

    manual_top_time = timeit.timeit(lambda: top10_manual(data), number=10)
    counter_top_time = timeit.timeit(lambda: top10_counter(data), number=10)

    print(f"my function: {manual_time:.7f}")
    print(f"Counter: {counter_time:.7f}")
    print(f"my top: {manual_top_time:.7f}")
    print(f"Counter's top: {counter_top_time:.7f}")
```

---

## ex05 — Генераторы

### ordinary.py
```python
import sys
import resource

def read_all(path):
    with open(path) as f:
        return f.readlines()

if __name__ == '__main__':
    filepath = sys.argv[1]
    lines = read_all(filepath)

    for line in lines:
        pass

    usage = resource.getrusage(resource.RUSAGE_SELF)
    peak_gb = usage.ru_maxrss / (1024 * 1024)
    cpu_time = usage.ru_utime + usage.ru_stime

    print(f"Peak Memory Usage = {peak_gb:.3f} GB")
    print(f"User Mode Time + System Mode Time = {cpu_time:.2f}s")
```

### generator.py
```python
import sys
import resource

def read_generator(path):
    with open(path) as f:
        for line in f:
            yield line

if __name__ == '__main__':
    filepath = sys.argv[1]
    gen = read_generator(filepath)

    for line in gen:
        pass

    usage = resource.getrusage(resource.RUSAGE_SELF)
    peak_gb = usage.ru_maxrss / (1024 * 1024)
    cpu_time = usage.ru_utime + usage.ru_stime

    print(f"Peak Memory Usage = {peak_gb:.3f} GB")
    print(f"User Mode Time + System Mode Time = {cpu_time:.2f}s")
```

---

## Как проверить что работает

```bash
# ex00
python3 benchmark.py
# → it is better to use a list comprehension
# → 55.71611063 vs 58.84998298

# ex02
python3 benchmark.py loop 10000000
# → 6.230267604

# ex04
python3 benchmark.py
# → my function: 0.4501532
# → Counter: 0.0432341

# ex05
python3 ordinary.py ratings.csv
python3 generator.py ratings.csv
```
