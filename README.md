# cmpe3209-project

CMPE3209 Computer Organization term project: from C to silicon (RV32IM)

Necati Selçuk, 5001240039 — G2 Sınav notu dağılımı

Etiketler: `M1` (Adım 0–1), `M2` (Adım 2), `final` (Adım 3–5)

## M1 ve M2
- `main.c`: C kaynak kodu
- `main_rars.s`: gcc -O0 çıktısının RARS 1.6 için uyarlanmış hali (değişiklikler dosya başında)
- `asm_O0.s`, `asm_O1.s`: gcc 16.1.0 ham assembly çıktıları (-O0 / -O1, M2)
- `objdump_O0.txt`: -O0 nesne dosyasının objdump -d çıktısı
- `screenshots/`: RARS ekran görüntüleri (`m1_*`: program çıktıları, `m2_enc_*`: machine code doğrulaması)
- `tutanak/`: proje teslim tutanağı (her aşamanın PDF ve Word hali)

## Final (Adım 3–5)
- `trace.csv`: -O0 programının tüm data load/store izi (1989 referans; sira,RW,adres_hex,boyut,c_satiri,stack_mi) — 4a
- `trace_sim.py`: `main_rars.s`'i RARS bellek yerleşimiyle çalıştırıp `trace.csv`'yi üretir
- `cache_sim.py`: LRU cache simülatörü; 4e tasarım uzayı (mapping ve line boyu serileri)
- `cache_log_rars.txt`: RARS Data Cache Simulator Runtime Log (1989 erişim) — 4d
- `cache_design_space.png`: 4e hit ratio grafiği
- `main_v2.c`, `asm_v2_O0.s`, `main_v2_rars.s`: 4g kod değişikliği (1. ve 2. döngü birleştirildi), godbolt -O0 çıktısı ve RARS uyarlaması
- `main_O1_rars.s`: -O1 çıktısının RARS 1.6 uyarlaması — 5a
- `screenshots/final_*`: 4d ve 4g cache sonuçları, 5a instruction istatistikleri (-O0 / -O1) ve -O1 cache sonucu

Çalıştırma (Python 3):
    python trace_sim.py main_rars.s trace.csv
    python cache_sim.py trace.csv