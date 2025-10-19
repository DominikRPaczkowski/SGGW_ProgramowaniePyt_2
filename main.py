import os

OUTPUT_DIR = "app"
os.makedirs(OUTPUT_DIR, exist_ok=True)
FILE_PATH_2 = os.path.join(OUTPUT_DIR, "output_2.txt")
FILE_PATH_3 = os.path.join(OUTPUT_DIR, "output_3.txt")


# =================================================================
# 1. Klasa Logger (Punkt 1.1)
# =================================================================

class Logger:
    def __enter__(self):
        print("[Logger] Start sekcji logowania")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("[Logger] Koniec sekcji logowania")
        return False


# =================================================================
# 2. Klasa FileWriter (Punkt 1.2)
# =================================================================

class FileWriter:

    def __init__(self, filepath):
        self.filepath = filepath
        self.file_handle = None

    def __enter__(self):
        print(f"[{self.__class__.__name__}] Otwieram plik: {self.filepath}")
        self.file_handle = open(self.filepath, 'w', encoding='utf-8')
        return self.file_handle

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file_handle:
            print(f"[{self.__class__.__name__}] Zamykam plik: {self.filepath}")
            self.file_handle.close()

        return False


# =================================================================
# 3. Klasa RobustFileWriter (Punktu 1.3)
# =================================================================

class RobustFileWriter:
    def __init__(self, filepath):
        self.filepath = filepath
        self.file_handle = None

    def __enter__(self):
        print(f"[{self.__class__.__name__}] Otwieram plik: {self.filepath}")
        self.file_handle = open(self.filepath, 'w', encoding='utf-8')
        return self.file_handle

    def __exit__(self, exc_type, exc_val, exc_tb):

        if self.file_handle:
            print(f"[{self.__class__.__name__}] Zamykam plik: {self.filepath}")
            self.file_handle.close()

        if exc_type is not None:
            print(f"Błąd podczas zapisu: <{exc_val}>")

        return False


# =================================================================
# 4. Klasa SafeDivision (Punkt 1.4)
# =================================================================

class SafeDivision:
    def __enter__(self):
        print(f"[{self.__class__.__name__}] Wchodzę do kontekstu SafeDivision.")
        return self

    def divide(self, a, b):
        print(f"[{self.__class__.__name__}] Próba dzielenia {a} przez {b}...")
        return a / b

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ZeroDivisionError:
            print("[SafeDivision] Nie można dzielić przez zero")
            return True
        
        print(f"[{self.__class__.__name__}] Wychodzę z kontekstu. Typ wyjątku: {exc_type}")
        return False


# =================================================================
# --- TESTOWANIE WSZYSTKICH KLAS ---
# =================================================================

def run_all_tests():
    print("=====================================================")
    print("           TESTOWANIE WSZYSTKICH KLAS")
    print("=====================================================")

    print("\n--- TEST 1: Klasa Logger (Pomyślny) ---")
    with Logger():
        print("Operacja w środku bloku Logger.")

    print("\n--- TEST 1.1: Klasa Logger (Z wyjątkiem) ---")
    try:
        with Logger():
            print("Operacja w środku bloku Logger, rzucam wyjątek...")
            raise ValueError("Błąd testowy dla Loggera")
    except ValueError as e:
        print(f"Wyjątek przechwycony po bloku Logger: {e}")

    print("\n--- TEST 2: Klasa FileWriter (Zapis pomyślny) ---")
    try:
        with FileWriter(FILE_PATH_2) as f:
            f.write("Zawartość dla FileWriter.\n")
        
        with open(FILE_PATH_2, 'r', encoding='utf-8') as f:
            print(f"Zapisana zawartość ({FILE_PATH_2}): {f.read().strip()}")
    except Exception as e:
        print(f"Błąd podczas testu FileWriter: {e}")

    print("\n--- TEST 3: Klasa RobustFileWriter (Z wyjątkiem) ---")
    try:
        with RobustFileWriter(FILE_PATH_3) as f:
            f.write("Ta linia może się zapisać.\n")
            print("Rzucam błąd, aby sprawdzić komunikat i brak stłumienia...")
            raise IOError("Błąd zapisu pliku")
    except IOError as e:
        print(f"Wyjątek przechwycony po bloku RobustFileWriter: {e} (Sukces: komunikat Błąd podczas zapisu został wyświetlony i wyjątek nie stłumiony).")

    print("\n--- TEST 4: Klasa SafeDivision (Dzielenie przez zero - stłumienie) ---")
    try:
        with SafeDivision() as sd:
            sd.divide(5, 0)
        print("Po bloku SafeDivision (ZeroDivisionError stłumiony).")
    except Exception as e:
        print(f"Błąd! Wyjątek ZeroDivisionError nie został stłumiony: {e}")

    print("\n--- TEST 4.1: Klasa SafeDivision (Inny wyjątek - brak stłumienia) ---")
    try:
        with SafeDivision() as sd:
            sd.divide(10, "A")
    except TypeError as e:
        print(f"Wyjątek przechwycony po bloku SafeDivision: {e} (Sukces: inny wyjątek nie stłumiony).")


if __name__ == "__main__":
    run_all_tests()
