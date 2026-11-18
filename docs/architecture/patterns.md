# Паттерны проектирования в Business Metrics Analyzer

## 1. Таблица выбора паттернов

| Паттерн | Где применяется | Обоснование | Альтернативы |
|---|---|---|---|
| Repository | Слой доступа к данным о продажах | Изоляция бизнес-логики от SQLAlchemy, облегчает тестирование | Прямые запросы к ORM |
| Unit of Work | Импорт данных и транзакции | Атомарность операций, откат при ошибках | Ручное управление транзакциями |
| Service Layer | Расчёт KPI, формирование отчётов | Инкапсуляция бизнес-сценариев | Логика в контроллерах |
| Factory | Создание отчётов разных типов | Гибкое расширение типов отчётов | Условные операторы |
| Strategy | Различные методы расчёта KPI | Взаимозаменяемость алгоритмов | Жёстко заданные методы |
| DTO | Передача данных API | Чёткие контракты, версионирование API | Сырые ORM-модели |
| Adapter | Интеграция с 1С / SMTP | Изоляция внешних зависимостей | Прямые вызовы |
| Observer | Обновление дашборда | Реакция на изменение данных | Периодический опрос |

## 2. Примеры реализации на Python

### Пример 1: Repository + Unit of Work

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class SaleRecord:
    id: int | None
    month: str
    revenue: Decimal
    cost: Decimal


class SaleRepository(ABC):
    @abstractmethod
    def add(self, record: SaleRecord) -> None: ...

    @abstractmethod
    def get_by_period(self, period: str) -> list[SaleRecord]: ...


class SqlSaleRepository(SaleRepository):
    def __init__(self, session):
        self.session = session

    def add(self, record: SaleRecord) -> None:
        self.session.add(record)

    def get_by_period(self, period: str) -> list[SaleRecord]:
        return self.session.query(SaleRecord).filter_by(month=period).all()


class UnitOfWork:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.sales = SqlSaleRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.session.close()
```

### Пример 2: Strategy для расчёта KPI

```python
from abc import ABC, abstractmethod


class KpiStrategy(ABC):
    @abstractmethod
    def calculate(self, revenue: float, cost: float) -> float: ...


class ProfitabilityStrategy(KpiStrategy):
    def calculate(self, revenue: float, cost: float) -> float:
        return 0.0 if revenue == 0 else (revenue - cost) / revenue * 100


class AverageCheckStrategy(KpiStrategy):
    def calculate(self, revenue: float, orders: int) -> float:
        return 0.0 if orders == 0 else revenue / orders
```

## 3. Результат выполнения (демонстрация в Google Colab)

```
============================================================
Repository + Unit of Work
============================================================
[+] Добавлена запись: SaleRecord(id=1, month='2026-01', revenue=Decimal('1000'), cost=Decimal('600'))
[OK] commit() выполнен. В БД записей: 1

[+] Добавлена запись: SaleRecord(id=2, month='2026-02', revenue=Decimal('2000'), cost=Decimal('1500'))
[!!] Имитация ошибки при импорте
[ROLLBACK] Отменено. В БД записей: 1 (старая осталась)

[READ] Записи за 2026-01: [SaleRecord(id=1, month='2026-01', revenue=Decimal('1000'), cost=Decimal('600'))]

============================================================
Strategy для расчёта KPI
============================================================
Входные данные: выручка=1000.0, себестоимость=600.0, заказов=50
Рентабельность:  40.0%
Средний чек:     20.0
```

## 4. Пояснения

**Repository + Unit of Work.** Паттерн Repository задаёт абстрактный интерфейс доступа к данным (`SaleRepository`), а реализация `SqlSaleRepository` инкапсулирует работу с SQLAlchemy. Unit of Work управляет жизненным циклом транзакции: при успешном выходе из блока `with` выполняется `commit()`, при исключении — `rollback()`. Это обеспечивает атомарность операций импорта больших объёмов данных (реализация драйвера AD-03).

**Strategy.** Абстрактный класс `KpiStrategy` задаёт интерфейс `calculate()`. Конкретные стратегии `ProfitabilityStrategy` (рентабельность) и `AverageCheckStrategy` (средний чек) реализуют различные формулы расчёта. Добавление новой метрики не требует изменения кода сервиса (принцип Open/Closed).
