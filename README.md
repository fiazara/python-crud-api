
# Python CRUD API

Aplikasi Backend API sederhana menggunakan Python dan Docker.

## Features

- GET / : Menampilkan status API
- GET /health : Memeriksa kesehatan API
- GET /messages : Menampilkan seluruh pesan
- POST /messages : Menambahkan pesan
- DELETE /messages?index=0 : Menghapus pesan berdasarkan indeks

## Requirements

- Python 3.11
- Docker
- Docker Compose (opsional)

## Build Docker Image

```bash
docker build -t python-crud-api:manual .
```

## Run Container

```bash
docker run -d --name production-api-container -p 5000:5000 -v production-api-data:/var/lib/backend_data python-crud-api:manual
```

## Access API

http://localhost:5000

## Health Check

http://localhost:5000/health

## Messages

http://localhost:5000/messages

## Persistent Storage

Data disimpan menggunakan Docker Volume bernama `production-api-data`, sehingga data tetap tersedia meskipun container dihapus dan dibuat ulang.
