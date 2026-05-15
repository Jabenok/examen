import csv
import os
from fpdf import FPDF


class Report:
    def __init__(self, headers):
        self.headers = headers
        self.rows = []

    def add_row(self, row):
        if len(row) != len(self.headers):
            raise ValueError()
        self.rows.append(row)

    def get_data(self):
        return [self.headers] + self.rows

    def to_csv(self, filename):
        try:
            with open(filename, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(self.get_data())
        except PermissionError:
            print(f"Ошибка: Нет прав на запись в файл '{filename}'.")
        except OSError as e:
            if e.errno == 28:
                print(f"Ошибка: Недостаточно свободного места на диске для сохранения '{filename}'.")
            else:
                print(f"Ошибка ввода-вывода при работе с '{filename}': {e}")


class PDFExporter:
    @staticmethod
    def convert_csv_to_pdf(csv_filename, pdf_filename):
        try:
            if not os.path.exists(csv_filename):
                print(f"Ошибка: Исходный файл '{csv_filename}' не найден.")
                return

            with open(csv_filename, mode="r", encoding="utf-8") as f:
                reader = csv.reader(f)
                data = list(reader)

            if not data:
                print(f"Ошибка: Файл '{csv_filename}' пуст.")
                return

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            col_width = pdf.epw / len(data[0])
            row_height = pdf.font_size * 2

            for row in data:
                for item in row:
                    pdf.cell(col_width, row_height, txt=str(item), border=1)
                pdf.ln(row_height)

            pdf.output(pdf_filename)

        except PermissionError:
            print(f"Ошибка: Нет прав на запись файла '{pdf_filename}'.")
        except OSError as e:
            if e.errno == 28:
                print(f"Ошибка: Недостаточно места на диске для создания '{pdf_filename}'.")
            else:
                print(f"Ошибка при создании PDF '{pdf_filename}': {e}")


if __name__ == "__main__":
    report = Report(["ID", "Name", "Role"])
    report.add_row(["1", "Alice", "Developer"])
    report.add_row(["2", "Bob", "Manager"])
    report.add_row(["3", "Charlie", "Designer"])

    csv_file = "report.csv"
    pdf_file = "report.pdf"

    report.to_csv(csv_file)
    PDFExporter.convert_csv_to_pdf(csv_file, pdf_file)