# Personal Finance API

API untuk manajemen keuangan pribadi menggunakan FastAPI.

## Fitur

- ✅ Autentikasi JWT
- ✅ Manajemen user
- ✅ Manajemen budget
- ✅ Manajemen transaksi
- ✅ Rate limiting
- ✅ Caching dengan Redis
- ✅ Database PostgreSQL
- ✅ CORS support

## Instalasi

1. Clone repository ini
2. Buat virtual environment:
   ```bash
   python -m venv kedata
   ```

3. Aktifkan virtual environment:
   - Windows: `kedata\Scripts\activate`
   - Linux/Mac: `source kedata/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Buat file `.env` dengan konfigurasi:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/finance_db
   REDIS_URL=redis://localhost:6379/0
   SECRET_KEY=your-secret-key-here
   ENVIRONMENT=development
   DEBUG=true
   ```

## Menjalankan Aplikasi

### Cara 1: Menggunakan file run.py (Direkomendasikan)
```bash
python run.py
```

### Cara 2: Menggunakan uvicorn langsung
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Cara 3: Menggunakan script
- Windows: `run.bat`
- Linux/Mac: `./run.sh`

## Konfigurasi Host dan Port

Untuk menjalankan aplikasi di `0.0.0.0` (bisa diakses dari jaringan lain):

### Menggunakan Environment Variables:
```bash
export HOST=0.0.0.0
export PORT=8000
python run.py
```

### Menggunakan uvicorn langsung:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Di Windows:
```cmd
set HOST=0.0.0.0
set PORT=8000
python run.py
```

## Akses API

- **Local**: http://localhost:8000
- **Network**: http://[IP_ADDRESS]:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Endpoints

### Authentication
- `POST /auth/register` - Register user baru
- `POST /auth/login` - Login user
- `POST /auth/refresh` - Refresh token
- `GET /auth/me` - Get user info

### Users
- `GET /api/v1/users/` - Get semua users
- `GET /api/v1/users/{user_id}` - Get user by ID

### Budgets
- `GET /api/v1/budgets/` - Get semua budgets
- `POST /api/v1/budgets/` - Create budget baru
- `PUT /api/v1/budgets/{budget_id}` - Update budget
- `DELETE /api/v1/budgets/{budget_id}` - Delete budget

### Transactions
- `GET /api/v1/transactions/` - Get semua transactions
- `POST /api/v1/transactions/` - Create transaction baru
- `PUT /api/v1/transactions/{transaction_id}` - Update transaction
- `DELETE /api/v1/transactions/{transaction_id}` - Delete transaction

## Struktur Project

```
app/
├── api/           # API endpoints
├── core/          # Core functionality (database, security, cache)
├── crud/          # Database operations
├── models/        # SQLAlchemy models
├── schemas/       # Pydantic schemas
├── config.py      # Configuration settings
└── main.py        # FastAPI application
```

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black app/
isort app/
```

### Linting
```bash
flake8 app/
```

## Production Deployment

Untuk production, gunakan gunicorn:

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Troubleshooting

### Aplikasi tidak bisa diakses dari jaringan lain
1. Pastikan menggunakan `--host 0.0.0.0`
2. Periksa firewall settings
3. Pastikan port tidak diblokir

### Database connection error
1. Periksa `DATABASE_URL` di file `.env`
2. Pastikan PostgreSQL berjalan
3. Periksa credentials database

### Redis connection error
1. Periksa `REDIS_URL` di file `.env`
2. Pastikan Redis berjalan
3. Aplikasi akan tetap berjalan tanpa Redis (cache akan disabled) 