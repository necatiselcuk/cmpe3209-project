# cmpe3209-project

CMPE3209 Computer Organization term project: from C to silicon (RV32IM)

Necati Selçuk, 5001240039 — G2 Sınav notu dağılımı

- `main.c`: C kaynak kodu
- `main_rars.s`: gcc -O0 çıktısının RARS 1.6 için uyarlanmış hali (değişiklikler dosya başında)
- `asm_O0.s`, `asm_O1.s`: gcc 16.1.0 ham assembly çıktıları (-O0 / -O1, M2)
- `screenshots/`: RARS ekran görüntüleri (`m1_*`: program çıktıları, `m2_enc_*`: machine code doğrulaması)
- `tutanak/`: proje teslim tutanağı (her aşamanın PDF ve Word hali)
- `objdump_O0.txt`: -O0 nesne dosyasının objdump -d çıktısı