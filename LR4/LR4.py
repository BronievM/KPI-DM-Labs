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
        self.master.title("ЛР4")
        main = tk.Frame(master)
        main.pack(fill="both", expand=True)
        canv = tk.Frame(main)
        canv.pack(side="left", padx=10, pady=10, anchor="n")
        tk.Label(canv, text=(f"Куліков Максим Миколайович\nГрупа: ІО-{variant.G}\nНомер у списку: {variant.N}\nВаріант: {variant.get_variant_number()}")).pack(anchor="w", pady=(0,10))
        tk.Label(canv, text="Кількість вершин:").pack(anchor="w")
        self.entry_n = tk.Entry(canv)
        self.entry_n.pack()
        tk.Button(canv, text="Генерувати випадкову матрицю", command=self.generate_random_matrix).pack(fill="x", pady=(5,5))
        tk.Label(canv, text="Матриця суміжності:").pack(anchor="w")
        self.text_matrix = tk.Text(canv, width=20, height=10)
        self.text_matrix.pack()
        tk.Button(canv, text="Побудувати граф на основі матриці", command=self.build_from_matrix).pack(fill="x", pady=(5,5))
        tk.Button(canv, text="Завантажити матрицю з файлу", command=self.load_matrix).pack(fill="x", pady=(5,5))
        tk.Button(canv, text="Зберегти матрицю у файл", command=self.save_matrix).pack(fill="x", pady=(5,5))
        tk.Button(canv, text="Розфарбувати граф", command=self.color_graph).pack(fill="x", pady=(5,5))
        graph_frame = tk.Frame(main)
        graph_frame.pack(side="right", padx=10, pady=10, expand=True, fill="both")
        self.graph = nx.Graph()
        self.fig, self.ax = plt.subplots(figsize=(6,6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def generate_random_matrix(self):
        try:
            n = int(self.entry_n.get())
            if n<=0: raise ValueError
        except:
            messagebox.showerror("Помилка","Невірне число вершин")
            return
        mat = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1,n):
                if random.choice([0,1]):
                    mat[i][j]=mat[j][i]=1
        text = "\n".join(" ".join(str(x) for x in row) for row in mat)
        self.text_matrix.delete("1.0","end")
        self.text_matrix.insert("1.0", text)
        self.build_from_matrix()

    def parse_matrix(self):
        text = self.text_matrix.get("1.0","end").strip().splitlines()
        mat = []
        for line in text:
            row = [int(x) for x in line.split()]
            mat.append(row)
        return mat

    def build_from_matrix(self):
        try:
            mat = self.parse_matrix()
            n = len(mat)
            for row in mat:
                if len(row)!=n: raise ValueError
        except:
            messagebox.showerror("Помилка","Невірна матриця")
            return
        self.graph.clear()
        nodes = [str(i+1) for i in range(n)]
        self.graph.add_nodes_from(nodes)
        for i in range(n):
            for j in range(i+1,n):
                if mat[i][j]==1:
                    self.graph.add_edge(nodes[i],nodes[j])
        self.draw_graph()

    def load_matrix(self):
        path = filedialog.askopenfilename(filetypes=[("Текст","*.txt")])
        if not path: return
        try:
            with open(path, encoding="utf-8") as f:
                data = f.read()
            self.text_matrix.delete("1.0","end")
            self.text_matrix.insert("1.0", data)
            self.build_from_matrix()
        except:
            messagebox.showerror("Помилка","Не вдалося завантажити файл")

    def save_matrix(self):
        try:
            mat = self.parse_matrix()
        except:
            messagebox.showerror("Помилка","Немає матриці")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Текст","*.txt")])
        if not path: return
        try:
            with open(path,"w",encoding="utf-8") as f:
                for row in mat:
                    f.write(" ".join(str(x) for x in row)+"\n")
            messagebox.showinfo("Готово","Матрицю збережено")
        except:
            messagebox.showerror("Помилка","Не вдалося зберегти файл")

    def generate_assignments(self, n, k):
        assignment = [0] * n
        while True:
            yield assignment[:]
            i = n - 1
            while i >= 0 and assignment[i] == k - 1:
                assignment[i] = 0
                i -= 1
            if i < 0:
                break
            assignment[i] += 1

    def is_valid(self,c):
        for u,v in self.graph.edges():
            if c[u]==c[v]:
                return False
        return True

    def brute_force(self):
        nodes=list(self.graph.nodes())
        n=len(nodes)
        for k in range(1,n+1):
            for assign in self.generate_assignments(n, k):
                c={nodes[i]:assign[i] for i in range(n)}
                if self.is_valid(c): return k,c
        return n,{nodes[i]:i for i in range(n)}

    def color_graph(self):
        if not self.graph.nodes:
            messagebox.showerror("Помилка","Спершу створіть граф")
            return
        k,c = self.brute_force()
        messagebox.showinfo("Результат",f"Кількість кольорів: {k}")
        cmap = plt.get_cmap("hsv")
        colors = [cmap(i / k) for i in range(k)]
        node_colors = [colors[c[node]] for node in self.graph.nodes()]
        self.draw_graph(node_colors=node_colors)

    def draw_graph(self,node_colors=None):
        self.ax.clear()
        pos=nx.spring_layout(self.graph,seed=42)
        nx.draw(self.graph,pos,ax=self.ax,with_labels=True,node_color=node_colors or "lightblue",node_size=600,edge_color="gray")
        self.canvas.draw()

if __name__ == "__main__":
    root=tk.Tk()
    GraphApp(root)
    root.mainloop()
