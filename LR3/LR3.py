import tkinter as tk
from tkinter import messagebox, filedialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import varCheck as variant

class GraphApp:
    def __init__(self, master):
        self.master = master
        self.master.title("ЛР3")
        main_frame = tk.Frame(master)
        main_frame.pack(fill="both", expand=True)

        control_frame = tk.Frame(main_frame)
        control_frame.pack(side="left", padx=10, pady=10, anchor="n")
        tk.Label(control_frame, text=f"Куліков Максим Миколайович\nГрупа: ІО-{variant.G}\nНомер у списку: {variant.N}\nВаріант: {variant.get_variant_number()}", justify="left").pack(anchor="w", pady=(0, 10))
        tk.Label(control_frame, text="Кількість вершин:").pack(anchor="w")
        self.entry_nodes = tk.Entry(control_frame)
        self.entry_nodes.pack()
        tk.Label(control_frame, text="Кількість ребер:").pack(anchor="w")
        self.entry_edges = tk.Entry(control_frame)
        self.entry_edges.pack()
        tk.Button(control_frame, text="Згенерувати граф", command=self.generate_random_graph).pack(anchor="center", pady=(5, 15))

        tk.Label(control_frame, text="Початкова вершина:").pack(anchor="w")
        self.entry_start = tk.Entry(control_frame)
        self.entry_start.pack()
        tk.Label(control_frame, text="Кінцева вершина:").pack(anchor="w")
        self.entry_end = tk.Entry(control_frame)
        self.entry_end.pack()
        tk.Button(control_frame, text="Знайти шлях (У глибину)", command=self.find_path).pack(anchor="center", pady=5)
        tk.Button(control_frame, text="Завантажити граф з файлу", command=self.load_graph_from_file).pack(anchor="center", pady=(0, 5))
        tk.Button(control_frame, text="Зберегти поточний граф у файл", command=self.save_graph_to_file).pack(anchor="center", pady=(0, 15))

        graph_frame = tk.Frame(main_frame)
        graph_frame.pack(side="right", padx=10, pady=10, expand=True, fill="both")
        self.graph = nx.Graph()
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def generate_random_graph(self):
        self.graph.clear()
        try:
            n = int(self.entry_nodes.get())
            m = int(self.entry_edges.get())
            if n <= 0 or m <= 0:
                raise ValueError
            if m > n * (n - 1) // 2:
                messagebox.showerror("Помилка", "Забагато ребер для заданої кількості вершин.")
                return

            self.graph.add_nodes_from([str(i) for i in range(n)])
            edges = set()
            while len(edges) < m:
                u, v = random.sample(list(self.graph.nodes), 2)
                if (u, v) not in edges and (v, u) not in edges:
                    self.graph.add_edge(u, v)
                    edges.add((u, v))
            self.draw_graph()
        except ValueError:
            messagebox.showerror("Помилка", "Введіть коректні числа для вершин і ребер.")

    def load_graph_from_file(self):
        file_path = filedialog.askopenfilename(title="Відкрити файл з графом", filetypes=[("Текстові файли", "*.txt"), ("Усі файли", "*")])
        if not file_path:
            return
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = f.read().strip()
            pairs = data.split('),')
            edges = []
            nodes_set = set()
            for pair in pairs:
                part = pair.replace('(', '').replace(')', '').strip()
                if not part:
                    continue
                u, v = [x.strip() for x in part.split(',')]
                edges.append((u, v))
                nodes_set.update([u, v])
            if not edges:
                raise ValueError
            self.graph.clear()
            self.graph.add_nodes_from(sorted(nodes_set))
            for u, v in edges:
                self.graph.add_edge(u, v)
            self.draw_graph()
        except Exception:
            messagebox.showerror("Помилка", "Не вдалося зчитати граф з файлу. Перевірте формат.")

    def save_graph_to_file(self):
        if not self.graph.edges:
            messagebox.showerror("Помилка", "Немає ребер для збереження.")
            return
        file_path = filedialog.asksaveasfilename(title="Зберегти граф у файл", defaultextension=".txt", filetypes=[("Текстові файли", "*.txt"), ("Усі файли", "*")])
        if not file_path:
            return
        try:
            edges = list(self.graph.edges)
            text = ", ".join(f"({u}, {v})" for u, v in edges)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)
            messagebox.showinfo("Успіх", "Граф збережено у файл.")
        except Exception:
            messagebox.showerror("Помилка", "Не вдалося зберегти граф.")

    def find_path(self):
        if not self.graph.nodes:
            messagebox.showerror("Помилка", "Спочатку побудуйте або завантажте граф.")
            return
        start = self.entry_start.get().strip()
        end = self.entry_end.get().strip()
        if start not in self.graph or end not in self.graph:
            messagebox.showerror("Помилка", "Вказані вершини відсутні в графі.")
            return
        path = self.dfs_shortest_path(start, end)
        if not path:
            messagebox.showinfo("Результат", "Шлях не знайдено.")
        else:
            messagebox.showinfo("Результат", f"Знайдено шлях: {' -> '.join(path)}")
            self.draw_graph(path)

    def dfs_shortest_path(self, start, end):
        used = {v: False for v in self.graph.nodes}
        shortest = []
        def dfs(v, target, curr):
            nonlocal shortest
            used[v] = True
            curr.append(v)
            if v == target and (not shortest or len(curr) < len(shortest)):
                shortest = curr[:]
            for nbr in self.graph.neighbors(v):
                if not used[nbr]:
                    dfs(nbr, target, curr)
            curr.pop()
            used[v] = False
        dfs(start, end, [])
        return shortest

    def draw_graph(self, highlight=None):
        self.ax.clear()
        pos = nx.spring_layout(self.graph, seed=42)
        nx.draw(self.graph, pos, ax=self.ax, with_labels=True, node_color="lightblue", node_size=600)
        if highlight:
            nx.draw_networkx_edges(self.graph, pos, edgelist=list(zip(highlight, highlight[1:])), edge_color="red", width=3)
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()