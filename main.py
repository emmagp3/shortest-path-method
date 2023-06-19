from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


def exists_node(current_node, next_node):
    elements = treeview.get_children()

    for element in elements:
        if treeview.item(element)["values"][0] == current_node and treeview.item(element)["values"][1] == next_node:
            return True
        return False


def clear_text_entries():
    current_node_txt.delete(0, END)
    next_node_txt.delete(0, END)
    weight_txt.delete(0, END)


def is_text_entries_empty():
    return len(current_node_txt.get()) == 0 or len(next_node_txt.get()) == 0 or len(weight_txt.get()) == 0


def add_node():
    try:
        current_node = current_node_txt.get()
        next_node = next_node_txt.get()
        weight = int(weight_txt.get())

        if is_text_entries_empty():
            messagebox.showerror("No se puede agregar el nodo", "Rellena todos los campos")
            return
        if weight <= 0:
            messagebox.showerror("Peso inválido", "El peso no puede ser menor o igual a cero")
            return
        if not exists_node(current_node, next_node):
            treeview.insert("", "end", values=(current_node, next_node, weight))
            clear_text_entries()

    except ValueError as error:
        messagebox.showerror("Error", f"Ha ocurrido un error: {str(error)}")


def delete_node():
    selected_item = treeview.selection()
    if selected_item:
        treeview.delete(selected_item[0])


def solve_network(start, end, nt_graph):
    try:
        shortest_path = nx.dijkstra_path(nt_graph, start, end)
        n_shortest_path = nx.dijkstra_path_length(nt_graph, start, end)
        messagebox.showinfo("Resolución", f"La ruta más corta es: {shortest_path}\nLa solución óptima es: {n_shortest_path}")
    except Exception as error:
        messagebox.showerror("Error en el cálculo", str(error))


def show_network():
    global network
    network = get_network()
    if len(network) == 0:
        messagebox.showwarning("No se puede procesar la red", "La tabla no contiene datos a procesar")
        return

    # Network window
    window = Tk()
    window.title("Visualización de la red")
    window.resizable(False, False)

    container = Frame(window, padx=20, pady=20)
    container.pack(fill="both", expand=True)

    # Creación del grafo
    global network_graph
    network_graph = nx.Graph()
    for node in network:
        network_graph.add_edge(str(node[0]), str(node[1]), weight=node[2])

    # Figura de matplotlib
    figure = plt.figure(figsize=(5, 5))
    ax = figure.add_subplot(111)

    pos = nx.spring_layout(network_graph, seed=7)
    nx.draw_networkx(network_graph, pos, node_size=700, with_labels=True, ax=ax)
    edges_labels = nx.get_edge_attributes(network_graph, "weight")
    nx.draw_networkx_edge_labels(network_graph, pos, edges_labels, ax=ax)

    # Creación del widget
    canvas = FigureCanvasTkAgg(figure, master=container)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Botones
    close_window_btn = Button(container, text="Cerrar", command=window.destroy, padx=10)
    close_window_btn.pack(side="right", fill="x")
    solve_network_btn = Button(
        container,
        text="Resolver red",
        command=lambda: solve_network(
            start_node_txt.get(),
            final_node_txt.get(),
            network_graph
        ), padx=10
    )
    solve_network_btn.pack(side="right", fill="x")

    # Cajas de texto y labels
    global final_node_txt
    global start_node_txt
    final_node_txt = Entry(container)
    start_node_txt = Entry(container)

    start_node_label = Label(container, text="Nodo origen")
    final_node_label = Label(container, text="Nodo destino")

    start_node_label.pack(side="left")
    start_node_txt.pack(side="left")

    final_node_label.pack(side="left")
    final_node_txt.pack(side="left")

    window.mainloop()


def get_network():
    network = []
    for item in treeview.get_children():
        network.append(treeview.item(item)["values"])
    return network


def app():
    window = Tk()
    window.title("Método de la ruta más corta")
    window.resizable(False, False)

    container = Frame(window, padx=20, pady=20)
    container.pack(fill="both", expand=True)

    # Creación del Treeview (que funcionará como tabla)
    global treeview
    treeview = ttk.Treeview(
        container,
        show="headings",
        selectmode="browse"
    )

    # Columnas de la tabla
    treeview["columns"] = ("nodo-actual", "nodo-siguiente", "peso")
    for heading in treeview["columns"]:
        treeview.heading(heading, text=heading.capitalize().replace("-", " "))

    # Mostrando la tabla
    treeview.pack(expand=True, fill=BOTH)

    # Cajas de texto y labels
    global current_node_txt
    global next_node_txt
    global weight_txt

    label_current_node = Label(container, text="Nodo actual: ")
    current_node_txt = Entry(container)

    label_next_node = Label(container, text="Nodo siguiente: ")
    next_node_txt = Entry(container)

    label_weight = Label(container, text="Peso: ")
    weight_txt = Entry(container)

    label_current_node.pack(side="left")
    current_node_txt.pack(side="left")

    label_next_node.pack(side="left")
    next_node_txt.pack(side="left")

    label_weight.pack(side="left")
    weight_txt.pack(side="left")

    # Botones
    add_node_btn = Button(
        container,
        text="Agregar nodo",
        command=add_node
    )

    delete_node_btn = Button(
        container,
        text="Eliminar fila seleccionada",
        command=delete_node
    )

    get_network_btn = Button(
        container,
        text="Ver red",
        command=show_network
    )

    add_node_btn.pack(side="left", pady=5, padx=10, fill="x")
    delete_node_btn.pack(side="left", pady=5, padx=10, fill="x")
    get_network_btn.pack(side="left", pady=5, padx=10, fill="x")

    window.mainloop()


if __name__ == "__main__":
    app()
