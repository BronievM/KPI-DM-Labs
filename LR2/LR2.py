import tkinter as tk
import LR2Data as data
from tkinter import messagebox
from tkinter import filedialog

group = 42
group_num = 18

set_a = set()
set_b = set()

class Window1:
    def __init__(self, root):
        self.root = root
        self.root.title("Вікно #1")

        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        menu.add_command(label="Вікно #2", command=self.open_window2)
        menu.add_command(label="Вікно #3", command=self.open_window3)
        menu.add_command(label="Вікно #4", command=self.open_window4)

        frame_info = tk.Frame(self.root)
        frame_info.pack(pady=10)
        tk.Label(frame_info, text="ПІБ студента: Куліков Максим Миколайович").grid(row=0, column=0)
        tk.Label(frame_info, text=f"Група: ІО-{group}").grid(row=1, column=0)
        tk.Label(frame_info, text=f"Номер у списку: {group_num}").grid(row=2, column=0)
        tk.Label(frame_info, text=f"Розрахований варіант: {data.calculate_var(group, group_num)}").grid(row=3, column=0)

    def open_window2(self):
        new_window = tk.Toplevel(self.root)
        Window2(new_window)

    def open_window3(self):
        new_window = tk.Toplevel(self.root)
        Window3(new_window)

    def open_window4(self):
        new_window = tk.Toplevel(self.root)
        Window4(new_window)


class Window2:
    def __init__(self, root):
        self.root = root
        self.root.title("Вікно #2")
        tk.Label(root, text="Жіночі імена").grid(row=0, column=0)
        self.list_female = tk.Listbox(root, selectmode=tk.MULTIPLE, height=10)
        self.list_female.grid(row=1, column=0, padx=15, pady=10)
        tk.Label(root, text="Чоловічі імена").grid(row=0, column=2)
        self.list_male = tk.Listbox(root, selectmode=tk.MULTIPLE, height=10)
        self.list_male.grid(row=1, column=2, padx=15, pady=10)
        for name in data.female_names:
            self.list_female.insert(tk.END, name)
        for name in data.male_names:
            self.list_male.insert(tk.END, name)

        self.radio_var = tk.StringVar(value="A")
        tk.Radiobutton(root, text="Множина A", variable=self.radio_var, value="A").grid(row=3, column=0)
        tk.Radiobutton(root, text="Множина B", variable=self.radio_var, value="B").grid(row=3, column=2)
        btn_add = tk.Button(root, text="Додати", command=self.add_to_set)
        btn_add.grid(row=4, column=1, pady=5)
        btn_save_a = tk.Button(root, text="Зберегти A", command=lambda: self.save_set("A"))
        btn_save_a.grid(row=5, column=0)
        btn_save_b = tk.Button(root, text="Зберегти B", command=lambda: self.save_set("B"))
        btn_save_b.grid(row=6, column=0)
        btn_load_a = tk.Button(root, text="Зчитати A", command=lambda: self.load_set("A"))
        btn_load_a.grid(row=5, column=1)
        btn_load_b = tk.Button(root, text="Зчитати B", command=lambda: self.load_set("B"))
        btn_load_b.grid(row=6, column=1)
        btn_clear_a = tk.Button(root, text="Очистити A", command=lambda: self.clear_set("A"))
        btn_clear_a.grid(row=5, column=2)
        btn_clear_b = tk.Button(root, text="Очистити B", command=lambda: self.clear_set("B"))
        btn_clear_b.grid(row=6, column=2, pady=10)

        tk.Label(root, text="Множина A").grid(row=7, column=0)
        self.list_a = tk.Listbox(root, height=10)
        self.list_a.grid(row=8, column=0, padx=15, pady=10)
        tk.Label(root, text="Множина B").grid(row=7, column=2)
        self.list_b = tk.Listbox(root, height=10)
        self.list_b.grid(row=8, column=2, padx=15, pady=10)

    def add_to_set(self):
        selected_names = [self.list_female.get(i) for i in self.list_female.curselection()]
        selected_names += [self.list_male.get(i) for i in self.list_male.curselection()]
        target_set = data.set_a if self.radio_var.get() == "A" else data.set_b
        target_list = self.list_a if self.radio_var.get() == "A" else self.list_b

        for name in selected_names:
            if name not in target_set:
                target_set.add(name)
                target_list.insert(tk.END, name)

    def clear_set(self, which):
        if which == "A":
            data.set_a.clear()
            self.list_a.delete(0, tk.END)
            messagebox.showinfo("Успіх!", "Множину A очищено!")
        else:
            data.set_b.clear()
            self.list_b.delete(0, tk.END)
            messagebox.showinfo("Успіх!", "Множину B очищено!")

    def save_set(self, which):
        target_set = data.set_a if which == "A" else data.set_b
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                for item in target_set:
                    file.write(f"{item}\n")
            print(f"Множина {which} збережена у файл {file_path}")

    def load_set(self, which):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                names = file.readlines()
                names = [name.strip() for name in names]
                target_set = data.set_a if which == "A" else data.set_b
                target_list = self.list_a if which == "A" else self.list_b
                target_set.clear()
            for name in names:
                if name not in target_set:
                    target_set.add(name)
                    target_list.insert(tk.END, name)
            messagebox.showinfo("Успіх!", "Множина успішно завантажена!")

class Window3:
    def __init__(self, root):
        self.root = root
        self.root.title("Вікно #3")
        self.root.geometry("1200x470")

        tk.Label(root, text="Множина A:").place(x=20, y=30)
        self.list_a = tk.Listbox(root, selectmode=tk.MULTIPLE, height=10)
        tk.Label(root, text="Множина B:").place(x=20, y=230)
        self.list_b = tk.Listbox(root, selectmode=tk.MULTIPLE, height=10)

        self.list_a.place(x=20, y=50)
        self.list_b.place(x=20, y=250)
        self.button_generate = tk.Button(root, text="Згенерувати S і R", command=lambda: self.calculate_r_s())
        self.button_generate.place(x=20, y=420)
        for item in sorted(data.set_a):
            self.list_a.insert(tk.END, item)
        for item in sorted(data.set_b):
            self.list_b.insert(tk.END, item)
        tk.Label(root, text="aSb, якщо a мати b.").place(x=180, y=20)
        tk.Label(root, text="aRb, якщо a онука b.").place(x=680, y=20)
        self.canvas_s = tk.Canvas(root, width=500, height=400, bg="white")
        self.canvas_s.place(x=180, y=50)
        self.canvas_r = tk.Canvas(root, width=500, height=400, bg="white")
        self.canvas_r.place(x=680, y=50)
        self.coord_dict_a = self.create_coordinates(data.set_a, 50, 100)
        self.coord_dict_b = self.create_coordinates(data.set_b, 50, 300)
        self.create_labels_and_ovals(self.canvas_s, data.set_a, self.coord_dict_a)
        self.create_labels_and_ovals(self.canvas_s, data.set_b, self.coord_dict_b)
        self.create_labels_and_ovals(self.canvas_r, data.set_a, self.coord_dict_a)
        self.create_labels_and_ovals(self.canvas_r, data.set_b, self.coord_dict_b)

    def calculate_r_s(self):
        data.create_random_s()
        data.create_random_r()
        self.update_graphs()

    def create_coordinates(self, names_set, x_start, y_start):
        coordinates = {}
        count = len(names_set)
        if count == 0:
            return coordinates
        spacing = 300 // max(1, count - 1)
        for idx, name in enumerate(sorted(names_set)):
            coordinates[name] = (x_start + idx * spacing, y_start)
        return coordinates

    def create_labels_and_ovals(self, canvas, names_set, coord_dict):
        for name, (x, y) in coord_dict.items():
            canvas.create_text(x, y + 20, text=name, font='Arial 10')
            canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="black")

    def draw_relations(self, canvas, relations, color):
        for a, b in relations:
            if a in self.coord_dict_a and b in self.coord_dict_b:
                x1, y1 = self.coord_dict_a[a]
                x2, y2 = self.coord_dict_b[b]
                canvas.create_line(x1, y1, x2, y2, arrow="last", fill=color)


    def update_graphs(self):
        self.canvas_s.delete("all")
        self.canvas_r.delete("all")
        self.coord_dict_a = self.create_coordinates(data.set_a, 50, 100)
        self.coord_dict_b = self.create_coordinates(data.set_b, 50, 300)
        self.create_labels_and_ovals(self.canvas_s, data.set_a, self.coord_dict_a)
        self.create_labels_and_ovals(self.canvas_s, data.set_b, self.coord_dict_b)
        self.create_labels_and_ovals(self.canvas_r, data.set_a, self.coord_dict_a)
        self.create_labels_and_ovals(self.canvas_r, data.set_b, self.coord_dict_b)
        self.draw_relations(self.canvas_s, data.s, "blue")
        self.draw_relations(self.canvas_r, data.r, "red")

class Window4:
    def __init__(self, root):
        self.root = root
        self.root.title("Вікно #4")

        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack(pady=10)

        tk.Button(root, text="Об'єднання (R∪S)",
                  command=lambda: self.draw_result(set(data.get_union()), "blue")).pack()
        tk.Button(root, text="Перетин (R∩S)",
                  command=lambda: self.draw_result(set(data.get_intersection()), "green")).pack()
        tk.Button(root, text="Різниця (R\\S)",
                  command=lambda: self.draw_result(set(data.get_difference()), "red")).pack()
        tk.Button(root, text="Доповнення (U\\R)",
                  command=lambda: self.draw_result(set(data.get_complement()), "purple")).pack()
        tk.Button(root, text="Обернене S (S⁻¹)",
                  command=lambda: self.draw_result(set(data.get_inverse()), "orange")).pack()

    def draw_result(self, relations, color):
        self.canvas.delete("all")

        coord_a = self.create_coordinates(data.set_a, 50, 100)
        coord_b = self.create_coordinates(data.set_b, 50, 300)

        self.draw_nodes(coord_a)
        self.draw_nodes(coord_b)
        if color == "orange":
            self.draw_relations(relations, coord_b, coord_a, color)
        else:
            self.draw_relations(relations, coord_a, coord_b, color)

    def create_coordinates(self, names_set, x_start, y_start):
        coordinates = {}
        count = len(names_set)
        spacing = 500 // max(1, count - 1) if count > 1 else 250

        for idx, name in enumerate(sorted(names_set)):
            coordinates[name] = (x_start + idx * spacing, y_start)
        return coordinates

    def draw_nodes(self, coord_dict):
        for name, (x, y) in coord_dict.items():
            self.canvas.create_text(x, y + 20, text=name, font='Arial 10')
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="black")

    def draw_relations(self, relations, coord_a, coord_b, color):
        for a, b in relations:
            if a in coord_a and b in coord_b:
                x1, y1 = coord_a[a]
                x2, y2 = coord_b[b]
                self.canvas.create_line(x1, y1, x2, y2, arrow="last", fill=color)

if __name__ == "__main__":
    root = tk.Tk()
    app = Window1(root)
    root.mainloop()