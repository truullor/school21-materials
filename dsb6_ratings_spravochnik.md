# DSB6 — Справочник: класс Ratings (вложенные Movies и Users)

## Данные (ratings.csv)
```
header: userId, movieId, rating, timestamp
row:    ['1', '1', '4.0', '964982703']
```
В self.rows каждая запись — список строк: `userId`, `movieId`, `rating` (текст-число), `timestamp` (Unix-секунды).

## Структура класса
```
Ratings(BaseDataset)           ← родитель, читает ratings.csv
   ├── class Movies(BaseDataset)  ← читает ratings.csv + movies.csv
   │     └── class Users(Movies)  ← наследует Movies (любые данные доступны)
```
- `Ratings` — просто оболочка, сам ничего не делает (наследует `BaseDataset`, есть `__init__` с `super().__init__`).
- `Ratings.Movies(ratings_path, movies_path)` — ему нужен ПУТЬ к ratings.csv И к movies.csv (для названий).
- `Ratings.Users(...)` — те же 2 пути, наследует всё от Movies.

### Почему Movies принимает 2 файла
Топы отдают НАЗВАНИЯ фильмов, а не id. Поэтому Movies строит словарь:
```python
self.movie_titles = {m[0]: m[1] for m in movies}   # movieId -> название
```
Внутренний помощник `_title(movie_id)`:
```python
return self.movie_titles.get(movie_id, movie_id)   # нет названия → отдаём id как есть
```
⚠️ `'2018'` в топах = id фильма, которого нет в первых 1000 строк movies.csv (лимит 1000 из README). Это нормально.

## Утилиты в модуле (моя зона — Разработчик А)
`statistics` в README запрещён, поэтому написаны вручную в модуле:
- `average(values)` — среднее арифметическое
- `median(values)` — медиана
- `variance(values)` — дисперсия (средний квадрат отклонений)

Импорт: `from datetime import datetime`, `from collections import defaultdict` (оба разрешены).

## Методы Ratings.Movies

| метод | что | сортировка | приём |
|---|---|---|---|
| `dist_by_year()` | год → число оценок | по году ВОЗРАСТ. | `datetime.fromtimestamp(int(row[3])).year` |
| `dist_by_rating()` | оценка → число | по оценке ВОЗРАСТ. | `float(row[2])` как ключ |
| `top_by_num_of_ratings(n)` | название → число оценок | по числу УБЫВ., топ-n | `len(values)` |
| `top_by_ratings(n, metric=average)` | название → средн./медиана | по метрике УБЫВ., топ-n, `round(...,2)` | `metric(values)` |
| `top_controversial(n)` | название → дисперсия | по дисперсии УБЫВ., топ-n, `round(...,2)` | `variance(values)` |

### Внутренние помощники Movies
```python
def _group_by_movie(self):
    grouped = defaultdict(list)
    for row in self.rows:
        grouped[row[1]].append(float(row[2]))   # movieId -> [оценки]
    return grouped

def _top_by_metric(self, n, metric):
    result = {}
    for movie_id, values in self._group_by_movie().items():
        result[self._title(movie_id)] = round(metric(values), 2)
    return dict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:n])
```
`_top_by_metric(n, metric)` используется и в `top_by_ratings`, и в `top_controversial` (передаётся `average`/`median` или `variance`) — без дублирования кода.

## Методы Ratings.Users (наследует Movies)

| метод | что | сортировка | приём |
|---|---|---|---|
| `dist_by_num_of_ratings()` | сколько оценок сделал пользователь → сколько таких пользователей | по числу оценок ВОЗРАСТ. | `len(values)` по группе пользователя |
| `dist_by_avg_rating(metric=average)` | средн./медиана оценок пользователя → сколько таких | по метрике ВОЗРАСТ., `round(...,2)` | `metric(values)` |
| `top_controversial_users(n)` | userId → дисперсия его оценок | по дисперсии УБЫВ., топ-n, `round(...,2)` | `variance(values)` |

💡 Users НЕ переопределяет `dist_by_year`/`dist_by_rating`/топы Movies — они наследуются и работают (данные те же). Новые методы учитываются **по userId, а не movieId**:
```python
def _group_by_user(self):
    grouped = defaultdict(list)
    for row in self.rows:
        grouped[row[0]].append(float(row[2]))   # userId -> [оценки]
    return grouped
```

## Приёмы, повторяющиеся всюду
1. `dict.get(key, 0) + 1` — счётчик без KeyError
2. `dict(sorted(d.items(), key=lambda x: x[1], reverse=True))` — сортировка по значению
3. `sorted(..., key=lambda x: x[0])` — сортировка по ключу (годам, оценкам) — без reverse для ВОЗРАСТАНИЯ
4. `[:n]` — срез списка пар до топ-`n`
5. `round(value, 2)` — округление до 2 знаков (требование README)
6. `defaultdict(list)` + `append` — группировка id → список значений
7. `float(row[2])` — оценка хранится как строка `'4.0'`, нужна как число

## Как вызвать
```python
rm = r.Movies('ml-latest-small/ratings.csv', 'ml-latest-small/movies.csv')
rm.top_by_ratings(5)
rm.top_by_ratings(5, metric=median)   # замена метрики
ru = r.Users('ml-latest-small/ratings.csv', 'ml-latest-small/movies.csv')
ru.top_controversial_users(5)
```

## Чек-лист требований README (по этой части)
- [x] типы: dict во всех методах
- [x] сортировка: везде явная (возр./убыв. по заданию)
- [x] `round(..., 2)` в метриках
- [x] используется `movieId→название` для читаемых топов
- [x] тесты PyTest на каждый метод — НАПИСАНЫ (класс `Tests` в модуле)

---

# ТЕСТЫ PyTest (теория + код)

## Что такое PyTest
Фреймворк для запуска тестов. Ты пишешь функции/методы с assert'ами, pytest находит их, запускает и сообщает, что упало.
Всё, что нужно от теста — **`assert <условие>`**. Если условие ложное — тест падает (красный).

## Как pytest находит тесты
- **Файлы**: `test_*.py` или `*_test.py`.
- **Классы**: имя начинается с `Test` (у нас `Tests`).
- **Методы**: имя начинается с `test_`.

В нашем проекте тесты живут **в классе `Tests` внутри самого модуля** `movielens_analysis.py` (требование README: «один класс для тестирования»). Запуск:
```
python -m pytest src/movielens_analysis.py -v
```

## Теория: что проверяем (по README, 3 пункта)
1. **метод возвращает корректный тип** → `assert isinstance(res, dict)`
2. **элементы списков имеют корректные типы** → `all(isinstance(k, int) for k in res)` и т.д.
3. **данные отсортированы корректно** → сравнить список значений с сортированным:
   ```python
   list(res.values()) == sorted(res.values(), reverse=True)   # убывание
   list(res.keys()) == sorted(res.keys())                     # возрастание по ключам
   ```

## Как устроен класс Tests

**Пути к данным** — строятся относительно файла, чтобы тест работал из любой папки:
```python
movies = os.path.join(os.path.dirname(__file__), "ml-latest-small", "movies.csv")
ratings = os.path.join(os.path.dirname(__file__), "ml-latest-small", "ratings.csv")
```
(`os` — разрешённый импорт.)

**Помощники** — сокращают проверки сортировки:
```python
@staticmethod
def _desc(values):
    return list(sorted(values, reverse=True))

@staticmethod
def _asc(values):
    return list(sorted(values))
```

## Полный код класса Tests (уже в модуле)

```python
class Tests:
    """PyTest-тесты для классов Movies, Ratings и утилит."""

    movies = os.path.join(os.path.dirname(__file__), "ml-latest-small", "movies.csv")
    ratings = os.path.join(os.path.dirname(__file__), "ml-latest-small", "ratings.csv")

    @staticmethod
    def _desc(values):
        return list(sorted(values, reverse=True))

    @staticmethod
    def _asc(values):
        return list(sorted(values))

    def test_util_average(self):
        assert average([1, 2, 3]) == 2.0
        assert average([5]) == 5.0

    def test_util_median(self):
        assert median([1, 2, 3]) == 2.0
        assert median([1, 2, 3, 4]) == 2.5

    def test_util_variance(self):
        assert variance([1, 3]) == 1.0
        assert variance([2, 2, 2]) == 0.0

    def test_dist_by_release(self):
        res = Movies(self.movies).dist_by_release()
        assert isinstance(res, dict)
        assert all(isinstance(k, int) for k in res)          # ключи — годы (int)
        assert all(isinstance(v, int) for v in res.values()) # значения — счётчики (int)
        assert list(res.values()) == self._desc(res.values())  # по убыванию

    def test_dist_by_genres(self):
        res = Movies(self.movies).dist_by_genres()
        assert isinstance(res, dict)
        assert all(isinstance(k, str) for k in res)          # ключи — жанры (str)
        assert all(isinstance(v, int) for v in res.values())
        assert list(res.values()) == self._desc(res.values())

    def test_most_genres(self):
        res = Movies(self.movies).most_genres(5)
        assert isinstance(res, dict)
        assert len(res) <= 5                                  # топ-n, не больше n
        assert all(isinstance(k, str) for k in res)
        assert all(isinstance(v, int) for v in res.values())
        assert list(res.values()) == self._desc(res.values())

    def test_dist_by_year(self):
        rm = Ratings(self.ratings).Movies(self.ratings, self.movies)
        res = rm.dist_by_year()
        assert isinstance(res, dict)
        assert all(isinstance(k, int) for k in res)          # ключи — годы (int)
        assert all(isinstance(v, int) for v in res.values())
        assert list(res.keys()) == self._asc(res.keys())     # по годам ВОЗРАСТ.

    def test_dist_by_rating(self):
        rm = Ratings(self.ratings).Movies(self.ratings, self.movies)
        res = rm.dist_by_rating()
        assert isinstance(res, dict)
        assert all(isinstance(k, float) for k in res)        # ключи — оценки (float)
        assert all(isinstance(v, int) for v in res.values())
        assert list(res.keys()) == self._asc(res.keys())     # по оценкам ВОЗРАСТ.

    def test_top_by_num_of_ratings(self):
        rm = Ratings(self.ratings).Movies(self.ratings, self.movies)
        res = rm.top_by_num_of_ratings(10)
        assert isinstance(res, dict)
        assert len(res) <= 10
        assert all(isinstance(k, str) for k in res)          # названия фильмов (str)
        assert all(isinstance(v, int) for v in res.values())
        assert list(res.values()) == self._desc(res.values())

    def test_top_by_ratings(self):
        rm = Ratings(self.ratings).Movies(self.ratings, self.movies)
        res = rm.top_by_ratings(10)
        assert isinstance(res, dict)
        assert len(res) <= 10
        assert all(isinstance(k, str) for k in res)
        assert all(isinstance(v, float) for v in res.values())
        assert all(round(v, 2) == v for v in res.values())   # округлено до 2 знаков
        assert list(res.values()) == self._desc(res.values())

    def test_top_by_ratings_median(self):
        rm = Ratings(self.ratings).Movies(self.ratings, self.movies)
        res = rm.top_by_ratings(10, metric=median)
        assert isinstance(res, dict)
        assert all(isinstance(k, str) for k in res)
        assert all(round(v, 2) == v for v in res.values())
        assert list(res.values()) == self._desc(res.values())

    def test_top_controversial(self):
        rm = Ratings(self.ratings).Movies(self.ratings, self.movies)
        res = rm.top_controversial(10)
        assert isinstance(res, dict)
        assert len(res) <= 10
        assert all(isinstance(v, float) for v in res.values())
        assert all(round(v, 2) == v for v in res.values())
        assert list(res.values()) == self._desc(res.values())

    def test_users_dist_by_num_of_ratings(self):
        ru = Ratings(self.ratings).Users(self.ratings, self.movies)
        res = ru.dist_by_num_of_ratings()
        assert isinstance(res, dict)
        assert all(isinstance(k, int) for k in res)
        assert all(isinstance(v, int) for v in res.values())
        assert list(res.keys()) == self._asc(res.keys())

    def test_users_dist_by_avg_rating(self):
        ru = Ratings(self.ratings).Users(self.ratings, self.movies)
        res = ru.dist_by_avg_rating()
        assert isinstance(res, dict)
        assert all(isinstance(k, float) for k in res)
        assert all(isinstance(v, int) for v in res.values())
        assert all(round(k, 2) == k for k in res)
        assert list(res.keys()) == self._asc(res.keys())

    def test_users_top_controversial(self):
        ru = Ratings(self.ratings).Users(self.ratings, self.movies)
        res = ru.top_controversial_users(10)
        assert isinstance(res, dict)
        assert len(res) <= 10
        assert all(isinstance(k, str) for k in res)
        assert all(isinstance(v, float) for v in res.values())
        assert all(round(v, 2) == v for v in res.values())
        assert list(res.values()) == self._desc(res.values())
```

## Пояснение ключевых приёмов в тестах

| приём | смысл |
|---|---|
| `all(isinstance(x, T) for x in coll)` | True, если КАЖДЫЙ элемент коллекции — тип T |
| `all(... for x in coll)` | генераторное выражение → передаётся в `all` |
| `list(res.values()) == self._desc(res.values())` | значения равны отсортированным по убыванию |
| `list(res.keys()) == self._asc(res.keys())` | ключи отсортированы возрастающе |
| `round(v, 2) == v` | значение уже округлено до 2 знаков (проверка `round(..., 2)`) |
| `len(res) <= 10` | топ не длиннее запрошенного n |
| `assert average([1,2,3]) == 2.0` | тест утилиты на вручную посчитанном ответе |

## Тесты утилит — почему они с конкретными числами
`average([1,2,3]) == 2.0`, `median([1,2,3,4]) == 2.5`, `variance([1,3]) == 1.0` — это «эталонные» значения, посчитанные руками (см. определение). Так проверяется **базовая корректность вычислений** — не только тип/сортировка, но и правильный результат (README глава V, бонус: «вручную посчитай результаты»).

## Как запускать
```
cd ~/projects/DSB6_MovieLens_Analytics_ID_1577649-.../src/DSB6    # папка venv
./bin/python -m pytest ../movielens_analysis.py -v
```
Ожидаемый результат: `15 passed`.

## Итог по тестам в проекте
- [x] класс `Tests` в `movielens_analysis.py` (требование README)
- [x] тест на КАЖДЫЙ метод Movies + Ratings (тип возврата, типы элементов, сортировка)
- [x] тесты на утилиты `average` / `median` / `variance` с эталонными ответами
- [x] `15 passed` при запуске
- [ ] тесты на классы `Tags`/`Links` — зона друга (Разработчик Б)