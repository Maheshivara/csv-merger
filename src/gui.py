from os import environ
from pathlib import Path
from sys import base_prefix

environ["TCL_LIBRARY"] = str(Path(base_prefix) / "tcl" / "tcl8.6")
environ["TK_LIBRARY"] = str(Path(base_prefix) / "tcl" / "tk8.6")
import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
from src.merger import merge_csv


def start_app():
    root = tk.Tk()
    root.title("Unir CSVs")

    left_file_path = tk.StringVar()
    right_file_path = tk.StringVar()
    left_column = tk.StringVar()
    right_column = tk.StringVar()
    output_file_path = tk.StringVar()

    def create_checkboxes(frame, columns, selected_columns, title):
        tk.Label(frame, text=title).pack(anchor="w")
        for col in columns:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(frame, text=col, variable=var)
            chk.pack(anchor="w")
            selected_columns[col] = var

    def select_columns(file_path, frame, selected_columns, title):
        df = pd.read_csv(file_path)
        columns = df.columns.tolist()
        create_checkboxes(frame, columns, selected_columns, title)
        return columns

    columns_frame = tk.Frame(root)
    columns_frame.grid(row=3, column=0, columnspan=6, sticky="nw")
    tk.Label(columns_frame, text="Colunas para manter:").grid(
        row=0, column=0, columnspan=6, sticky="n"
    )

    left_columns_frame = tk.Frame(columns_frame)
    left_columns_frame.grid(row=1, column=0, columnspan=3, sticky="nw")
    right_columns_frame = tk.Frame(columns_frame)
    right_columns_frame.grid(row=1, column=3, columnspan=3, sticky="nw")

    left_selected_columns = {}
    right_selected_columns = {}

    def select_left_file():
        file_path = filedialog.askopenfilename(filetypes=[("CSV principal", "*.csv")])
        if file_path:
            left_file_path.set(file_path)
            for widget in left_columns_frame.winfo_children():
                widget.destroy()
            columns = select_columns(
                file_path, left_columns_frame, left_selected_columns, "CSV principal"
            )
            left_column_combobox["values"] = columns

    def select_right_file():
        file_path = filedialog.askopenfilename(filetypes=[("CSV auxiliar", "*.csv")])
        if file_path:
            right_file_path.set(file_path)
            for widget in right_columns_frame.winfo_children():
                widget.destroy()
            columns = select_columns(
                file_path, right_columns_frame, right_selected_columns, "CSV auxiliar"
            )
            right_column_combobox["values"] = columns

    def on_confirm():
        if not left_file_path.get() or not right_file_path.get():
            tk.messagebox.showerror("Erro", "Selecione todos os arquivos necessários.")
            return

        if not output_file_path.get():
            tk.messagebox.showerror("Erro", "Selecione a pasta de saída.")
            return

        left_on = left_column.get()
        right_on = right_column.get()
        if not left_on or not right_on:
            tk.messagebox.showerror("Erro", "Escolha as colunas de junção.")
            return
        
        left_selected = [
                col for col, var in left_selected_columns.items() if var.get()
            ]
        right_selected = [
            col for col, var in right_selected_columns.items() if var.get()
        ]
        if len(left_selected) == 0 or len(right_selected) == 0:
            tk.messagebox.showerror("Erro", "Selecione pelo menos uma coluna de cada CSV.")
            return
        
        try:
            merge_csv(
                [left_file_path.get(), right_file_path.get()],
                left_on,
                right_on,
                output_file_path.get(),
                left_selected,
                right_selected,
            )
            tk.messagebox.showinfo("Sucesso", "Os CSVs foram unidos com sucesso!")
        except Exception:
            tk.messagebox.showerror("Erro", "Ops, ocorreu um erro ao unir os CSVs.")

    def select_output_file():
        file_path = filedialog.askdirectory(title="Selecione a pasta de saída")
        if file_path:
            output_file_path.set(file_path)

    tk.Label(root, text="CSV principal:").grid(row=0, column=0, sticky="w")
    left_file_button = tk.Button(root, text="Selecionar", command=select_left_file)
    left_file_button.grid(row=0, column=1, sticky="w")
    left_column_combobox = ttk.Combobox(root, textvariable=left_column)
    left_column_combobox.grid(row=0, column=2, sticky="w")

    tk.Label(root, text="CSV para juntar:").grid(row=1, column=0, sticky="w")
    right_file_button = tk.Button(root, text="Selecionar", command=select_right_file)
    right_file_button.grid(row=1, column=1, sticky="w")
    right_column_combobox = ttk.Combobox(root, textvariable=right_column)
    right_column_combobox.grid(row=1, column=2, sticky="w")

    tk.Label(root, text="Caminho do arquivo de saída:").grid(
        row=2, column=0, sticky="w"
    )
    output_file_button = tk.Button(root, text="Selecionar", command=select_output_file)
    output_file_button.grid(row=2, column=1, sticky="w")

    confirm_button = tk.Button(root, text="Confirmar", command=on_confirm)
    confirm_button.grid(row=4, column=0, columnspan=3)

    root.mainloop()
