# Шпаргалка ООП (DSB3) — карманная

> Быстрый синтаксис для взгляда на телефоне. Подробности — в `dsb3_spravochnik.md`.

## Класс и объект
```python
class Research:          # чертёж
    pass
r = Research()           # объект (экземпляр)
```

## Метод (функция в классе)
```python
class Research:
    def file_reader(self):     # первый параметр ВСЕГДА self
        return "данные"
r = Research()
r.file_reader()          # self подставляется сам
```
- Метод **возвращает** (`return`), класс сам по себе — нет.
- Печатает основная программа, не метод.

## self — «я сам»
```python
def __init__(self, path):
    self.path = path      # сохранили в объект
def file_reader(self):
    open(self.path)       # взяли из объекта
```

## Конструктор `__init__`
```python
class Research:
    def __init__(self, path):   # запускается при создании объекта
        self.path = path
r = Research("data.csv")  # "data.csv" → path
```

## Вложенный класс
```python
class Research:
    def file_reader(self, has_header=True):
        ...
    class Calculations:          # класс внутри класса
        def counts(self, data):
            ...
```

## Наследование
```python
class Analytics(Calculations):   # берёт всё от Calculations
    def predict_random(self, n):
        ...
# Analytics видит методы Calculations (counts, fractions)
```

## Импорт своих модулей
```python
import config              # config.py той же папки
from analytics import Analytics   # класс из analytics.py
```

## Логирование (ex06)
```python
import logging
logging.basicConfig(filename='analytics.log',
                    format='%(asctime)s %(message)s')
logging.info("сообщение")   # → 2020-05-01 22:16:16,877 сообщение
```

## Типичные ошибки новичка
| Ошибка | Как правильно |
|---|---|
| забыл `self` в методе | всегда `def m(self, ...)` |
| пишет `print` внутри, а нужен `return` | метод возвращает, main печатает |
| `self.data` не видно в наследнике | положи данные в `__init__` родителя |
| путает колонки `[орёл, решка]` | орлы = сумма 1-х элементов, решки = сумма 2-х |
| код в глобальной области | только в функциях/методах + `if __name__` |
