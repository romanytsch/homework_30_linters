# ERRORS.MD

## Ошибка 1: Неверный расчёт возраста в методе get_age

В исходном коде метод get_age рассчитывал возраст как разницу между годом рождения и текущим 
годом, что даёт отрицательные значения.

Исходный код:

    def get_age(self) -> int:
        now: datetime.datetime = datetime.datetime.now()
        return self.yob - now.year

Исправленный код:

    def get_age(self) -> int:
        now: datetime.datetime = datetime.datetime.now()
        return now.year - self.yob

---

## Ошибка 2: Метод set_name не меняет имя

В методе set_name значение имени не присваивается переданному параметру, а само себе.

Исходный код:

    def set_name(self, name: str) -> None:
        self.name = self.name

Исправленный код:

    def set_name(self, name: str) -> None:
        self.name = name

---

## Ошибка 3: Метод set_address неправильно задаёт адрес

В методе set_address используется оператор сравнения вместо присваивания.

Исходный код:

    def set_address(self, address: str) -> None:
        self.address == address

Исправленный код:

    def set_address(self, address: str) -> None:
        self.address = address

---

## Ошибка 4: Метод is_homeless всегда возвращает False

Метод проверяет несуществующую переменную address вместо self.address и неправильно 
проверяет пустоту адреса.

Исходный код:

    def is_homeless(self) -> bool:
        return address is None

Исправленный код:

    def is_homeless(self) -> bool:
        return not self.address
