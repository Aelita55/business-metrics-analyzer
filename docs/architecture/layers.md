# Декомпозиция системы на компоненты (слоистая архитектура)

| Слой | Компоненты | Ответственность |
|---|---|---|
| **Presentation (API)** | `auth_controller`, `sales_controller`, `kpi_controller`, `reports_controller` | Обработка HTTP-запросов, валидация входных данных, вызов сервисов |
| **Application (Service Layer)** | `AuthService`, `SalesImportService`, `KpiService`, `ReportService`, `UserService` | Бизнес-сценарии, оркестрация домена и инфраструктуры |
| **Domain** | Модели: `Sale`, `Kpi`, `User`, `Report`; стратегии KPI; валидаторы | Бизнес-правила, не зависящие от инфраструктуры |
| **Infrastructure** | `SqlSaleRepository`, `SqlUserRepository`, `UnitOfWork`, `JwtProvider`, `ExcelReportGenerator`, `EmailNotifier` | Доступ к данным и внешним системам |

## Зависимости между слоями

- Presentation → Application (вызов сервисов)
- Application → Domain (использование моделей и стратегий)
- Application → Infrastructure (через интерфейсы репозиториев, UnitOfWork, провайдеров)
- Infrastructure → внешние системы (PostgreSQL, SMTP, файловое хранилище)

Правило: **зависимости направлены внутрь** — Domain не знает о Infrastructure и Presentation.
