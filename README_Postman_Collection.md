# Personal Finance API - Postman Collection

## Overview
Collection Postman ini berisi semua endpoint untuk Personal Finance API dengan contoh payload, header, dan parameter yang diperlukan.

## Setup

### 1. Import Collection
1. Buka Postman
2. Klik "Import" 
3. Pilih file `Personal_Finance_API.postman_collection.json`
4. Collection akan muncul di sidebar

### 2. Setup Environment Variables
Setelah import, setup environment variables:

1. Klik kanan pada collection → "Edit"
2. Pilih tab "Variables"
3. Update nilai berikut:
   - `base_url`: `http://127.0.0.1:8000` (atau URL server Anda)
   - `access_token`: Akan diisi otomatis setelah login

## Struktur Collection

### 1. Health Check
- **Root Endpoint** (`GET /`): Cek status API
- **Health Check** (`GET /health`): Health check endpoint

### 2. Authentication
- **Register User** (`POST /auth/register`): Daftar user baru
- **Login** (`POST /auth/login`): Login dan dapatkan token
- **Refresh Token** (`POST /auth/refresh`): Refresh access token
- **Request Password Reset** (`POST /auth/password-reset-request`): Request reset password
- **Confirm Password Reset** (`POST /auth/password-reset-confirm`): Konfirmasi reset password
- **Get Current User** (`GET /auth/me`): Dapatkan info user yang login

### 3. Users
- **Get Current User** (`GET /api/v1/users/me`): Dapatkan info user
- **Update Current User** (`PUT /api/v1/users/me`): Update info user
- **Delete Current User** (`DELETE /api/v1/users/me`): Hapus akun user

### 4. Budget Categories
- **Get All Budget Categories** (`GET /api/v1/budget-categories`): Dapatkan semua kategori budget
- **Create Budget Category** (`POST /api/v1/budget-categories`): Buat kategori budget baru
- **Get Budget Category by ID** (`GET /api/v1/budget-categories/{id}`): Dapatkan kategori budget berdasarkan ID
- **Update Budget Category** (`PUT /api/v1/budget-categories/{id}`): Update kategori budget
- **Delete Budget Category** (`DELETE /api/v1/budget-categories/{id}`): Hapus kategori budget
- **Get Budget Category Usage** (`GET /api/v1/budget-categories/{id}/usage`): Dapatkan penggunaan budget

### 5. Transactions
- **Get All Transactions** (`GET /api/v1/transactions`): Dapatkan semua transaksi dengan filter
- **Create Transaction** (`POST /api/v1/transactions`): Buat transaksi baru
- **Get Transaction by ID** (`GET /api/v1/transactions/{id}`): Dapatkan transaksi berdasarkan ID
- **Update Transaction** (`PUT /api/v1/transactions/{id}`): Update transaksi
- **Delete Transaction** (`DELETE /api/v1/transactions/{id}`): Hapus transaksi
- **Get Monthly Summary** (`GET /api/v1/transactions/summary/monthly`): Dapatkan ringkasan bulanan

## Cara Penggunaan

### 1. Setup Awal
1. Pastikan server API berjalan di `http://127.0.0.1:8000`
2. Test endpoint "Root Endpoint" untuk memastikan API berjalan

### 2. Register dan Login
1. Jalankan "Register User" dengan data yang valid
2. Jalankan "Login" dengan username dan password yang sudah didaftarkan
3. Copy `access_token` dari response login
4. Update variable `access_token` di collection dengan token yang didapat

### 3. Testing Endpoint
Setelah login, Anda bisa test semua endpoint yang memerlukan authentication.

## Contoh Payload

### Register User
```json
{
  "email": "user@example.com",
  "username": "testuser",
  "full_name": "Test User",
  "password": "password123"
}
```

### Login
```json
{
  "username": "testuser",
  "password": "password123"
}
```

### Create Budget Category
```json
{
  "name": "Makanan",
  "description": "Pengeluaran untuk makanan sehari-hari",
  "monthly_limit": 1000000,
  "color": "#FF6B6B"
}
```

### Create Transaction
```json
{
  "type": "expense",
  "amount": 50000,
  "description": "Makan siang di warung",
  "date": "2024-12-15T12:30:00Z",
  "category_id": 1
}
```

## Query Parameters

### Get All Transactions
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100, max: 100)
- `category_id`: Filter by category ID (optional)
- `transaction_type`: Filter by type - "income" or "expense" (optional)
- `start_date`: Filter by start date (YYYY-MM-DD) (optional)
- `end_date`: Filter by end date (YYYY-MM-DD) (optional)
- `search`: Search in description (optional)

### Get Budget Categories
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100, max: 100)

### Get Budget Usage
- `month`: Month (1-12) (required)
- `year`: Year (2020+) (required)

### Get Monthly Summary
- `month`: Month (1-12) (required)
- `year`: Year (2020+) (required)

## Response Examples

### Login Response
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Budget Category Response
```json
{
  "id": 1,
  "name": "Makanan",
  "description": "Pengeluaran untuk makanan sehari-hari",
  "monthly_limit": "1000000.00",
  "color": "#FF6B6B",
  "user_id": 1,
  "is_active": 1,
  "created_at": "2024-12-15T10:30:00Z",
  "updated_at": null
}
```

### Transaction Response
```json
{
  "id": 1,
  "type": "expense",
  "amount": "50000.00",
  "description": "Makan siang di warung",
  "date": "2024-12-15T12:30:00Z",
  "category_id": 1,
  "user_id": 1,
  "created_at": "2024-12-15T10:30:00Z",
  "updated_at": null
}
```

### Monthly Summary Response
```json
{
  "total_income": "5000000.00",
  "total_expenses": "3000000.00",
  "balance": "2000000.00",
  "month": "December",
  "year": 2024
}
```

## Error Handling

### Common Error Responses

#### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

#### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

#### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

#### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Tips Penggunaan

1. **Authentication**: Selalu pastikan `access_token` sudah diset sebelum test endpoint yang memerlukan auth
2. **Rate Limiting**: API memiliki rate limiting, jadi jangan spam request
3. **Data Validation**: Perhatikan format data yang dikirim (email, date, amount, dll)
4. **Error Handling**: Periksa response untuk memahami error yang terjadi
5. **Pagination**: Gunakan parameter `skip` dan `limit` untuk pagination

## Troubleshooting

### Token Expired
Jika mendapat error 401, refresh token dengan endpoint "Refresh Token"

### Server Not Running
Pastikan server berjalan dengan menjalankan:
```bash
uvicorn app.main:app --reload
```

### Database Issues
Pastikan database sudah disetup dan berjalan dengan benar

### CORS Issues
Jika ada masalah CORS, pastikan CORS middleware sudah dikonfigurasi dengan benar di server 