import customtkinter as ctk
import re
import csv
import os
import shutil
from tkinter import filedialog, messagebox


class ImportHighlighter(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.csv_path = None

        self.title("Maximo Import Error Highlighter")
        self.geometry("860x720")
        self.minsize(680, 520)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(
            self, text="  Maximo Import Error Highlighter",
            font=ctk.CTkFont("Segoe UI", 18, "bold"),
            anchor="w",
        )
        title.grid(row=0, column=0, padx=20, pady=(16, 8), sticky="ew")

        card = ctk.CTkFrame(self)
        card.grid(row=1, column=0, padx=20, pady=(0, 12), sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            card, text="Paste Maximo Import Preview:",
            font=ctk.CTkFont("Segoe UI", 13),
            anchor="w",
        ).grid(row=0, column=0, padx=16, pady=(16, 6), sticky="ew")

        self.preview_text = ctk.CTkTextbox(
            card, wrap="word",
            font=ctk.CTkFont("Consolas", 12),
        )
        self.preview_text.grid(row=1, column=0, padx=16, pady=(0, 10), sticky="nsew")

        sep = ctk.CTkFrame(card, height=1, fg_color="#3c3c3c")
        sep.grid(row=2, column=0, padx=16, pady=4, sticky="ew")

        csv_row = ctk.CTkFrame(card, fg_color="transparent")
        csv_row.grid(row=3, column=0, padx=16, pady=(6, 2), sticky="ew")
        csv_row.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            csv_row, text="Browse for CSV...",
            command=self.select_csv,
            width=130,
            font=ctk.CTkFont("Segoe UI", 12),
        ).grid(row=0, column=0, padx=(0, 10))

        self.csv_label = ctk.CTkLabel(
            csv_row, text="No file selected",
            anchor="w",
            font=ctk.CTkFont("Segoe UI", 12),
            text_color="#888888",
        )
        self.csv_label.grid(row=0, column=1, sticky="ew")

        sep2 = ctk.CTkFrame(card, height=1, fg_color="#3c3c3c")
        sep2.grid(row=4, column=0, padx=16, pady=4, sticky="ew")

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.grid(row=5, column=0, padx=16, pady=(10, 14), sticky="ew")

        self.run_btn = ctk.CTkButton(
            btn_row, text="Mark Import Errors",
            command=self.run,
            font=ctk.CTkFont("Segoe UI", 13, "bold"),
            height=36,
            width=200,
        )
        self.run_btn.pack()

        self.status_label = ctk.CTkLabel(
            card, text="",
            anchor="w",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color="#4ec9b0",
        )
        self.status_label.grid(row=6, column=0, padx=16, pady=(0, 12), sticky="ew")

    def select_csv(self):
        path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if path:
            self.csv_path = path
            name = os.path.basename(path)
            self.csv_label.configure(text=name, text_color="#d4d4d4")

    def parse_preview(self, text):
        errors = {}
        lines = text.split("\n")
        i = 0
        while i < len(lines):
            line = lines[i]
            m = re.search(r"starts at line (\d+) and ends at line (\d+)", line)
            if m and "BMXAA5598E" in line:
                start = int(m.group(1))
                end = int(m.group(2))
                detail = ""
                for j in range(i + 1, len(lines)):
                    if lines[j].strip():
                        detail = lines[j].strip()
                        break
                for ln in range(start, end + 1):
                    if ln not in errors:
                        errors[ln] = detail
                    else:
                        existing = errors[ln]
                        if detail not in existing:
                            errors[ln] = existing + " | " + detail
            i += 1
        return errors

    def run(self):
        preview = self.preview_text.get("1.0", "end-1c").strip()
        if not preview:
            messagebox.showerror("Error", "Paste the Maximo import preview first.")
            return
        if not self.csv_path:
            messagebox.showerror("Error", "Select a CSV file first.")
            return

        try:
            errors = self.parse_preview(preview)
            if not errors:
                messagebox.showinfo("No Errors", "No BMXAA5598E errors found in the preview.")
                return

            with open(self.csv_path, "r", encoding="utf-8-sig", newline="") as f:
                reader = csv.reader(f)
                rows = [row for row in reader if any(field.strip() for field in row)]

            if not rows:
                messagebox.showerror("Error", "CSV file is empty.")
                return

            has_column = rows[0] and rows[0][-1] == "Import_Error"

            if not has_column:
                rows[0].append("Import_Error")

            marked = 0
            for i in range(1, len(rows)):
                csv_line_num = i + 1
                msg = errors.get(csv_line_num, "")
                if has_column:
                    rows[i][-1] = msg
                else:
                    rows[i].append(msg)
                if msg:
                    marked += 1

            bak_path = self.csv_path + ".bak"
            shutil.copy2(self.csv_path, bak_path)

            with open(self.csv_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(rows)

            self.status_label.configure(
                text=f"Done — {marked} rows marked. Backup saved to {os.path.basename(bak_path)}"
            )
            messagebox.showinfo(
                "Success",
                f"Lines with errors in preview: {len(errors)}\n"
                f"Rows marked in CSV: {marked}\n"
                f"Backup saved to: {bak_path}"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = ImportHighlighter()
    app.mainloop()
