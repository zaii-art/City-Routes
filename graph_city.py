import os
import matplotlib.pyplot as plt


class Vertex:
    X = 0
    Y = 0

    def __init__(self, value, x, y):
        self.value = value
        self.X = x
        self.Y = y
        self.neighbors = []

    def add_edge(self, other):
        if other not in self.neighbors:
            self.neighbors.append(other)
        if self not in other.neighbors:
            other.neighbors.append(self)

    def __repr__(self):
        return f"Vertex({self.value}, X={self.X}, Y={self.Y})"


class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = []

    def add_vertex(self, value, x, y):
        self.vertices[value] = Vertex(value, x, y)

    def add_edge(self, a, b):
        va, vb = self.vertices[a], self.vertices[b]
        va.add_edge(vb)
        self.edges.append((va, vb))

    def print_adjacency_list(self):
        for v in self.vertices.values():
            print(v.value, (v.X, v.Y), "->",
                  [n.value for n in v.neighbors])

    def draw(self, image_path, save_path):
        img = plt.imread(image_path)
        fig, ax = plt.subplots(figsize=(8, 9))
        ax.imshow(img)
        for a, b in self.edges:
            ax.plot([a.X, b.X], [a.Y, b.Y], color="red",
                    linewidth=2, zorder=2)
        for v in self.vertices.values():
            ax.scatter(v.X, v.Y, s=40, color="blue",
                       edgecolor="white", zorder=3)
            ax.text(v.X + 6, v.Y - 6, v.value, fontsize=7,
                    weight="bold", zorder=4,
                    bbox=dict(facecolor="white", alpha=0.7,
                              pad=0.5, lw=0))
        ax.set_title("Graph Representation of My City")
        ax.axis("off")
        plt.tight_layout()
        try:
            plt.savefig(save_path, dpi=150)
            print("Saved picture to:", save_path)
        except Exception as e:
            print("Could not save picture:", e)
        plt.show()


COORDS = {
    "V1": (24, 498),   "V2": (82, 591),   "V3": (173, 615),  "V4": (257, 611),
    "V5": (232, 545),  "V6": (304, 549),  "V7": (160, 643),  "V8": (187, 688),
    "V9": (318, 752),  "V10": (313, 818), "V11": (348, 831), "V12": (353, 868),
    "V13": (376, 766), "V14": (422, 710), "V15": (499, 721), "V16": (382, 546),
    "V17": (414, 577), "V18": (497, 478), "V19": (505, 554), "V20": (508, 624),
    "V21": (271, 644), "V22": (460, 881), "V23": (308, 1146), "V24": (792, 1133),
    "V25": (852, 1178), "V26": (980, 1063), "V27": (1066, 1126), "V28": (483, 314),
    "V29": (477, 242), "V30": (482, 184), "V31": (547, 261), "V32": (548, 233),
    "V33": (582, 273), "V34": (477, 29),  "V35": (652, 306), "V36": (680, 319),
    "V37": (640, 469), "V38": (555, 602), "V39": (766, 715), "V40": (907, 439),
    "V41": (655, 166), "V42": (615, 37),  "V43": (686, 859), "V44": (710, 818),
    "V45": (575, 749), "V46": (559, 778), "V47": (861, 941), "V48": (950, 817),
    "V49": (1067, 558), "V50": (996, 497), "V51": (857, 767),
}

EDGES = [
    (1, 2), (2, 3), (2, 7), (3, 5), (3, 4), (4, 6), (5, 6), (6, 16),
    (16, 17), (7, 8), (7, 21), (21, 17), (8, 9), (9, 10), (10, 11),
    (11, 12), (11, 13), (13, 14), (14, 15), (17, 19), (15, 22), (22, 23), (22, 24), (32, 31), (29, 31), 
    (24, 25), (24, 26), (26, 27), (17, 18), (17, 20), (18, 19), (19, 20),
    (20, 15), (18, 28), (28, 29), (29, 30), (30, 34), (30, 32), (28, 31),
    (31, 33), (33, 35), (35, 36), (35, 37), (37, 38), (36, 40), (36, 41),
    (41, 42), (40, 50), (40, 39), (50, 49), (50, 51), (49, 48), (48, 47),
    (48, 51), (51, 39), (38, 39), (39, 44), (44, 43), (44, 45), (45, 46),
    (46, 43), (43, 47),
]


def build_city_graph():
    g = Graph()
    for name, (x, y) in COORDS.items():
        g.add_vertex(name, x, y)
    for a, b in EDGES:
        g.add_edge(f"V{a}", f"V{b}")
    return g


def find_image():
    folders = []
    try:
        folders.append(os.path.dirname(os.path.abspath(__file__)))
    except NameError:
        pass
    folders += [os.getcwd(),
                "/storage/emulated/0/Download",
                "/storage/emulated/0/Downloads",
                "/storage/emulated/0"]
    for f in folders:
        p = os.path.join(f, "city_map.jpg")
        if os.path.exists(p):
            return p, f
    return None, None


if __name__ == "__main__":
    graph = build_city_graph()
    print("Vertices:", len(graph.vertices), " Edges:", len(graph.edges))
    graph.print_adjacency_list()

    path, folder = find_image()
    if path is None:
        print("ERROR: city_map.jpg not found. Put it in your Download folder.")
    else:
        graph.draw(path, os.path.join(folder, "result.png"))