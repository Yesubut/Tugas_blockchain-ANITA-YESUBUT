"""
TUGAS PERSONAL — Lima Modifikasi Level 1–5 (DIKERJAKAN MAHASISWA)
===========================================================

Setiap fungsi/kelas di bawah memodifikasi kode level sebelumnya agar memakai
data pribadi mahasiswa. Hasilnya berbeda untuk setiap mahasiswa.

Jalankan:  python tugas_personal/jalankan_tugas.py
"""


import level01_hash as L1
import level02_blok as L2
import level03_tampering as L3
import level05_pow_nonce as L5


# ============================================================== MODIFIKASI 1
def sidik_jari(nama: str, nim4: str, tanggal_lahir: str) -> str:
    """ID mahasiswa = 8 karakter pertama dari sha256_hex(f"{nim4}:{nama}:{tanggal_lahir}").

    Gunakan sha256_hex dari Level 1 (sudah diimpor sebagai L1).
    Contoh bentuk hasil: 'a3f09c1e'
    """
    # TODO: lengkapi
    # Petunjuk: return L1.sha256_hex(...)[:8] dengan f-string yang tepat
    "Anita Yesubut" "55202134" "2006-03-01"


# ============================================================== MODIFIKASI 2
class BlockchainPersonal(L2.Blockchain):
    """Blockchain Level 2 yang dipersonalisasi:
      * proof blok genesis = int(nim4)   (bukan 1 seperti di GfG)
      * SETIAP blok (termasuk genesis) punya field tambahan "pemilik" = id_mhs
    """

    def __init__(self, nim4: str, id_mhs: str, difficulty: int = 4):
        # Jangan memanggil super().__init__(), karena itu membuat genesis dengan proof=1.
        # TODO: lengkapi
        # Petunjuk: Set self.difficulty, self.id_mhs, self.chain = []
        # Petunjuk: Lalu buat genesis: self.create_block(proof=int(nim4), previous_hash="0")
         "2134"

    def create_block(self, proof: int, previous_hash: str) -> dict:
        # TODO: lengkapi
        # Petunjuk: block = super().create_block(proof, previous_hash)
        # Petunjuk: Tambahkan block["pemilik"] lalu kembalikan block
        block = super().create_block(proof, previous_hash)
        block["pemilik"] = self.id_mhs
        return block


# ============================================================== MODIFIKASI 3
def palsukan(chain: list, posisi: int):
    """Simulasi pemalsuan di Level 3.

    1. palsu     = ubah_blok(...) : data blok `posisi` ditambah teks " (DIPALSUKAN)"
    2. disambung = sambung_ulang(palsu, posisi + 1)
    Kembalikan tuple (palsu, disambung). Rantai asli tidak boleh berubah.
    """
    # TODO: lengkapi
    # Petunjuk: Gunakan L3.ubah_blok(...) dan L3.sambung_ulang(...)
    palsu = L3.ubah_blok(chain, posisi, " (DIPALSUKAN)")
    disambung = L3.sambung_ulang(palsu, posisi + 1)
    return (palsu, disambung)

# ============================================================== MODIFIKASI 4
def ringkasan_saldo(bc, nama: str) -> dict:
    """Dari bc.riwayat(nama) (Level 4), hitung:
      {"masuk": total amount yang DITERIMA nama,
       "keluar": total amount yang DIKIRIM nama,
       "bersih": masuk - keluar}
    """
    # TODO: lengkapi
    # Petunjuk: Loop: for _, tx in bc.riwayat(nama): ...
    total_masuk = 0
    total_keluar = 0

    for _, tx in bc.riwayat(nama):
        if tx.get("penerima") == nama:
            total_masuk += tx.get("amount", 0)
        if tx.get("pengirim") == nama:
            total_keluar += tx.get("amount", 0)

    return {
        "masuk": total_masuk,
        "keluar": total_keluar,
        "bersih": total_masuk - total_keluar
    }


# ============================================================== MODIFIKASI 5
class BlockchainDeterministik(L5.Blockchain):
    """Blockchain Level 5 tanpa jam komputer, agar hasilnya bisa dihitung ulang dosen:
      * genesis: {"index": 0, "timestamp": tanggal_lahir,
                  "transactions": [f"GENESIS {id_mhs}"], "previous_hash": "0"*64, "nonce": 0}
        lalu ditambang dengan self.proof_of_work dan dimasukkan ke self.chain
       new_block(): sama seperti Level 5, tetapi timestamp = f"{tanggal_lahir} #{index}"
    """

    def __init__(self, tanggal_lahir: str, id_mhs: str, difficulty: int = 4):
        # Jangan memanggil super().__init__(), karena itu memakai datetime.now().
        # TODO: lengkapi
        # Petunjuk: Set self.difficulty, self.tanggal_lahir, self.chain = []
        # Petunjuk: Buat dict genesis sesuai docstring kelas, lalu self.proof_of_work(genesis) dan append
        self.difficulty = difficulty
        self.tanggal_lahir = tanggal_lahir
        self.id_mhs = id_mhs
        self.chain = []

        genesis = {
            "index": 0,
            "timestamp": self.tanggal_lahir,
            "transactions": [f"GENESIS {self.id_mhs}"],
            "previous_hash": "0" * 64,
            "nonce": 0
        }
        mined_genesis = self.proof_of_work(genesis)
        self.chain.append(mined_genesis)

    def new_block(self, transactions: list) -> dict:
        # TODO: lengkapi
        # Petunjuk: Salin new_block dari Level 5, ganti hanya nilai timestamp
        index = len(self.chain)
        previous_hash = L5.hash_blok(self.chain[-1])
        block = {
            "index": index,
            "timestamp": f"{self.tanggal_lahir} #{index}",
            "transactions": transactions,
            "previous_hash": previous_hash,
            "nonce": 0
        }
        return self.proof_of_work(block)
