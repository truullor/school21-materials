# DSB3 — план за час (делаем БЕЗ ассистента)

Пошаговый чеклист выполнения проекта на ноуте. Рядом держи `dsb3_spravochnik.md` (там скелеты кода). Цель часа — дойти до ex02–ex03 своими руками; ex04–ex06 добьём вечером вместе.

## 0. Подготовка (2 мин)
- Зайди в проект: `cd ~/projects/DSB3_OOP_skills_ID_1577670-1`
- Создай ветку: `git checkout -b develop`  ← НЕ работай на `master`!
- Убедись, что `data.csv` готов (он в задании: заголовок `head,tail`, 11 строк данных `0,1`/`1,0`).

## 1. ex00 — простой класс (5 мин)
- Файл: `src/ex00/first_class.py`
- Класс `Must_Read`, читает `data.csv` и печатает его. Без методов и конструктора.
- Главное: код внутри класса выполняется при его создании.

## 2. ex01 — метод (5 мин)
- `src/ex01/first_method.py`, класс `Research`.
- Перенеси чтение в метод `file_reader(self)`, вместо `print` поставь `return`.
- Внизу файла: `print(Research().file_reader())`.

## 3. ex02 — конструктор (10 мин)
- `src/ex02/first_constructor.py` (разрешён `import sys, os`).
- `__init__(self, path)` → `self.path = path`.
- `file_reader` читает через `self.path`.
- Валидация: заголовок `head,tail`; каждая строка только `[0,1]` или `[1,0]`; иначе `raise`.
- Путь бери из `sys.argv[1]`.
- Тест: `python src/ex02/first_constructor.py data.csv`

## 4. ex03 — вложенный класс (10 мин)
- `src/ex03/first_nest.py` (`sys`, `os`).
- `file_reader(self, has_header=True)` → список списков `[[0,1],[1,0],...]`.
- Вложенный `class Calculations`: `counts(data)` → (орлы, решки); `fractions(heads, tails)` → (%, %).
- Орлы = сумма 1-х элементов строк, решки = сумма 2-х.

## 5. ex04 — наследование (10 мин)
- `src/ex04/first_child.py` (`sys`, `from random import randint`).
- `Calculations.__init__(self, data)` → `self.data = data`.
- `Analytics(Calculations)`: `predict_random(n)`, `predict_last()`.

## 6. ex05 — модули и конфиг (10 мин)
- `config.py`: `num_of_steps` + шаблон отчёта (глобальные переменные, БЕЗ `__main__`).
- `analytics.py`: классы ex04 + `save_file(self, data, filename, ext)` (БЕЗ `__main__`).
- `make_report.py`: логика + `if __name__ == '__main__':`, импортирует `config` и `analytics`.

## 7. ex06 — логирование (10 мин)
- Те же 3 файла.
- Каждый метод пишет в `analytics.log` форматом `"%(asctime)s %(message)s"` (дата время сообщение).
- В `Research` — метод отправки в Телеграм через webhook (`requests.post`).

## 8. Финал (5 мин)
- Проверь каждое упражнение запуском.
- `git add . && git commit -m "DSB3 OOP done" && git push -u origin develop`
- Застрял — см. `dsb3_errors.md`.
