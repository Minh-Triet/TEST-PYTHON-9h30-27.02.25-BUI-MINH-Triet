@echo off
docker run -d ^
  --name my-postgres ^
  -e POSTGRES_USER=postgres ^
  -e POSTGRES_PASSWORD=123300 ^
  -e POSTGRES_DB=sales_db ^
  -p 5432:5432 ^
  -v postgres_data:/var/lib/postgresql/data ^
  postgres