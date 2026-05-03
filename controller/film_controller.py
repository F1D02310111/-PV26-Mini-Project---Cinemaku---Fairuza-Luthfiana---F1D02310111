from database.db import add_film, update_film, delete_film, get_all_films

def load_films():
    return get_all_films()

def save_film(judul, genre, sutradara, tahun, rating, catatan):
    if not judul or not genre or not sutradara or not tahun or not rating:
        return False, "Semua field wajib diisi!"
    try:
        tahun = int(tahun)
    except ValueError:
        return False, "Tahun harus berupa angka!"
    add_film(judul, genre, sutradara, tahun, rating, catatan)
    return True, "Film berhasil ditambahkan."

def edit_film(id, judul, genre, sutradara, tahun, rating, catatan):
    if not judul or not genre or not sutradara or not tahun or not rating:
        return False, "Semua field wajib diisi!"
    try:
        tahun = int(tahun)
    except ValueError:
        return False, "Tahun harus berupa angka!"
    update_film(id, judul, genre, sutradara, tahun, rating, catatan)
    return True, "Film berhasil diperbarui."

def remove_film(id):
    delete_film(id)
    return True, "Film berhasil dihapus."
