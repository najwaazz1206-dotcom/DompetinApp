import sqlite3

class Database:
    def __init__(self):
        self.db_name = "dompetin.db"
        self.create_tables()

    def create_tables(self):
        # Menggunakan 'with' agar koneksi otomatis ditutup setelah selesai
        with sqlite3.connect(self.db_name) as con:
            cursor = con.cursor()
            
            # Tabel User
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                )
            """)
            # Tabel Transaksi
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    type TEXT,
                    category TEXT,
                    amount INTEGER,
                    note TEXT,
                    date TEXT
                )
            """)
            # Tabel Budget
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS budgets(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    name TEXT,
                    amount INTEGER,
                    period TEXT
                )
            """)
            con.commit()

    # --- FITUR LOGIN/REGISTER ---
    def register_user(self, username, password):
        try:
            with sqlite3.connect(self.db_name) as con:
                cursor = con.cursor()

                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                               (username, password))

                con.commit()
                return True  

        except sqlite3.IntegrityError:
            return False  

    def login_user(self, username, password):
        with sqlite3.connect(self.db_name) as con:
            cursor = con.cursor()
            cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
            result = cursor.fetchone()
            return result[0] if result else None

    # --- FITUR TRANSAKSI ---
    def add_transaction(self, user_id, type, category, amount, note, date):
        with sqlite3.connect(self.db_name) as con:
            cursor = con.cursor()
            cursor.execute("INSERT INTO transactions (user_id, type, category, amount, note, date) VALUES (?, ?, ?, ?, ?, ?)",
                            (user_id, type, category, amount, note, date))
            con.commit()

    def get_summary(self, user_id):
        with sqlite3.connect(self.db_name) as con:
            cursor = con.cursor()
            # Pemasukan
            cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id=? AND type='pemasukan'", (user_id,))
            inc = cursor.fetchone()[0] or 0
            # Pengeluaran
            cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id=? AND type='pengeluaran'", (user_id,))
            exp = cursor.fetchone()[0] or 0
            
            return inc, exp, (inc - exp)

    def get_recent_transactions(self, user_id):
        with sqlite3.connect(self.db_name) as con:
            cursor = con.cursor()
            cursor.execute("""
                SELECT id, date, category, amount, type 
                FROM transactions 
                WHERE user_id=? 
                ORDER BY id DESC 
                LIMIT 5
            """, (user_id,))
            return cursor.fetchall()
    
    def delete_transaction(self, trans_id):
        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM transactions WHERE id=?", (trans_id,))
            con.commit()

    # --- FITUR BUDGETING ---
    def add_budget(self, user_id, name, amount, period):
        with sqlite3.connect(self.db_name) as con:
            cursor = con.cursor()
            cursor.execute("INSERT INTO budgets (user_id, name, amount, period) VALUES (?, ?, ?, ?)",
                            (user_id, name, amount, period))
            con.commit()

    def get_budgets(self, user_id):
        with sqlite3.connect(self.db_name) as con:
            cursor = con.cursor()
            cursor.execute("SELECT id, name, amount, period FROM budgets WHERE user_id=?", (user_id,))
            return cursor.fetchall()
    
        # --- DELETE BUDGET ---
    def delete_budget(self, budget_id, user_id):
        with sqlite3.connect(self.db_name) as con:
            cursor = con.cursor()

            # Pastikan budget milik user ini
            cursor.execute("SELECT id FROM budgets WHERE id=? AND user_id=?", (budget_id, user_id))
            result = cursor.fetchone()
            if not result:
                return False  # budget tidak ditemukan / bukan milik user

            cursor.execute("DELETE FROM budgets WHERE id=? AND user_id=?", (budget_id, user_id))
            con.commit()
            return True

    # --- FITUR OVERVIEW ---
    def get_budget_progress(self, user_id):
        with sqlite3.connect(self.db_name) as con:
            cursor = con.cursor()
            
            # 1. Ambil Budget
            cursor.execute("SELECT name, amount, period FROM budgets WHERE user_id=?", (user_id,))
            budgets = cursor.fetchall()
            
            summary_data = []
            
            for bud in budgets:
                b_name = bud[0]
                b_limit = bud[1]
                
                # 2. Hitung pengeluaran terkait
                cursor.execute("""
                    SELECT SUM(amount) FROM transactions 
                    WHERE user_id=? AND type='pengeluaran' AND category LIKE ?
                """, (user_id, f'%{b_name}%'))
                
                spent = cursor.fetchone()[0] or 0
                percent = (spent / b_limit) if b_limit > 0 else 0
                
                summary_data.append({
                    'name': b_name,
                    'limit': b_limit,
                    'spent': spent,
                    'percent': percent
                })
                
            return summary_data