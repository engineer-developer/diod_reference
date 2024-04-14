import csv
import re
from pathlib import Path
import tkinter as tk
from tkinter import Label, Entry, Button, messagebox, scrolledtext


BASE_PATH = Path.cwd()
CSV_FILE_PATH = BASE_PATH / "Diod.csv"


class DiodeDirectoryApp(tk.Tk):
    def __init__(self, storage: list[dict]):
        super().__init__()
        self.title('Справочник полупроводниковых диодов')
        self.geometry('640x480')
        self.storage = storage

        Label(self, text="Введите наименование диода:").pack(pady=10)
        self.search_entry = Entry(self, width=50)
        self.search_entry.pack(pady=10)

        Button(self, text="Поиск", command=self.search_diodes).pack(pady=10)

        self.results_text = scrolledtext.ScrolledText(self, width=70, height=30)
        self.results_text.pack(pady=20)

    def search_diodes(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            messagebox.showinfo("Ошибка", "Введите значение для поиска!")
            return

        pattern = re.compile(f"^{query}$", flags=2)
        found_diodes = [diode for diode in self.storage if re.match(pattern, diode["Наименование диода"])]

        self.results_text.delete('1.0', tk.END)
        if found_diodes:
            for diode in found_diodes:
                for key, value in diode.items():
                    self.results_text.insert(tk.END, f"{key}: {value}\n")
                self.results_text.insert(tk.END, "-" * 60 + "\n")
        else:
            messagebox.showinfo("Результат", "Указанное наименование отсутствует!")


def add_diods_from_csv(storage: list):
    with open(CSV_FILE_PATH, "r", encoding="utf-8") as fi:
        csv_reader = csv.DictReader(fi, delimiter="|", dialect="excel")
        for line in csv_reader:
            storage.append(line)


if __name__ == '__main__':
    diodes: list = []
    add_diods_from_csv(diodes)
    app = DiodeDirectoryApp(storage=diodes)
    app.mainloop()
