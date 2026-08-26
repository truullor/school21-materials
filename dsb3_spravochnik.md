# Самоучитель DSB3 — ООП на Python (для учёбы с телефона)

> Цель файла: ты читаешь его на работе/в дороге, понимаешь ООП и потом САМ быстро делаешь проект, не сидя со мной.
> Проект: `DSB3_OOP_skills_ID_1577670-1`. Суть: одна программа анализа монеты (орёл/решка), которую ты шаг за шагом переделываешь в объектный стиль (ex00→ex06).

---

## 0. Главное понимание (прочти первым)

**Все 7 упражнений — это ОДИН и тот же проект, который ты постепенно улучшаешь.** Файл `data.csv` не меняется. Каждое упражнение добавляет ровно одну новую идею ООП поверх предыдущего. Поэтому, поняв общий поток, ты делаешь их почти механически.

Поток данных всегда такой:
```
data.csv → прочитать → [[0,1],[1,0],...] → посчитать орлы/решки → доли % → (позже) предсказания и отчёт
```

**Правила проекта (из README):**
- Никакого кода в глобальной области — только в функциях/методах.
- В конце каждого файла: `if __name__ == '__main__':` (кроме ex05/ex06, где `config.py` и `analytics.py` НЕ имеют этого блока).
- Импорты только те, что разрешены в шапке упражнения.
- **Ветка `develop`**: сейчас репозиторий на `master`. Перед началом: `git checkout -b develop`. Пуши только в `develop`.
- В `src/` только файлы из задания.

---

## 1. Быстрый курс ООП (теория, которой хватит)

### Класс и объект
- **Класс** — это чертёж/шаблон. **Объект (экземпляр)** — конкретная вещь, созданная по чертежу.
- Создаём класс: `class Research:` — имя с большой буквы по конвенции.
- Создаём объект: `r = Research()` — вызываем класс как функцию.

### Метод = функция внутри класса
- Отличается тем, что первым аргументом всегда идёт `self` (ссылка на сам объект).
- `def file_reader(self):` — внутри класса. Вызываешь: `r.file_reader()` (self подставляется автоматически).
- **Методы могут возвращать значение (`return`), классы сами по себе — нет.** В ex01 как раз меняешь `print()` на `return`.

### self — это «я сам»
- Через `self` метод обращается к данным объекта: `self.path`, `self.data`.
- Конструктор `__init__` сохраняет пришедшие данные в `self`, чтобы другие методы их видели.

### Конструктор `__init__`
- Выполняется автоматически при создании объекта: `def __init__(self, path): self.path = path`.
- Создаёшь так: `r = Research("data.csv")` — `"data.csv"` попадает в `path`.

### Вложенный класс
- Класс внутри класса: `class Research:  class Calculations: ...`. Помогает сгруппировать логику.

### Наследование
- `class Analytics(Calculations):` — `Analytics` получает все методы `Calculations` бесплатно.
- Дальше добавляешь свои методы или переопределяешь.

### Импорт своих модулей
- `import config` — подхватит `config.py` из той же папки.
- `from analytics import Analytics` — подхватит класс из `analytics.py`.

### Логирование и запросы (ex06)
- `logging` пишет события в файл (дата время сообщение).
- `requests`/`urllib` + Telegram webhook — отправка сообщения по URL.

---

## 2. По упражнениям (что делать + скелет)

### ex00 — Простой класс (`first_class.py`)
**Суть:** класс `Must_Read` читает `data.csv` и печатает его. Пока БЕЗ методов и конструктора — код прямо в теле класса.
```python
class Must_Read:
    with open("data.csv") as f:
        for line in f:
            print(line.rstrip())
```
При создании класса этот код выполняется. Запуск: `python3 first_class.py` → печатает файл.
**Камень:** `data.csv` создай сам (см. раздел 3).

### ex01 — Метод (`first_method.py`)
**Суть:** переносишь код в метод `file_reader()`, меняешь класс на `Research`, `print` → `return`.
```python
class Research:
    def file_reader(self):
        with open("data.csv") as f:
            return f.read()
if __name__ == '__main__':
    print(Research().file_reader())
```
**Камень:** метод возвращает строку, печатает основная программа.

### ex02 — Конструктор (`first_constructor.py`, импорт: sys, os)
**Суть:** путь к файлу приходит аргументом (`sys.argv[1]`), сохраняется в `__init__`, `file_reader` берёт его из `self.path`. При плохой структуре файла — `raise`.
```python
import sys
class Research:
    def __init__(self, path):
        self.path = path
    def file_reader(self):
        with open(self.path) as f:
            lines = f.read().splitlines()
        # валидация: заголовок "head,tail", строки из 0/1
        if lines[0] != "head,tail":
            raise ValueError("Bad structure")
        for row in lines[1:]:
            parts = row.split(",")
            if parts != ["0","1"] and parts != ["1","0"]:
                raise ValueError("Bad row")
        return "\n".join(lines)
if __name__ == '__main__':
    print(Research(sys.argv[1]).file_reader())
```
**Камень:** `raise` при неверной структуре (заголовок две колонки-запятые; строки — либо `0,1`, либо `1,0`, никогда не оба сразу).

### ex03 — Вложенный класс (`first_nest.py`, импорт: sys, os)
**Сути две:**
1. `file_reader(self, has_header=True)` возвращает **список списков** `[[0,1],[1,0],...]` (без заголовка). Если `has_header=False` — не пропускать первую строку.
2. Вложенный класс `Calculations` с методами:
   - `counts(data)` → количество орлов и решек. Орёл = сумма первых элементов строк, решка = сумма вторых. Возвращает `(heads, tails)`, напр. `(5, 6)`.
   - `fractions(heads, tails)` → доли в %: `heads/(heads+tails)*100`, `tails/(heads+tails)*100`. Возвращает `(h%, t%)`, напр. `(45.45, 54.54)`.

```python
class Research:
    def file_reader(self, has_header=True):
        with open(self.path) as f:
            lines = f.read().splitlines()
        if has_header:
            lines = lines[1:]
        return [[int(x) for x in row.split(",")] for row in lines]
    class Calculations:
        def counts(self, data):
            heads = sum(r[0] for r in data)
            tails = sum(r[1] for r in data)
            return heads, tails
        def fractions(self, heads, tails):
            t = heads + tails
            return heads/t*100, tails/t*100
```
Вывод скрипта: данные, затем `counts`, затем `fractions`.
**Камень:** данные — это пары `[орёл, решка]`, где `1` = выпала эта сторона. Значит орлы = сумма первых столбцов, решки = сумма вторых.

### ex04 — Наследование (`first_child.py`, импорт: sys, from random import randint)
**Суть:**
1. Данные переносятся в `Calculations.__init__(self, data)` (храним `self.data`).
2. Новый класс `Analytics(Calculations)` наследует `counts`/`fractions`.
3. В `Analytics` добавить:
   - `predict_random(n)` → список из `n` случайных наблюдений `[1,0]` или `[0,1]` (через `randint(0,1)`).
   - `predict_last()` → последний элемент `self.data` (как список).

```python
from random import randint
class Calculations:
    def __init__(self, data):
        self.data = data
    def counts(self):
        heads = sum(r[0] for r in self.data)
        tails = sum(r[1] for r in self.data)
        return heads, tails
    def fractions(self):
        h, t = self.counts()
        tot = h + t
        return h/tot*100, t/tot*100
class Analytics(Calculations):
    def predict_random(self, n):
        out = []
        for _ in range(n):
            out.append([1,0] if randint(0,1)==0 else [0,1])
        return out
    def predict_last(self):
        return self.data[-1]
```
Вывод: данные, counts, fractions, predict_random(3), predict_last.
**Камень:** `Analytics` видит `self.data` из родителя — благодаря наследованию.

### ex05 — Конфиг и модули (`config.py`, `analytics.py`, `make_report.py`)
**Суть:** разнести код по файлам.
- `config.py`: глобальные переменные разрешены. Храни `num_of_steps` (для predict_random) и ШАБЛОН текста отчёта (строка с плейсхолдерами). Блок `__main__` НЕ нужен.
- `analytics.py`: классы из ex04, переименованные файлы. Добавить метод `save_file(self, data, filename, ext)` — сохраняет `data` в файл `filename.ext` (например, `.txt`). Блок `__main__` НЕ нужен.
- `make_report.py`: вся логика программы. Импортирует `config` и `analytics`, создаёт объект, считает, формирует отчёт по шаблону из `config`, сохраняет через `save_file`. Имеет `__main__`.

Пример отчёта (цифры берутся из реальных данных!):
```
В нашем эксперименте с подбрасыванием монеты из 12 наблюдений пять раз выпала решка и семь раз — орёл. Вероятности составляют 41,67% и 58,33% соответственно. Мы прогнозируем, что в следующих трёх наблюдениях решка выпадет один раз, а орёл — два раза.
```
**Камень:** шаблон текста — в `config.py`; заполняй его f-строкой или `.format` значениями.

### ex06 — Логирование (`config.py`, `analytics.py`, `make_report.py`)
**Суть:**
1. В КАЖДОМ методе КАЖДОГО класса писать в `analytics.log` строку `ДАТА ВРЕМЯ сообщение` (через пробел), напр.:
   `2020-05-01 22:16:16,877 Calculating the counts of heads and tails`
   Используй модуль `logging` (настрой `basicConfig(filename='analytics.log', format='%(asctime)s %(message)s')`).
2. В классе `Research` добавить метод, отправляющий сообщение в Telegram через webhook (`requests.post(url, ...)`): либо `"The report has been successfully created"`, либо `"The report hasn't been created due to an error."`
**Камень:** формат лога — дата, время (с миллисекундами), сообщение, разделитель пробел.

---

## 3. Файл data.csv (создай сам в ex00)
```
head,tail
0,1
1,0
0,1
1,0
0,1
0,1
0,1
1,0
1,0
0,1
1,0
```

---

## 4. Чек-лист перед сдачей
- [ ] Создал ветку `develop` и пушил туда.
- [ ] В каждом файле нет глобального кода (кроме `config.py` в ex05/06 — там переменные разрешены).
- [ ] `if __name__ == '__main__':` есть где надо (не в `config.py`/`analytics.py` ex05/06).
- [ ] Импорты только разрешённые.
- [ ] `data.csv` лежит там, где скрипт его ищет.
- [ ] ex02/ex03/ex04 выводят ровно то, что в примерах README.
- [ ] Нет лишних файлов в `src/exXX/`.

---

## 5. Как учить по этому файлу (план)
1. Прочти раздел 1 (ООП-теория) — 20 минут, станет понятно.
2. Прочти раздел 2 сверху вниз — увидишь, как один проект растёт.
3. Когда делаешь проект на ноуте: открывай нужное упражнение, пиши по скелету, сверяй вывод с примером README.
4. Застрял — слушай `dsb3_audio.txt` (аудио-версию) в дороге.
