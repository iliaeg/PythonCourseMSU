import sys, os
from tkinter import Tk, Label, Entry, Button, Text, StringVar, \
    filedialog, BOTH, END, N, S, W, E
from tkinter.ttk import Frame, Combobox
import networkx as nx
import matplotlib.pyplot as plt
import json

from utils import eprint


def select_file(event=None):
    global filename

    file_path = filedialog.askopenfilename(
        initialdir = os.getcwd(),
        # initialfile = os.path.join(os.getcwd(), "data", "data_fixed.json"),
        title = "Select file",
        filetypes = (("json files","*.json"),("all files","*.*")))
    filename.delete(0, END)
    filename.insert(0, file_path)

def load_file(event):
    global multigraph, dropbox

    multigraph = nx.MultiGraph()

    file_path = filename.get()
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file {file_path} not found")
    # read json
    with open(file_path, "r") as read_file:
        data = json.load(read_file)

    list_of_actors = []
    for actor in data:
        multigraph.add_node(actor['name'])
        list_of_actors.append(actor['name'])

    films = {}
    for actor in data:
        for film in actor['films']:
            films.setdefault(json.dumps(film),[]).append(actor['name'])

    for film, actors in films.items():
        for i in range(len(actors)):
            for j in range(i, len(actors)):
                dictionary = json.loads(film)
                multigraph.add_edge(
                    actors[i],
                    actors[j],
                    title = dictionary['title'],
                    year = dictionary['year'])

    draw_graph = False
    if draw_graph:
        # Need to create a layout when doing
        # separate calls to draw nodes and edges
        pos = nx.spring_layout(multigraph)
        nx.draw_networkx_nodes(multigraph, pos, cmap=plt.get_cmap('jet'), node_size = 500)
        nx.draw_networkx_labels(multigraph, pos)
        nx.draw_networkx_edges(multigraph, pos, edge_color='r', arrows=True)
        nx.draw_networkx_edge_labels(multigraph, pos)
        plt.show()

    dropbox['values'] = list_of_actors
    dropbox.current(0)

def calculate_bacon(event):
    global dropbox, tkvar, bacon_number, path_from, path, multigraph

    to_actor = tkvar.get()
    actors_path = nx.shortest_path(multigraph, source='Kevin Bacon', target=to_actor)

    bacon_number['text'] = len(actors_path) - 1
    path_from['text'] = "Path from Kevin Bacon to " + to_actor

    path.delete(1.0, END)
    path_str = "\n"
    for i in range(1, len(actors_path)):
        edge = multigraph.get_edge_data(actors_path[i - 1], actors_path[i])
        path_str += actors_path[i] + " : \n" \
            + '\t' + str(edge[0]['title']) + ", " + str(edge[0]['year']) + '\n\n'
    path.insert(1.0, path_str)

class MainWindow(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        global filename, dropbox, tkvar, bacon_number, path_from, path

        paddingx = 10
        paddingy = 10

        self.master.title("Bacon Number")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(0, pad=3,weight=2)
        self.columnconfigure(1, pad=3,weight=2)
        self.columnconfigure(2, pad=3,weight=4)
        self.columnconfigure(3, pad=3,weight=2)

        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)

        data_lbl = Label(self, text="Data file")
        data_lbl.grid(row=0, column=0, columnspan=2)
        filename = Entry(self)
        filename.grid(row=1, column=0, columnspan=2, padx=paddingx, sticky=W+E)
        select_btn = Button(self, text="Select", command=select_file)
        select_btn.grid(row=2, column=0, padx=paddingx, sticky=W+E)
        load_btn = Button(self, text="Load")
        load_btn.grid(row=2, column=1, padx=paddingx, sticky=W+E)
        load_btn.bind("<Button-1>", load_file)

        select_lbl = Label(self, text="Select actor")
        select_lbl.grid(row=0, column=2, columnspan=2)
        tkvar = StringVar()
        dropbox = Combobox(self, textvariable = tkvar,state="readonly")
        dropbox.grid(row=1, column=2, columnspan=2, padx=paddingx, sticky=W+E)
        dropbox.bind('<<ComboboxSelected>>', calculate_bacon)

        number_lbl = Label(self, text="Bacon number:")
        number_lbl.grid(row=3, column=0, columnspan=2, sticky=E)
        bacon_number = Label(self, text="")
        bacon_number.grid(row=3, column=2, columnspan=2, sticky=W)
        path_from = Label(self, text="Path from Kevin Bacon to ..")
        path_from.grid(row=4, column=0, columnspan=4)
        path = Text(self)
        path.grid(row=5, column=0, columnspan=4, padx=paddingx, pady=paddingy, sticky=E+W+S+N)


def main(argv):
    try:

        root = Tk()
        MainWindow()
        root.mainloop()

        return 0

    except FileNotFoundError as ex:
        eprint("FileNotFoundError exception caught: \n", ex)
    except Exception as ex:
        eprint("An exception caught: ", ex)

    return 1

if __name__ == "__main__":
    main(sys.argv[:])