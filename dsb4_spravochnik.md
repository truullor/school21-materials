# DSB4 — Управление пакетами и виртуальные среды (учебник)

> Объёмный и структурированный гид по DSB4. Упор — на работу с **несколькими файлами** и инструментами Python (venv, pip, пакеты, cProfile, PyTest). Читай по главам, код учебных упражнений пиши сам.

## Оглавление
1. [Контекст: что такое «управление пакетами»](#1)
2. [Виртуальные окружения (venv)](#2)
3. [Модули и пакеты: работа с несколькими файлами](#3)
4. [pip и requirements.txt](#4)
5. [Shell-скрипты и termgraph (ex01)](#5)
6. [BeautifulSoup и парсинг (ex03)](#6)
7. [Профилирование cProfile / pstats (ex04)](#7)
8. [Тестирование PyTest (ex05)](#8)
9. [Конвенции и чек-лист сдачи](#9)
10. [Карта упражнений ex00–ex05](#10)
11. [План изучения](#11)

---

## 1. Контекст: что такое «управление пакетами» <a name="1"></a>

**Пакет (библиотека)** — чужой готовый код, который можно переиспользовать (`termgraph`, `beautifulsoup4`, `pytest`, …). Вместо того чтобы писать всё с нуля, ставишь пакет и импортируешь.

Две главные проблемы, которые решает DSB4:
- **Изоляция**: не лезть в системный Python (`sudo pip install` — плохая практика, можно сломать систему).
- **Воспроизводимость**: зафиксировать, какие пакеты и версии нужны проекту (`requirements.txt`).

Ключевая мысль проекта: пакеты и твой код живут **в виртуальном окружении** — отдельной песочнице. И весь твой код DSB4 тоже раскидан по **нескольким файлам** (`venv.py`, `pies_bars.sh`, `librarian.py`, `financial.py`, `financial_test.py`…). Поэтому ниже отдельная большая глава про многофайловость.

---

## 2. Виртуальные окружения (venv) <a name="2"></a>

### Зачем
Виртуальное окружение = копия Python в отдельной папке со своим `site-packages`. Ставишь туда пакеты — система не страдает. Сломал окружение — удалил папку, создал заново.

### Команды (Linux/macOS)
```bash
# создать окружение с именем = твой никнейм
python3 -m venv trullor

# активировать (подставляет venv/bin/python и venv/bin/pip в PATH)
source trullor/bin/activate

# проверить, что активно
which python      # покажет .../trullor/bin/python

# деактивировать
deactivate
```

На Windows активация иная: `trullor\Scripts\activate` (cmd) или `trullor/Scripts/Activate.ps1` (PowerShell).

### Как скрипт узнаёт, в каком он окружении (ex00)
Когда окружение активировано, Python ставит переменную среды `VIRTUAL_ENV` и меняет `sys.prefix`. Поэтому в `venv.py`:
```python
import os
import sys

# способ 1 (проще): читаем переменную среды
env_path = os.environ.get("VIRTUAL_ENV")

# способ 2: сравниваем префиксы
if sys.prefix != sys.base_prefix:
    env_path = sys.prefix

print(f"Your current virtual env is {env_path}")
```
Если окружение **не** активировано — `VIRTUAL_ENV` будет `None`, а `sys.prefix == sys.base_prefix`. Именно поэтому при деактивации скрипт выдаёт `None`/ошибку — он больше не видит путь к песочнице. Это и есть поведение, о котором предупреждает README (KeyError/None при деактивации — не страшно, просто объясни на защите).

### Что сдавать в ex00
- `venv.py` (скрипт выше),
- папку с самим виртуальным окружением (`trullor/`),
- окружение должно быть создано и активировано хотя бы раз.

> Важно: папку окружения (`trullor/`, `bin/`, `lib/`, `site-packages/`) надо добавить в `.gitignore` внутри самого окружения или не коммитить целиком — но в DSB4 окружение **архивируют** (см. ex02). Уточняй по инструкции конкретного упражнения.

---

## 3. Модули и пакеты: работа с несколькими файлами <a name="3"></a>

Это ядро твоего запроса. DSB4 (и вообще реальный Python) — это не один файл, а **набор файлов, которые импортируют друг друга**.

### Модуль и пакет
- **Модуль** = один файл `something.py`. Импорт модуля: `import something` → Python ищет `something.py`.
- **Пакет** = папка с файлом `__init__.py` внутри. Импорт из пакета: `from mypkg import mod`.

### Как Python ищет модуль (sys.path)
При `import x` Python перебирает папки из списка `sys.path` (выведи `import sys; print(sys.path)`). Туда входят:
1. текущая папка (откуда запустили скрипт),
2. стандартная библиотека,
3. `site-packages` активного окружения (туда pip ставит пакеты).

Поэтому импорт работает, только если файл/пакет лежит в одной из этих папок.

### Абсолютные vs относительные импорты
Допустим, структура:
```
project/
    src/
        tool.py          # def add(a,b): return a+b
        main.py          # from tool import add
```
В `main.py` абсолютный импорт: `from tool import add` (ищет `tool` в `sys.path`). Если запускать `python main.py` из `src/`, сработает.

Относительный импорт (внутри пакета):
```
project/
    src/
        mypkg/
            __init__.py
            core.py      # def run(): ...
            utils.py     # from .core import run   <-- относительный: "." = текущий пакет
```
`from .core import run` означает «возьми core из ТОГО ЖЕ пакета, где я». Точка = текущий пакет, `..` = родительский.

### Рекомендованная структура многофайлового проекта
```
project/
    src/                  # рабочая директория (по инструкции DSB — работай в src)
        ex00/
            venv.py
        ex03/
            financial.py
            financial_test.py
    requirements.txt
    .gitignore
```
Для DSB4 каждое упражнение — отдельная папка `exNN/`. Внутри — свои файлы. Это и есть «несколько файлов».

### Типичные ошибки импортов
| Ошибка | Почему | Как исправить |
|---|---|---|
| `ModuleNotFoundError: No module named 'x'` | файл `x.py` не в `sys.path` | запускай из правильной папки или добавь путь (`sys.path.insert(0, папка)`) |
| `ImportError: attempted relative import with no known parent package` | относительный импорт запустили как скрипт (`python utils.py`) | запускай извне пакета или используй абсолютный импорт |
| циклический импорт (A импортирует B, B импортирует A) | плохая архитектура | вынеси общее в третий модуль |

### Практика (сам себе)
Создай `src/sandbox/pkg_a/__init__.py` и `src/sandbox/pkg_a/hello.py` (`def hi(): return "привет"`), и `src/sandbox/run.py` с `from pkg_a.hello import hi; print(hi())`. Запусти `python run.py` из `src/sandbox/`. Почувствуй, как файлы связываются через импорт — это та же «связка вызовов», что в OOP, только на уровне файлов.

---

## 4. pip и requirements.txt <a name="4"></a>

### Установка
```bash
# ВНУТРИ активированного окружения:
pip install termgraph
pip install beautifulsoup4
pip install pytest
```
Не используй `sudo pip install` — ставишь в системный Python.

### requirements.txt (ex02)
Зафиксируй состав окружения:
```bash
pip freeze > requirements.txt
```
Файл содержит `name==version` для всех установленных пакетов:
```
six==1.14.0
soupsieve==2.0
termgraph==0.2.0
wcwidth==0.1.9
```
Установить всё разом (без циклов, одной командой — этого и требует ex02):
```bash
pip install -r requirements.txt
```

### ex02: librarian.py (что делать)
1. Проверь, что скрипт запущен **в нужном виртуальном окружении**: сравни `sys.prefix` (или `os.environ["VIRTUAL_ENV"]`) с ожидаемым путём. Если не совпадает — `raise Exception(...)`.
2. Установи нужные пакеты (BeautifulSoup, PyTest) — через `pip install -r requirements.txt` из кода (`subprocess.run(["pip", "install", "-r", "requirements.txt"])`) или вручную.
3. Выведи список установленных пакетов (`pip freeze`) и сохрани в `requirements.txt`.
4. Захарчь окружение: `tar -czf venv.tar.gz trullor/` (или программно) и положи архив в папку ex02.

---

## 5. Shell-скрипты и termgraph (ex01) <a name="5"></a>

### Shell-скрипт `pies_bars.sh`
- Первая строка — shebang: `#!/bin/bash`.
- Сделай исполняемым: `chmod +x pies_bars.sh`.
- Запуск: `./pies_bars.sh` (должен быть активирован venv, иначе `termgraph` не найдётся).
- В скрипте — **только** часть построения графика, без activate/deactivate:
```bash
#!/bin/bash
python -m termgraph data.txt --color {blue,red} --title "Pies vs Bars"
```
(точный синтаксис termgraph смотри в `termgraph --help`; цвета — другие, чем в примере README).

### termgraph
Рисует bar-чарт прямо в терминале. Данные — файл со строками `метка,значение` или `метка значение`. Пример `data.txt`:
```
Pies 5
Bars 7
```
Запуск: `python -m termgraph data.txt --color blue`.

---

## 6. BeautifulSoup и парсинг (ex03) <a name="6"></a>

### Зачем
Сайт отдаёт HTML. BeautifulSoup превращает его в дерево, по которому удобно ходить (`soup.find`, `soup.select`).

### Схема (ex03 financial.py)
```python
import sys
import time
import requests
from bs4 import BeautifulSoup

def get_field(ticker, field):
    url = f"https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if resp.status_code != 200:
        raise Exception("bad URL")
    soup = BeautifulSoup(resp.text, "html.parser")
    # найти строку таблицы по названию поля и вытащить ячейки
    ...
    time.sleep(5)   # ОБЯЗАТЕЛЬНО: "сон на 5 секунд" (нужен для ex04)
    return (field, val1, val2, ...)

if __name__ == "__main__":
    print(get_field(sys.argv[1], sys.argv[2]))
```
Особенности:
- Принимает тикер и поле как аргументы (`sys.argv[1]`, `sys.argv[2]`).
- Возвращает **кортеж** (`return`, не print).
- `sleep(5)` — оставь, в ex04 будешь профилировать именно его.
- Если URL/поля нет — `raise`.

> Парсинг Yahoo Finance хрупок (вёрстка меняется). Главное — понять механику: запрос → парсинг → извлечение → возврат кортежа. На защите объясни логику, а не конкретный селектор.

---

## 7. Профилирование cProfile / pstats (ex04) <a name="7"></a>

**Профилирование** — измерение, где код тратит время/вызовы. DSB4 требует `cProfile`.

### Команды
```bash
# 1. профиль по общему времени (tottime), сохранить в файл
python -m cProfile -s tottime financial.py 'MSFT' 'Total Revenue' > profiling-sleep.txt

# 2. убрать time.sleep(5) из financial.py, повторить -> profiling-tottime.txt

# 3. сменить HTTP-клиента (например, urllib вместо requests) -> financial_enhanced.py -> profiling-http.txt

# 4. отсортировать по числу вызовов (ncalls)
python -m cProfile -s ncalls financial.py 'MSFT' 'Total Revenue' > profiling-ncalls.txt
```

### pstats (кумулятивное время, топ-5)
```python
import pstats
p = pstats.Stats("профиль_файл.prof")   # cProfile можно писать в .prof через -o
p.sort_stats("cumulative").print_stats(5)
```
Сохрани в `pstats-cumulative.txt`.

### Что искать
- `tottime` — чистое время в функции (без учёта вызванных). `sleep` там будет большим.
- `cumtime` — время с учётом всех вложенных вызовов.
- `ncalls` — сколько раз вызвана; много вызовов = кандидат на оптимизацию.

---

## 8. Тестирование PyTest (ex05) <a name="8"></a>

**Тест** = проверка, что функция при заданном входе даёт ожидаемый выход. PyTest находит функции `test_*`, запускает и сверяет через `assert`.

### Пример financial_test.py
```python
import pytest
from financial import get_field

def test_returns_tuple():
    assert isinstance(get_field("MSFT", "Total Revenue"), tuple)

def test_total_revenue_value():
    res = get_field("MSFT", "Total Revenue")
    assert res[0] == "Total Revenue"

def test_bad_ticker_raises():
    with pytest.raises(Exception):
        get_field("NONEXISTENT_TICKER_XYZ", "Total Revenue")
```
Запуск из папки ex05 (в активированном venv с pytest):
```bash
pytest financial_test.py
```
Все тесты должны быть зелёными. Если нет — чини `financial.py`.

Правило ex05: для **каждой** функции — минимум 3 теста (нормальный случай, тип возврата, исключение).

---

## 9. Конвенции и чек-лист сдачи <a name="9"></a>

Общие правила DSB (из инструкции проекта):
- **Никакого кода в глобальной области.** Всё в функциях.
- В конце каждого `.py` — блок `if __name__ == '__main__':` (там вызовы и обработка ошибок).
- **Импорты только разрешённые** в шапке упражнения (в DSB4 большинство — «без ограничений», но проверяй).
- **Только те файлы, что указаны** в задании. Лишнее — в `.gitignore`.
- Работай в `src/`. Пушь **только в `develop`** (`master` игнорируется проверяющими).
- `if __name__` не подменяй заранее заготовленным выводом — скрипт должен реально работать.

`.gitignore` (минимум для DSB4):
```
__pycache__/
*.pyc
trullor/            # папка окружения (если не архивируешь иначе)
*.tar.gz            # если архив не коммитишь
```

---

## 10. Карта упражнений ex00–ex05 <a name="10"></a>

| Упр | Файлы | Суть |
|---|---|---|
| ex00 | `venv.py` + папка venv | создать/активировать venv, скрипт печатает путь через `os` |
| ex01 | `pies_bars.sh` + data + venv | поставить `termgraph`, нарисовать график в терминале, shell-скрипт |
| ex02 | `librarian.py` + архив venv | поставить BS4+PyTest через `requirements.txt`, проверить окружение, сохранить `requirements.txt` |
| ex03 | `financial.py` | BeautifulSoup парсит Yahoo Finance, возврат кортежа, `sleep(5)` |
| ex04 | `financial.py`, `financial_enhanced.py`, `profiling-*.txt`, `pstats-cumulative.txt` | cProfile/pstats, убрать sleep, сменить HTTP-клиент |
| ex05 | `financial_test.py` | PyTest, минимум 3 теста на функцию |

---

## 11. План изучения <a name="11"></a>

1. **Вечер/день 1:** главы 2 и 3 (venv + многофайловость) — самое важное концептуально. Потренируйся: создай venv, напиши `venv.py`, потренируй импорт из п. 3.
2. **День 2:** главы 4 и 5 (pip/requirements, termgraph) → сделай ex00, ex01, ex02.
3. **День 3:** глава 6 (BeautifulSoup) → ex03.
4. **День 4:** глава 7 (cProfile) → ex04.
5. **День 5:** глава 8 (PyTest) → ex05.
6. Перед сдачей: глава 9 (чек-лист), `git checkout -b develop`, коммит, пуш.

Совет: DSB4 — про **инструменты**, а не про сложный алгоритм. Пойми механику (venv изолирует, pip ставит, import связывает файлы, cProfile мерит, pytest проверяет) — и упражнения пойдут сами.
