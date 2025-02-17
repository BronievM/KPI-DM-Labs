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
        tk.Radiobutton(frame_mode, text="Автоматичне генерування", variable=self.mode, value="auto",
                       command=self.toggle_mode).grid(row=0, column=0, padx=10)
        tk.Radiobutton(frame_mode, text="Ручне введення", variable=self.mode, value="manual",
                       command=self.toggle_mode).grid(row=0, column=1, padx=10)

        self.frame_inputs = tk.Frame(self.root)
        self.frame_inputs.pack(pady=10)
        self.frame_manual_inputs = tk.Frame(self.frame_inputs)
        self.frame_manual_inputs.grid(row=0, column=0, sticky="nsew")
        self.frame_auto_inputs = tk.Frame(self.frame_inputs)
        self.frame_auto_inputs.grid(row=0, column=0, sticky="nsew")

        self.create_auto_inputs()
        self.create_manual_inputs()
        self.toggle_mode()

        self.set_a = set()
        self.set_b = set()
        self.set_c = set()
        self.universal_set = set()

        self.create_result_labels()

    def create_result_labels(self):
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
        self.entry_range_min = tk.Entry(frame, width=5)
        self.entry_range_min.grid(row=3, column=1)
        self.entry_range_min.insert(0, "0")
        self.entry_range_max = tk.Entry(frame, width=5)
        self.entry_range_max.grid(row=3, column=2)
        self.entry_range_max.insert(0, "10")

        tk.Button(frame, text="Згенерувати", command=self.generate_auto_sets).grid(row=4, column=0, columnspan=3, pady=10)

    def generate_manual_sets(self):
        try:
            self.set_a = set(map(int, self.entry_manual_a.get().split(',')))
            self.set_b = set(map(int, self.entry_manual_b.get().split(',')))
            self.set_c = set(map(int, self.entry_manual_c.get().split(',')))
            if self.entry_manual_u.get().strip() != "":
                self.universal_set = set(map(int, self.entry_manual_u.get().split(',')))
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
        self.label_A.config(text=f"A: {self.set_a}")
        self.label_B.config(text=f"B: {self.set_b}")
        self.label_C.config(text=f"C: {self.set_c}")
        self.label_U.config(text=f"U: {self.universal_set}")

    def open_window2(self):
        Window2(self.root, self.set_a, self.set_b, self.set_c)

    def open_window3(self): pass
    def open_window4(self):
        Window4(self.root, self.set_a, self.set_b)
    def open_window5(self): pass

class Window2:
    def __init__(self, root, set_a, set_b, set_c):
        self.root = root
        self.set_a = set_a
        self.set_b = set_b
        self.set_c = set_c
        self.step = 0
        self.result_d = set()

        self.window = tk.Toplevel(self.root)
        self.window.title("Вікно #2")

        self.label_D = tk.Label(self.window, text="D: {}")
        self.label_D.pack(pady=10)

        self.label_step1 = tk.Label(self.window, text="Крок 1: ")
        self.label_operands.pack()
        self.label_step1_res = tk.Label(self.window, text="Result ")
        self.label_operands.pack(pady=10)

        self.calculate_button = tk.Button(self.window, text="Обчислити", command=self.calculate_step_by_step)
        self.calculate_button.pack(pady=10)

        self.save_button = tk.Button(self.window, text="Зберегти результат", command=self.save_result)
        self.save_button.pack(pady=10)

    def calculate_step_by_step(self):
            gen = functions.calc_steps(self.set_a, self.set_b, self.set_c) 
            stepResult = next(gen)
            self.result_d = stepResult
            self.label_step1.config(text=f"{stepResult}")
            self.label_D.config(text=f"D: {self.result_d}")
            
 


    def save_result(self):
        file_path = filedialog.asksaveasfilename(defaultextension="result-D.txt",
                                                 filetypes=[("Текстові файли", "*.txt"), ("Усі файли", "*.*")])
        if file_path:
            file_path.write(f"Результат обчислення D: {self.result_d}")
            file_path.close()

class Window4:
    def __init__(self, root, set_x, set_y):
        self.root = root
        self.set_x = set_x
        self.set_y = set_y

        self.window = tk.Toplevel(self.root)
        self.window.title("Вікно #4")

        self.label_X = tk.Label(self.window, text=f"X = {self.set_x}")
        self.label_X.pack()

        self.label_Y = tk.Label(self.window, text=f"Y = {self.set_y}")
        self.label_Y.pack()

        self.label_Z = tk.Label(self.window, text="Z: ")
        self.label_Z.pack()

        self.calculate_button = tk.Button(self.window, text="Обчислити Z", command=self.calculate_z)
        self.calculate_button.pack()



    def calculate_z(self):
        z_result = functions.calculate_z(self.set_x, self.set_y)
        self.label_Z.config(text=f"Z: {z_result}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Window1(root)
    root.mainloop()
