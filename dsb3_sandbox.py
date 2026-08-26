# dsb3_sandbox.py — мини-песочница ООП для DSB3
# Запуск: python dsb3_sandbox.py
# Меняй код и смотри, что меняется. Это учебная игрушка, не часть проекта.

# --- Пример 1: класс + объект + метод ---
class Dog:
    def say(self):
        return "Гав!"


print(Dog().say())  # Гав!


# --- Пример 2: конструктор __init__ и self ---
class Dog:
    def __init__(self, name):
        self.name = name  # атрибут объекта

    def say(self):
        return f"{self.name}: Гав!"


print(Dog("Шарик").say())  # Шарик: Гав!


# --- Пример 3: вложенный класс (как в ex03) ---
class Research:
    def file_reader(self):
        return [[0, 1], [1, 0], [0, 1]]

    class Calc:
        def counts(self, data):
            heads = sum(row[0] for row in data)
            tails = sum(row[1] for row in data)
            return heads, tails


r = Research()
print(Research.Calc().counts(r.file_reader()))  # (1, 2)


# --- Пример 4: наследование (как в ex04) ---
class Base:
    def counts(self, data):
        return sum(data)


class Child(Base):
    def predict(self, n):
        return [1, 0, 1][:n]


c = Child()
print(c.counts([1, 0, 1]))  # 2  (метод взят от Base)
print(c.predict(2))         # [1, 0]
