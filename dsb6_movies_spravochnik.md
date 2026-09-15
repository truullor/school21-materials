# DSB6 — Справочник: класс Movies

## Данные (movies.csv)
```
header: movieId, title, genres
row:    ['1', 'Toy Story (1995)', 'Adventure|Animation|Children|Comedy|Fantasy']
```
В `self.rows` каждая запись — список строк:
- `row[0]` = movieId ('1')
- `row[1]` = название с годом в скобках ('Toy Story (1995)')
- `row[2]` = жанры через `|` ('Adventure|Animation|...')

## Класс
```python
class Movies(BaseDataset):
```
Наследует `BaseDataset` → при создании `Movies(path)` автоматически заполняется `self.rows` (первые 1000 фильмов). Свой `__init__` НЕ пишем.

## Методы

### 1. `dist_by_release()` — распределение фильмов по годам
**Ввод/вывод:** `{год: количество фильмов}`, сортировка по количеству — УБЫВАНИЕ.

```python
def dist_by_release(self):
    release_years = {}
    for row in self.rows:
        m = re.search(r'\((\d{4})\)', row[1])   # ищем "(4 цифры)" в названии
        if m:
            year = int(m.group(1))              # достаём год как число
            release_years[year] = release_years.get(year, 0) + 1
    return dict(sorted(release_years.items(), key=lambda x: x[1], reverse=True))
```

Ключевые приёмы:
- `re.search(r'\((\d{4})\)', title)` — регэксп вытаскивает год из названия (`\(` скобка, `(\d{4})` группа из 4 цифр, `\)` скобка). `match.group(1)` = символы группы.
- `if m:` — если года в названии нет (`None`), фильм пропускаем.
- `int(...)` — строка '1995' → число 1995 (чтобы сортировка была числовой, а не по алфавиту).
- `dict.get(year, 0) + 1` — счётчик: если ключа нет, берём 0 и +1 (без ошибки KeyError).
- `sorted(items, key=lambda x: x[1], reverse=True)` — сортировка пар по значению (количество), убывание.

Пример результата: `{1995: 224, 1994: 184, 1996: 181, ...}`

### 2. `dist_by_genres()` — распределение фильмов по жанрам
**Ввод/вывод:** `{жанр: количество}`, сортировка по количеству — УБЫВАНИЕ.

```python
def dist_by_genres(self):
    genres_count = {}
    for row in self.rows:
        genres = row[2].split("|")              # жанры -> список
        for g in genres:
            genres_count[g] = genres_count.get(g, 0) + 1
    return dict(sorted(genres_count.items(), key=lambda x: x[1], reverse=True))
```

Ключевое отличие от `dist_by_release`: у фильма НЕСКОЛЬКО жанров. Поэтому:
- `row[2].split("|")` разбивает строку жанров на список: `['Adventure', 'Animation', 'Children', ...]`;
- второй цикл `for g in genres` засчитывает КАЖДЫЙ жанр фильма;
- из-за этого сумма значений = 2219 (больше, чем фильмов 1000 — каждый может быть в нескольких жанрах).

### 3. `most_genres(n)` — топ-n фильмов по числу жанров
**Ввод/вывод:** `{название: число жанров}`, сортировка — УБЫВАНИЕ, только первые n.

```python
def most_genres(self, n):
    genres_count = {}
    for row in self.rows:
        genres_count[row[1]] = len(row[2].split("|"))   # название -> сколько жанров
    return dict(sorted(genres_count.items(), key=lambda x: x[1], reverse=True)[:n])
```

Новые приёмы:
- `len(list)` — считаем элементы после `split("|")` = число жанров;
- `[:n]` — срез отсортированного списка пар: берём первые n (топ);
- ключ — `row[1]` (название фильма целиком), значение — число жанров.

Пример: `Movies('movies.csv').most_genres(5)` вернёт 5 фильмов с самым большим числом жанров.

## Общие приёмы в классе Movies
1. `dict.get(key, 0) + 1` — счётчик без KeyError
2. `dict(sorted(d.items(), key=lambda x: x[1], reverse=True))` — сортировка по значению
3. `[:n]` — срез до топ-n
4. `row[1].split("|")` — жанры в список; `len(...)` — сколько штук
5. `re.search(r'\((\d{4})\)', ...)` — вытащить год из названия
6. `int()` — строка → число (важно для сортировки лет)

## Тест на понимание

```python
movies = Movies('ml-latest-small/movies.csv')
print(movies.dist_by_release())
print(movies.most_genres(3))
```

Предскажи: что будет первым годом? сколько фильмов в `most_genres(3)`?
(Ответ: первый год — 1995 (224 фильма); в most_genres(3) ровно 3 фильма с самым большим числом жанров.)