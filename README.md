# 🧠 AI Destekli Müşteri Yorum Analiz Sistemi

Türkçe müşteri yorumlarının duygu durumunu (Pozitif / Negatif) gerçek zamanlı olarak analiz eden, yapay zeka destekli bir sistem.

## Mimari

| Katman | Teknoloji |
|--------|-----------|
| Model | `azizbarank/distilbert-base-turkish-cased-sentiment` (Türkçe DistilBERT) |
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Güvenlik | API Key (`x-api-key` header) |

## Kurulum & Çalıştırma

### 1. Gerekli Paketleri Kur
```bash
pip install fastapi uvicorn transformers torch python-dotenv streamlit requests
```

### 2. Backend'i Başlat (Terminal 1)
```bash
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

### 3. Frontend'i Başlat (Terminal 2)
```bash
python -m streamlit run streamlit_app.py --server.port 8501
```

### 4. Tarayıcıda Aç
```
http://localhost:8501
```

## API Kullanımı

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -H "x-api-key: sentiment_analysis_secure_key_2026" \
  -d '{"text": "Ürün çok güzeldi, memnun kaldım!"}'
```

Yanıt:
```json
{"negative": 0.06, "positive": 0.94}
```

## API Key

`.env` dosyasında tanımlıdır:
```
API_KEY=sentiment_analysis_secure_key_2026
```

## Model Performansı

- Türkçe pozitif yorumlar → %90+ doğrulukla POZİTİF
- Türkçe negatif yorumlar → %70+ doğrulukla NEGATİF
- Türkçe karakterler (ü, ğ, ş, ı, ö, ç) tam desteklenir
