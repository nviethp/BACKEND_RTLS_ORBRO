# BACKEND_RTLS_ORBRO

# TAG Backend System (In-Memory Version)

## Requirements
- Ubuntu 20.04+
- Python 3.9+

## Install
```bash
python -m venv venv
## # Windows
venv\Scripts\Activate.ps1
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt

### Chạy Backend
```bash
python main.py
```

- Server: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

### Chạy Tag Simulator
> Backend phải chạy trước
```bash
python tag_simulator.py
```

---

```

---

## 2. Phương thức giả lập (Simulation) Tag

### Định dạng dữ liệu TAG
```
TAG,<tag_id>,<cnt>,<timestamp>
```
Ví dụ:
```
TAG,fa451f0755d8,197,20240503140059.456
```

### Nguyên lý giả lập
- Tối thiểu 3 Tag ID
- Mỗi Tag có CNT ban đầu
- CNT tăng định kỳ (1 giây/lần)
- Gửi dữ liệu qua API:
```
POST /tag
```
Payload:
```json
{
  "raw_line": "TAG,fa451f0755d8,198,20240503140059.456"
}
```

> Chỉ Tag đã đăng ký (`POST /tags`) mới được cập nhật trạng thái.

---

## 3. Ví dụ kiểm thử API (curl)

### Health Check
```bash
curl http://localhost:8000/health
```

### Đăng ký Tag
```bash
curl -X POST http://localhost:8000/tags \
  -H "Content-Type: application/json" \
  -d '{"id":"fa451f0755d8","description":"Helmet Tag for worker A"}'
```

### Tag Data
```bash
curl -X POST http://localhost:8000/tag \
  -H "Content-Type: application/json" \
  -d '{"raw_line":"TAG,fa451f0755d8,198,20240503140059.456"}'
```

### Lấy danh sách Tag
```bash
curl http://localhost:8000/tags
```

### Tra cứu Tag đơn lẻ
```bash
curl http://localhost:8000/tag/fa451f0755d8
```

---

