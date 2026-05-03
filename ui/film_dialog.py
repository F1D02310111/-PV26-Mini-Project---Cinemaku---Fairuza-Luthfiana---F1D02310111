from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox,
    QSpinBox, QTextEdit, QDialogButtonBox, QLabel, QVBoxLayout
)

GENRES = ["Action", "Drama", "Comedy", "Horror", "Romance", "Sci-Fi", "Thriller", "Animation", "Documentary"]
RATINGS = ["G", "PG", "PG-13", "R", "NC-17"]

class FilmDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Tambah Film" if data is None else "Edit Film")
        self.setMinimumWidth(380)
        self._build_ui(data)

    def _build_ui(self, data):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.setSpacing(10)

        self.input_judul = QLineEdit()
        self.input_judul.setPlaceholderText("Judul film...")

        self.input_genre = QComboBox()
        self.input_genre.addItems(GENRES)

        self.input_sutradara = QLineEdit()
        self.input_sutradara.setPlaceholderText("Nama sutradara...")

        self.input_tahun = QSpinBox()
        self.input_tahun.setRange(1900, 2100)
        self.input_tahun.setValue(2024)

        self.input_rating = QComboBox()
        self.input_rating.addItems(RATINGS)

        self.input_catatan = QTextEdit()
        self.input_catatan.setPlaceholderText("Catatan pribadi tentang film ini...")
        self.input_catatan.setMaximumHeight(80)

        form.addRow("Judul *", self.input_judul)
        form.addRow("Genre *", self.input_genre)
        form.addRow("Sutradara *", self.input_sutradara)
        form.addRow("Tahun *", self.input_tahun)
        form.addRow("Rating *", self.input_rating)
        form.addRow("Catatan", self.input_catatan)

        if data:
            self.input_judul.setText(data[1])
            self.input_genre.setCurrentText(data[2])
            self.input_sutradara.setText(data[3])
            self.input_tahun.setValue(data[4])
            self.input_rating.setCurrentText(data[5])
            self.input_catatan.setPlainText(data[6] or "")

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addLayout(form)
        layout.addWidget(buttons)

    def get_data(self):
        return {
            "judul": self.input_judul.text().strip(),
            "genre": self.input_genre.currentText(),
            "sutradara": self.input_sutradara.text().strip(),
            "tahun": str(self.input_tahun.value()),
            "rating": self.input_rating.currentText(),
            "catatan": self.input_catatan.toPlainText().strip(),
        }
