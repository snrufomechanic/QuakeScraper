# -_- coding:utf-8 -_-

# QuakeScraper

## Bu Python paketi [T.C. İçişleri Bakanlığı Afet ve Acil Durum Yönetimi Başkanlığı (AFAD)](www.afad.gov.tr) resmi web sitesi üzerinden verilen parametrelere göre istenilen verileri çeker.

# Kurulum

---

```bash
pip install QuakeScraper
```

---

## Kullanım

```python
from QuakeScraper import fetch_earthquake_data, create_map_image

# Sorgu parametrelerinizi tanımlayın

start_year = "2023"
start_month = "01"
start_day = "01"
end_year = "2023"
end_month = "12"
end_day = "31"

# Deprem verilerini çekin ve bir DataFrame olarak kaydedin

earthquake_df = fetch_earthquake_data(start_year, start_month, start_day, end_year, end_month, end_day, output_type='DF')

# DataFrame'i konsolda görüntüleyin

print(earthquake_df.head())

# Harita üzerinde görüntüleyin

create_map_image(earthquake_df)
```

---

<h1> Parametreler  </h1>
- `start_year`, `start_month`, `start_day`: Sorgu döneminin başlangıç tarihi. <br>
- `end_year`, `end_month`, `end_day`: Sorgu döneminin bitiş tarihi. <br>

# fetch_earthquake_data() İçin İsteğe Bağlı Parametreler:

<center>

| Parametre       | Varsayılan Değer |
| --------------- | ---------------- |
| `min_latitude`  | 35.00            |
| `max_latitude`  | 42.00            |
| `min_longitude` | 26.00            |
| `max_longitude` | 45.00            |
| `min_magnitude` | 3.5              |
| `max_magnitude` | 9.0              |
| `min_depth`     | 0                |
| `max_depth`     | 500              |
| `output_type`   | 'DF'             |

</center>

| Çıktı Türleri | :                                                              |
| ------------- | -------------------------------------------------------------- |
| DF:           | Deprem verilerini bir DataFrame olarak döndürür.               |
| TXT:          | Ham verileri bir metin dosyasına kaydeder.                     |
| CSV:          | Ham verileri CSV formatına dönüştürür ve bir dosyaya kaydeder. |
