# DSB6 — Обзор проекта (MovieLens Analytics)

## Что это
Групповой проект: подготовить аналитический отчёт по данным MovieLens (400 тыс. оценок фильмов).
Работаем ВДВОЁМ (ты + друг Azamat / «кент»), каждый делает свою часть, потом объединяем.

## Роли
- **Ты — Разработчик А** (ветка `trullors`):
  - классы `Movies` и `Ratings` (+ тесты PyTest)
  - общие утилиты (чтение CSV) — согласуешь с Б
  - разделы отчёта, где используются Movies и Ratings
  - интеграция — проверяешь, что все методы задействованы
- **Друг — Разработчик Б** (ветка `sabretsa`):
  - классы `Tags` и `Links` (+ тесты PyTest)
  - разделы отчёта по тегам и IMDB-ссылкам

## Итоговые файлы (результат к сдаче — 2 файла, обе в `src/`)
1. `src/movielens_analysis.py` — модуль: классы с методами + класс Tests
2. `src/movielens_report.ipynb` — Jupyter-отчёт, собранный ТОЛЬКО из модуля

## Данные (лежат в `src/ml-latest-small/`)
| файл | колонки | что внутри |
|---|---|---|
| `movies.csv` | movieId, title, genres | фильмы, жанры через `\|` |
| `ratings.csv` | userId, movieId, rating, timestamp | оценки 0.5–5.0, время в Unix |
| `tags.csv` | userId, movieId, tag, timestamp | теги пользователей |
| `links.csv` | movieId, imdbId, tmdbId | ссылки на IMDB/TMDb |

- Rating = 0.5…5.0 (шаг 0.5)
- В названиях могут быть запятые в кавычках: `"American President, The (1995)"` — поэтому нужен честный парсер CSV, а не `split(",")`.
- В tags бывают кавычки как текст: `""artsy""` → `artsy`.
- По README: **берём первые 1000 записей** каждого файла.

## Git-правило (главное!)
> «Всегда делай push ТОЛЬКО в ветку develop! Ветка master будет проигнорирована. Работай в директории src.»

- Сдаём только то, что в `develop`.
- Сами файлы проекта лежат в `src/`.

## Ссылка на репозиторий
`origin` → `git-ssh.21-school.ru:2222/students_repo/dratinim/DSB6_MovieLens_Analytics_ID_1577649-Team_TL_dratinim_f0de3639_292c_4c04-1.git`