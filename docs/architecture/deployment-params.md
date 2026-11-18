# Параметры развёртывания Business Metrics Analyzer

| Узел | Образ / ПО | Ресурсы (CPU / RAM) | Назначение |
|---|---|---|---|
| Nginx | nginx:alpine | 0.5 CPU, 256 MB | Reverse proxy, TLS |
| App (API) | bma-api:latest | 1 CPU, 1 GB | API и бизнес-логика |
| PostgreSQL | postgres:16 | 2 CPU, 2 GB | Хранение данных о продажах и KPI |
| Redis | redis:7-alpine | 0.5 CPU, 512 MB | Кэш KPI |
| MinIO / S3 | minio/minio | 0.5 CPU, 512 MB | Хранение сгенерированных отчётов |
