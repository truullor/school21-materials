# dsb3_tracer.py — трассировка: что реально происходит при вызовах.
# Запуск: python3 dsb3_tracer.py

print("=== 1. ОПРЕДЕЛЕНИЕ КЛАССА (это просто ЧЕРТЁЖ, код ещё не выполняется) ===")


class Dog:
    def __init__(self, name):
        # self — это будущая коробка-объект. Python передаст её сюда сам.
        print(f"  [__init__] создаю объект self={self} (id={id(self)}), кладу в него имя '{name}'")
        self.name = name  # кладём данные ВНУТРЬ коробки

    def say(self):
        # тот же self, что и в __init__ — та же самая коробка
        print(f"  [say] меня вызвали на коробке self={self} (id={id(self)}), там лежит self.name='{self.name}'")
        return f"{self.name}: Гав!"


print("\n=== 2. СОЗДАНИЕ ОБЪЕКТА (Dog('Шарик')) ===")
d = Dog("Шарик")
print(f"  переменная d указывает на ту же коробку: d={d} (id={id(d)})")

print("\n=== 3. ВЫЗОВ МЕТОДА ЧЕРЕЗ ТОЧКУ (d.say()) ===")
print("  под капотом Python делает: Dog.say(d)  <- d становится self")
result = d.say()
print(f"  метод ВЕРНУЛ значение: {result!r}  (его и получила переменная result)")

print("\n=== 4. МЕТОД МЕНЯЕТ ДАННЫЕ В КОРОБКЕ (d.rename) ===")


def rename(self, new_name):
    print(f"  [rename] self={self}, меняю имя внутри коробки")
    self.name = new_name


Dog.rename = rename  # приклеим метод к классу для наглядности
d.rename("Бобик")
print(f"  теперь d.say() -> {d.say()!r}  (имя сохранилось в коробке!)")

print("\n=== 5. ДВА ОБЪЕКТА — У КАЖДОГО СВОЯ КОРОБКА ===")
d2 = Dog("Рекс")
print(f"  d.say()  -> {d.say()!r}   (у d имя 'Бобик')")
print(f"  d2.say() -> {d2.say()!r}  (у d2 имя 'Рекс')")

print("\n=== 6. ЦЕПОЧКА ВЫЗОВОВ (obj.m1().m2()) ===")
# вернём объект из одного метода и сразу вызовем другой на нём:
class Box:
    def give(self):
        return self  # возвращает саму коробку
    def shout(self):
        return "я коробка!"


print(f"  Box().give().shout() -> {Box().give().shout()!r}")
print("  Box() -> коробка; .give() -> та же коробка; .shout() -> вызван на ней")
