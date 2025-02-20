import functions
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import random

group = 42
group_num = 18

class Window1:
    def __init__(self, root):
        self.root = root
        self.root.title("Вікно #1")
        self.set_a = set()
        self.set_b = set()
        self.set_c = set()
        self.universal_set = set()

        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        menu.add_command(label="Вікно #2", command=self.open_window2)
        menu.add_command(label="Вікно #3", command=self.open_window3)
        menu.add_command(label="Вікно #4", command=self.open_window4)
        menu.add_command(label="Вікно #5", command=self.open_window5)

        frame_info = tk.Frame(self.root)
        frame_info.pack(pady=10)
        tk.Label(frame_info, text="ПІБ студента: Куліков Максим Миколайович").grid(row=0, column=0)
        tk.Label(frame_info, text=f"Група: ІО-{group}").grid(row=1, column=0)
        tk.Label(frame_info, text=f"Номер у списку: {group_num}").grid(row=2, column=0)
        tk.Label(frame_info, text=f"Розрахований варіант: {functions.calculate_var(group, group_num)}").grid(row=3, column=0)

        self.mode = tk.StringVar(value="auto")
        frame_mode = tk.Frame(self.root)
        frame_mode.pack(pady=10)
        tk.Radiobutton(frame_mode, text="Автоматичне генерування", variable=self.mode, value="auto", command=self.toggle_mode).grid(row=0, column=0, padx=10)
        tk.Radiobutton(frame_mode, text="Ручне введення", variable=self.mode, value="manual", command=self.toggle_mode).grid(row=0, column=1, padx=10)

        self.frame_inputs = tk.Frame(self.root)
        self.frame_inputs.pack(pady=10)
        self.frame_manual_inputs = tk.Frame(self.frame_inputs)
        self.frame_manual_inputs.grid(row=0, column=0, sticky="nsew")
        self.frame_auto_inputs = tk.Frame(self.frame_inputs)
        self.frame_auto_inputs.grid(row=0, column=0, sticky="nsew")
        self.create_auto_inputs()
        self.create_manual_inputs()
        self.toggle_mode()
        frame_results = tk.Frame(self.root)
        frame_results.pack(pady=10)
        self.label_A = tk.Label(frame_results, text="A: {}")
        self.label_A.pack()
        self.label_B = tk.Label(frame_results, text="B: {}")
        self.label_B.pack()
        self.label_C = tk.Label(frame_results, text="C: {}")
        self.label_C.pack()
        self.label_U = tk.Label(frame_results, text="U: {}")
        self.label_U.pack()

    def toggle_mode(self):
        if self.mode.get() == "manual":
            self.frame_manual_inputs.tkraise()
        else:
            self.frame_auto_inputs.tkraise()

    def create_manual_inputs(self):
        frame = self.frame_manual_inputs
        frame.grid_columnconfigure((0, 1), weight=1)
        tk.Label(frame, text="Елементи множини A (через кому):").grid(row=0, column=0)
        self.entry_manual_a = tk.Entry(frame, width=20)
        self.entry_manual_a.grid(row=0, column=1)
        tk.Label(frame, text="Елементи множини B (через кому):").grid(row=1, column=0)
        self.entry_manual_b = tk.Entry(frame, width=20)
        self.entry_manual_b.grid(row=1, column=1)
        tk.Label(frame, text="Елементи множини C (через кому):").grid(row=2, column=0)
        self.entry_manual_c = tk.Entry(frame, width=20)
        self.entry_manual_c.grid(row=2, column=1)
        tk.Label(frame, text="Універсум (через кому):").grid(row=3, column=0)
        self.entry_manual_u = tk.Entry(frame, width=20)
        self.entry_manual_u.grid(row=3, column=1)
        tk.Button(frame, text="Застосувати", command=self.generate_manual_sets).grid(row=4, column=0, columnspan=2, pady=10)

    def create_auto_inputs(self):
        frame = self.frame_auto_inputs
        frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        tk.Label(frame, text="Кількість елементів A:").grid(row=0, column=0)
        self.entry_a = tk.Entry(frame, width=5)
        self.entry_a.grid(row=0, column=1)
        self.entry_a.insert(0, "4")
        tk.Label(frame, text="Кількість елементів B:").grid(row=1, column=0)
        self.entry_b = tk.Entry(frame, width=5)
        self.entry_b.grid(row=1, column=1)
        self.entry_b.insert(0, "4")
        tk.Label(frame, text="Кількість елементів C:").grid(row=2, column=0)
        self.entry_c = tk.Entry(frame, width=5)
        self.entry_c.grid(row=2, column=1)
        self.entry_c.insert(0, "4")
        tk.Label(frame, text="Діапазон чисел:").grid(row=3, column=0, pady=10)
        self.entry_range_min = tk.Entry(frame, width=10)
        self.entry_range_min.grid(row=3, column=1)
        self.entry_range_min.insert(0, "0")
        self.entry_range_max = tk.Entry(frame, width=10)
        self.entry_range_max.grid(row=3, column=2)
        self.entry_range_max.insert(0, "10")
        tk.Button(frame, text="Згенерувати", command=self.generate_auto_sets).grid(row=4, column=0, columnspan=3, pady=10)

    def generate_manual_sets(self):
        try:
            self.set_a = set(map(int, self.entry_manual_a.get().split(','))) if self.entry_manual_a.get().strip() else set()
            self.set_b = set(map(int, self.entry_manual_b.get().split(','))) if self.entry_manual_b.get().strip() else set()
            self.set_c = set(map(int, self.entry_manual_c.get().split(','))) if self.entry_manual_c.get().strip() else set()
            if self.entry_manual_u.get().strip():
                manual_u = set(map(int, self.entry_manual_u.get().split(',')))
                self.universal_set = self.set_a | self.set_b | self.set_c | manual_u
            else:
                self.universal_set = set(self.set_a | self.set_b | self.set_c)
            self.update_results()
        except ValueError:
            messagebox.showerror("Помилка", "Введіть коректні значення для множин A, B, C.")

    def generate_auto_sets(self):
        min_val = int(self.entry_range_min.get())
        max_val = int(self.entry_range_max.get())
        self.universal_set = set(range(min_val, max_val + 1))
        self.set_a = set(random.sample(list(self.universal_set), int(self.entry_a.get())))
        self.set_b = set(random.sample(list(self.universal_set), int(self.entry_b.get())))
        self.set_c = set(random.sample(list(self.universal_set), int(self.entry_c.get())))
        self.update_results()

    def update_results(self):
        def format_set(s):
            return "{}" if not s else str(s)
        self.label_A.config(text=f"A: {format_set(self.set_a)}")
        self.label_B.config(text=f"B: {format_set(self.set_b)}")
        self.label_C.config(text=f"C: {format_set(self.set_c)}")
        self.label_U.config(text=f"U: {format_set(self.universal_set)}")

    def open_window2(self):
        if self.are_sets_created():
            Window2(self.root, self.set_a, self.set_b, self.set_c)
        else:
            messagebox.showerror("Помилка", "Спочатку створіть множини!")

    def open_window3(self):
        if self.are_sets_created():
            Window3(self.root, self.set_a, self.set_b, self.set_c)
        else:
            messagebox.showerror("Помилка", "Спочатку створіть множини!")

    def open_window4(self):
        if self.are_sets_created():
            Window4(self.root, self.set_a, self.set_b)
        else:
            messagebox.showerror("Помилка", "Спочатку створіть множини!")

    def open_window5(self):
        if self.are_sets_created():
            Window5(self.root, self.set_a, self.set_b)
        else:
            messagebox.showerror("Помилка", "Спочатку створіть множини!")

    def are_sets_created(self):
        return bool(self.set_a and self.set_b and self.set_c)

class Window2:
    def __init__(self, root, set_a, set_b, set_c):
        self.root = root
        self.set_a = set_a
        self.set_b = set_b
        self.set_c = set_c
        self.step = 0
        self.result_d = set()
        self.calculator = functions.calculate_default_expression(self.set_a, self.set_b, self.set_c)
        self.window = tk.Toplevel(self.root)
        self.window.title("Вікно #2")
        self.label_D = tk.Label(self.window, text="D: {}")
        self.label_D.pack(pady=10)
        self.label_step1 = tk.Label(self.window, text="Крок 1: A \\ B")
        self.label_step1.pack(anchor="center")
        self.label_step1_res = tk.Label(self.window, text="Результат буде тут", fg="blue")
        self.label_step1_res.pack(anchor="center")
        self.label_step2 = tk.Label(self.window, text="Крок 2: B ∩ A")
        self.label_step2.pack(anchor="center")
        self.label_step2_res = tk.Label(self.window, text="Результат буде тут", fg="blue")
        self.label_step2_res.pack(anchor="center")
        self.label_step3 = tk.Label(self.window, text="Крок 3: (A \\ B) ∪ (B ∩ A)")
        self.label_step3.pack(anchor="center")
        self.label_step3_res = tk.Label(self.window, text="Результат буде тут", fg="blue")
        self.label_step3_res.pack(anchor="center")
        self.label_step4 = tk.Label(self.window, text="Крок 4: C ∪ B")
        self.label_step4.pack(anchor="center")
        self.label_step4_res = tk.Label(self.window, text="Результат буде тут", fg="blue")
        self.label_step4_res.pack(anchor="center")
        self.label_step5 = tk.Label(self.window, text="Крок 5: ((A \\ B) ∪ (B ∩ A)) \\ (C ∪ B)")
        self.label_step5.pack(anchor="center")
        self.label_step5_res = tk.Label(self.window, text="Результат буде тут", fg="blue")
        self.label_step5_res.pack(anchor="center")
        self.calculate_button = tk.Button(self.window, text="Обчислити", command=self.calculate_step_by_step)
        self.calculate_button.pack(pady=10)
        self.save_button = tk.Button(self.window, text="Зберегти результат", command=self.save_result)
        self.save_button.pack(pady=10)

    def calculate_step_by_step(self):
        try:
            step_result = next(self.calculator)
            if not step_result:
                step_result = "{}"
            if self.step == 0:
                self.label_step1_res.config(text=f"{step_result}")
            elif self.step == 1:
                self.label_step2_res.config(text=f"{step_result}")
            elif self.step == 2:
                self.label_step3_res.config(text=f"{step_result}")
            elif self.step == 3:
                self.label_step4_res.config(text=f"{step_result}")
            elif self.step == 4:
                self.label_step5_res.config(text=f"{step_result}")
                self.result_d = step_result
                self.label_D.config(text=f"D: {self.result_d}")
                self.calculate_button.config(state=tk.DISABLED)
            self.step += 1
        except StopIteration:
            self.calculate_button.config(state=tk.DISABLED)

    def save_result(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(f"Результат обчислення D: {self.result_d}")

class Window3:
    def __init__(self, root, set_a, set_b, set_c):
        self.root = root
        self.set_a = set_a
        self.set_b = set_b
        self.set_c = set_c
        self.step = 0
        self.result_d = set()
        self.calculator = functions.calculate_simplified_expression(self.set_a, self.set_b, self.set_c)
        self.window = tk.Toplevel(self.root)
        self.window.title("Вікно #3")
        self.label_D = tk.Label(self.window, text="D: {}")
        self.label_D.pack(pady=10)
        self.label_step1 = tk.Label(self.window, text="Крок 1: C ∪ B")
        self.label_step1.pack(anchor="center")
        self.label_step1_res = tk.Label(self.window, text="Результат буде тут", fg="blue")
        self.label_step1_res.pack(anchor="center")
        self.label_step2 = tk.Label(self.window, text="Крок 2: A \\ (C ∪ B) = ")
        self.label_step2.pack(anchor="center")
        self.label_step2_res = tk.Label(self.window, text="Результат буде тут", fg="blue")
        self.label_step2_res.pack(anchor="center")
        self.calculate_button = tk.Button(self.window, text="Обчислити", command=self.calculate_step_by_step)
        self.calculate_button.pack(pady=10)
        self.save_button = tk.Button(self.window, text="Зберегти результат", command=self.save_result)
        self.save_button.pack(pady=10)

    def calculate_step_by_step(self):
        try:
            step_result = next(self.calculator)
            if not step_result:
                step_result = "{}"
            if self.step == 0:
                self.label_step1_res.config(text=f"{step_result}")
            elif self.step == 1:
                self.label_step2_res.config(text=f"{step_result}")
                self.result_d = step_result
                self.label_D.config(text=f"D: {self.result_d}")
                self.calculate_button.config(state=tk.DISABLED)
            self.step += 1
        except StopIteration:
            self.calculate_button.config(state=tk.DISABLED)

    def save_result(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(f"Результат спрощеного обчислення D: {self.result_d}")

class Window4:
    def __init__(self, root, set_x, set_y):
        self.root = root
        self.set_x = set_x
        self.set_y = set_y
        self.result_z = set()
        self.window = tk.Toplevel(self.root)
        self.window.title("Вікно #4")
        self.label_X = tk.Label(self.window, text=f"X = {self.set_x}")
        self.label_X.pack()
        self.label_Y = tk.Label(self.window, text=f"Y = {self.set_y}")
        self.label_Y.pack()
        self.label_Z = tk.Label(self.window, text="X\\Y = Z: ")
        self.label_Z.pack()
        self.calculate_button = tk.Button(self.window, text="Обчислити Z", command=self.calculate_z)
        self.calculate_button.pack()
        self.save_z_button = tk.Button(self.window, text ="Зберегти Z до файлу", command=self.save_z)
        self.save_z_button.pack()
    def calculate_z(self):
        self.result_z = functions.calculate_z(self.set_x, self.set_y)
        self.label_Z.config(text=f"X\\Y = Z: {self.result_z}")
    def save_z(self):
        if self.result_z:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                with open(file_path, "w") as file:
                    file.write(f"Результат обчислення Z: {self.result_z}")
        else:
            messagebox.showerror("Помилка", "Спочатку обчисліть Z!")


class Window5:
        def __init__(self, root, x_set, y_set):
            self.root = root
            self.x_set = x_set
            self.y_set = y_set
            self.window = tk.Toplevel(self.root)
            self.window.title("Вікно #5")
            self.window.minsize(width=200, height=250)
            tk.Button(self.window, text="Завантажити множину D", command=self.load_d_set).pack()
            self.label_expr = tk.Label(self.window, text="Початковий вираз: Невідомо")
            self.label_expr.pack()
            tk.Button(self.window, text="Завантажити спрощену множину D", command=self.load_simplified_d_set).pack()
            self.label_simplified_expr = tk.Label(self.window, text="Спрощений вираз: Невідомо")
            self.label_simplified_expr.pack()
            tk.Button(self.window, text="Завантажити множину Z", command=self.load_z_set).pack()
            self.label_z = tk.Label(self.window, text="Z: Невідомо")
            self.label_z.pack()
            tk.Button(self.window, text="Обчислити множину Z", command=self.calculate_z).pack()
            self.label_calc_z = tk.Label(self.window, text="Обчислений Z: Невідомо")
            self.label_calc_z.pack()
            tk.Button(self.window, text="Порівняти результати", command=self.compare_results).pack()
            self.label_comparison = tk.Label(self.window, text="Результат порівняння: Невідомо")
            self.label_comparison.pack()

        def load_d_set(self):
            self.d_set = self.load_set_from_file("Початковий вираз", self.label_expr)

        def load_simplified_d_set(self):
            self.simplified_d_set = self.load_set_from_file("Спрощений вираз", self.label_simplified_expr)

        def load_set_from_file(self, label_text, label):
            file_path = filedialog.askopenfilename(filetypes=[("Текстові файли", "*.txt"), ("Усі файли", "*.*")])
            if file_path:
                try:
                    with open(file_path, "r") as file:
                        content = file.read().strip()
                        content = content.split(":")[-1].strip()
                        content = content.strip("{}")
                        set_data = set(map(int, content.split(',')))
                        label.config(text=f"{label_text}: {set_data}")
                        return set_data
                except Exception as e:
                    messagebox.showerror("Помилка", f"Не вдалося завантажити {label_text}: {e}")
                    return None

        def load_z_set(self):
            self.z_set = self.load_set_from_file("Z", self.label_z)

        def calculate_z(self):
            if hasattr(self, 'x_set') and hasattr(self, 'y_set'):
                self.calc_z = functions.calculate_z(self.x_set, self.y_set)
                self.label_calc_z.config(text=f"Обчислений Z: {self.calc_z}")
            else:
                messagebox.showerror("Помилка", "Передайте множини X і Y!")

        def compare_results(self):
            comparison_results = []
            if hasattr(self, 'd_set') and hasattr(self, 'simplified_d_set'):
                comparison_results.append(
                    "D і спрощена D співпадають" if self.d_set == self.simplified_d_set else "D і спрощена D не співпадають")
            else:
                comparison_results.append("Завантажте множини D!")
            if hasattr(self, 'calc_z') and hasattr(self, 'z_set'):
                comparison_results.append(
                    "Обчислений Z і завантажений Z співпадають" if self.calc_z == self.z_set else "Обчислений Z і завантажений Z не співпадають")
            else:
                comparison_results.append("Спочатку завантажте та обчисліть Z!")
            self.label_comparison.config(text="\n".join(comparison_results))

if __name__ == "__main__":
    root = tk.Tk()
    app = Window1(root)
    root.mainloop()