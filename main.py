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


def add_node():
    try:
        current_node = current_node_txt.get()
        next_node = next_node_txt.get()
        weight = int(weight_txt.get())

        if not exists_node(current_node, next_node):
            treeview.insert("", "end", values=(current_node, next_node, weight))

        clear_text_entries()

    except ValueError as error:
        messagebox.showerror("Error", f"Ha ocurrido un error: {str(error)}")


def delete_node():
    selected_item = treeview.selection()
    if selected_item:
        treeview.delete(selected_item)

def show_network():
    network = get_network()
    # Network window
    window = Tk()
    window.title("Visualización de la red")
    window.resizable(False, False)

    if len(network) == 0:
        messagebox.showwarning("No se puede procesar la red", "La tabla no contiene datos a procesar")
        return
    g = nx.Graph()
    for node in network:
        g.add_edge(node[0], node[1], weight=node[2])

    # Figura de matplotlib
    figure = plt.figure(figsize=(5, 5))
    ax = figure.add_subplot(111)

    pos = nx.spring_layout(g, seed=7)
    nx.draw_networkx(g, pos, node_size=700, with_labels=True, ax=ax)
    edges_labels = nx.get_edge_attributes(g, "weight")
    nx.draw_networkx_edge_labels(g, pos, edges_labels, ax=ax)

    # Creación del widget
    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Botones
    close_window_btn = Button(window, text="Cerrar", command=window.destroy)

    close_window_btn.pack()

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

    # Creación del Treeview (que funcionará como tabla)
    global treeview
    treeview = ttk.Treeview(window, show="headings", selectmode="browse")

    # Columnas de la tabla
    treeview["columns"] = ("nodo-actual", "nodo-siguiente", "peso")
    for heading in treeview["columns"]:
        treeview.heading(heading, text=heading.capitalize().replace("-", " "))

    # Mostrando la tabla
    treeview.pack(expand=True, fill=BOTH)

    # Cajas de texto
    global current_node_txt
    global next_node_txt
    global weight_txt

    label_current_node = Label(window, text="Nodo actual: ")
    current_node_txt = Entry(window)

    label_next_node = Label(window, text="Nodo siguiente: ")
    next_node_txt = Entry(window)

    label_weight = Label(window, text="Peso: ")
    weight_txt = Entry(window)

    label_current_node.pack()
    current_node_txt.pack()

    label_next_node.pack()
    next_node_txt.pack()

    label_weight.pack()
    weight_txt.pack()

    # Botones
    add_node_btn = Button(window, text="Agregar nodo", command=add_node)
    delete_node_btn = Button(window, text="Eliminar fila seleccionada", command=delete_node)
    get_network_btn = Button(window, text="Ver red", command=show_network)

    add_node_btn.pack()
    delete_node_btn.pack()
    get_network_btn.pack()

    window.mainloop()


if __name__ == "__main__":
    app()
