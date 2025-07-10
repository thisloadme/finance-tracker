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

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Buat file `.env` dengan konfigurasi:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/finance_db
   REDIS_URL=redis://localhost:6379/0
   SECRET_KEY=your-secret-key-here
   ENVIRONMENT=development
   DEBUG=true
   ```

4. Setup database:
   ```bash
   # Buat database PostgreSQL
   createdb finance_db
   
   # Jalankan migration untuk membuat tabel
   python -m app.core.init_db
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

## Database Migration

### Inisialisasi Database
Script `python -m app.core.init_db` akan:
- Membuat tabel `user` untuk menyimpan data pengguna
- Membuat tabel `category` untuk kategori budget
- Membuat tabel `transaction` untuk transaksi keuangan
- Menggunakan `checkfirst=True` untuk mencegah error jika tabel sudah ada

### Struktur Tabel

#### Tabel User
- `user_id` - Primary key
- `role` - Role pengguna (default: "personal")
- `email` - Email pengguna (unique)
- `username` - Username (unique)
- `hashed_password` - Password yang di-hash
- `full_name` - Nama lengkap
- `is_active` - Status aktif (1=aktif, 0=nonaktif)
- `is_verified` - Status verifikasi email (1=terverifikasi, 0=belum)
- `token_reset_password` - Token untuk reset password
- `created_at` - Waktu pembuatan
- `updated_at` - Waktu update terakhir
- `deleted_at` - Soft delete timestamp

#### Tabel Category
- `category_id` - Primary key
- `user_id` - Foreign key ke user
- `name` - Nama kategori (max 100 karakter)
- `description` - Deskripsi kategori (max 500 karakter)
- `monthly_limit` - Limit budget bulanan (decimal 10,2)
- `is_active` - Status aktif (1=aktif, 0=nonaktif)
- `created_at` - Waktu pembuatan
- `updated_at` - Waktu update terakhir

#### Tabel Transaction
- `transaction_id` - Primary key
- `user_id` - Foreign key ke user
- `category_id` - Foreign key ke category (nullable)
- `type` - Tipe transaksi (income/expense)
- `amount` - Jumlah transaksi (decimal 10,2)
- `description` - Deskripsi transaksi (max 500 karakter)
- `date` - Tanggal transaksi
- `created_at` - Waktu pembuatan
- `updated_at` - Waktu update terakhir

### Reset Database (Development)
```bash
# Hapus dan buat ulang database
dropdb finance_db
createdb finance_db
python -m app.core.init_db
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

## Troubleshooting

### Database connection error
1. Periksa `DATABASE_URL` di file `.env`
2. Pastikan PostgreSQL berjalan
3. Periksa credentials database
4. Jalankan `python -m app.core.init_db` untuk membuat tabel

### Redis connection error
1. Periksa `REDIS_URL` di file `.env`
2. Pastikan Redis berjalan
3. Aplikasi akan tetap berjalan tanpa Redis (cache akan disabled)

### Authentication error
1. Pastikan user sudah register
2. Gunakan endpoint `/auth/login` untuk dapat token
3. Sertakan header `Authorization: Bearer YOUR_TOKEN` untuk endpoint yang memerlukan auth 