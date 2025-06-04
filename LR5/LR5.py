import tkinter as tk
from tkinter import messagebox
import random
import varCheck as variant

class BinaryVectorApp:
    def __init__(self, master):
        self.master = master
        master.title("ЛР5")
        frame = tk.Frame(master)
        frame.pack(padx=10, pady=10)
        tk.Label(frame, text=(f"Куліков Максим Миколайович\nГрупа: ІО-{variant.G}\nНомер у списку: {variant.N}\nВаріант: {variant.get_variant_number()}")).pack(pady=(0, 10))
        tk.Label(frame, text="Введіть n (довжина вектора):").pack(anchor="w")
        self.entry_n = tk.Entry(frame)
        self.entry_n.pack(fill="x")
        tk.Label(frame, text="Введіть m (кількість векторів):").pack(anchor="w")
        self.entry_m = tk.Entry(frame)
        self.entry_m.pack(fill="x", pady=(0, 10))
        tk.Button(frame, text="Згенерувати вектори", command=self.run_algorithm).pack(fill="x", pady=5)
        tk.Label(frame, text="Результат:").pack(anchor="w")
        self.output_text = tk.Text(frame, height=15, width=50)
        self.output_text.pack()

    def run_algorithm(self):
        try:
            n = int(self.entry_n.get())
            m = int(self.entry_m.get())
            if n <= 0 or m <= 0 or n > variant.get_NZK() or m > n:
                raise ValueError
        except:
            messagebox.showerror("Помилка", f"Введіть коректні числа n і m (n ≤ {variant.get_NZK()}).")
            return

        b = [random.randint(0, 1) for _ in range(n)]
        result = ["".join(map(str, b))]

        for _ in range(m - 1):
            i = n - 1
            while i >= 0 and b[i] == 1:
                b[i] = 0
                i -= 1
            if i < 0:
                break
            b[i] = 1
            result.append("".join(map(str, b)))

        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", "\n".join(result))


if __name__ == "__main__":
    root = tk.Tk()
    app = BinaryVectorApp(root)
    root.mainloop()
