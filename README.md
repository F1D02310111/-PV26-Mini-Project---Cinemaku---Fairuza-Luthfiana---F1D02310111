# CatatFilm — Bioskop Pribadi

Aplikasi pencatatan film bioskop pribadi menggunakan PySide6 dan SQLite.

## Deskripsi
CatatFilm memungkinkan pengguna mencatat, mengelola, dan mencari koleksi film yang pernah ditonton, lengkap dengan genre, sutradara, tahun rilis, rating, dan catatan pribadi.

## Cara Menjalankan

```bash
pip install PySide6
python main.py
```

## Teknologi
- Python 3.10+
- PySide6 (GUI)
- SQLite (database lokal)
- QSS (styling eksternal)

## Struktur Project (SoC)
```
bioskop/
├── main.py                  # Entry point
├── database/
│   └── db.py                # Koneksi & operasi SQLite
├── controller/
│   └── film_controller.py   # Logika bisnis
├── ui/
│   ├── main_window.py       # Jendela utama
│   └── film_dialog.py       # Dialog tambah/edit
└── style/
    └── theme.qss            # Styling QSS
```
