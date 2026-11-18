# Интерфейсы компонентов Business Metrics Analyzer

| Компонент | Интерфейс | Ключевые методы |
|---|---|---|
| **KpiService** | `IKpiService` | `calculate_period(period) -> KpiResult`<br>`get_dashboard(period) -> DashboardDto` |
| **SalesImportService** | `ISalesImportService` | `import_csv(file) -> ImportResult`<br>`validate(records) -> ValidationResult` |
| **ReportService** | `IReportService` | `generate(report_type, period) -> ReportFile`<br>`export_excel(report_id) -> bytes` |
| **AuthService** | `IAuthService` | `authenticate(username, password) -> Token`<br>`refresh_token(token) -> Token` |
| **UserService** | `IUserService` | `get_user(user_id) -> UserDto`<br>`update_role(user_id, role) -> None` |
