from tkinter import Tk, Toplevel, Canvas, Label, LabelFrame, Button, Listbox, Entry, Radiobutton, StringVar, TOP, LEFT, END
from tkinter.messagebox import showerror
from random import randint
from math import sin, cos, atan, pi


class MainWindow:
    def __init__(self):
        self.__SCREEN_WIDTH = 500
        self.__SCREEN_HEIGHT = 500
        self.__POINTS_RADIUS = 50
        self.__coords = [-self.__POINTS_RADIUS, -self.__POINTS_RADIUS]
        self.__zoom = 4
        self.__selection = ""
        self.__points = {}
        self.__subwindow = None
        self.__window = Tk()
        self.__window.title("Graphe")
        self.__canvas = Canvas(self.__window, width=self.__SCREEN_WIDTH, height=self.__SCREEN_HEIGHT, bg="white")
        self.__canvas.pack(side=LEFT, anchor="n", padx=5, pady=5)
        self.__canvas.bind("<Button-1>", self.__mouse_left_down)
        self.__canvas.bind("<ButtonRelease-1>", self.__mouse_left_up)
        self.__canvas.bind("<Button-3>", self.__mouse_right_down)
        self.__canvas.bind("<ButtonRelease-3>", self.__mouse_right_up)
        self.__canvas.bind("<Motion>", self.__mouse_motion)
        self.__canvas.bind("<MouseWheel>", self.__mouse_wheel)
        self.__canvas.bind("<Delete>", self.__del_point)
        frame = LabelFrame(self.__window, borderwidth=0, padx=5, pady=5)
        frame.pack(side=LEFT, fill="both", expand="no", padx=0, pady=0)
        frame2 = LabelFrame(frame, text="Affichage :", padx=5, pady=5)
        frame2.pack(side=TOP, fill="both", expand="no", padx=0, pady=5)
        Button(frame2, text="Zoom -", command=self.__zoom_out).pack(side=TOP, anchor="w", padx=0, pady=0)
        Button(frame2, text="Zoom +", command=self.__zoom_in).pack(side=TOP, anchor="w", padx=0, pady=0)
        frame3 = LabelFrame(frame2, text="Dimensions :", padx=5, pady=5)
        frame3.pack(side=TOP, anchor="w", fill="both", expand="no", padx=0, pady=5)
        frame4 = LabelFrame(frame3, borderwidth=0, padx=0, pady=0)
        frame4.pack(side=TOP, anchor="w", fill="both", expand="no", padx=0, pady=0)
        Label(frame4, text="Largeur : ").pack(side=LEFT, anchor="w", padx=0, pady=0)
        self.__entry_width = Entry(frame4, width=5)
        self.__entry_width.pack(side=LEFT, padx=0, pady=0)
        self.__entry_width.insert(0, str(self.__SCREEN_WIDTH))
        self.__entry_width.bind("<Return>", self.__change_dimensions)
        Label(frame4, text="px").pack(side=LEFT, anchor="w", padx=0, pady=0)
        frame4 = LabelFrame(frame3, borderwidth=0, padx=0, pady=0)
        frame4.pack(side=TOP, anchor="w", fill="both", expand="no", padx=0, pady=0)
        Label(frame4, text="Hauteur : ").pack(side=LEFT, anchor="w", padx=0, pady=0)
        self.__entry_height = Entry(frame4, width=5)
        self.__entry_height.pack(side=LEFT, padx=0, pady=0)
        self.__entry_height.insert(0, str(self.__SCREEN_HEIGHT))
        self.__entry_height.bind("<Return>", self.__change_dimensions)
        Label(frame4, text="px").pack(side=LEFT, anchor="w", padx=0, pady=0)
        Button(frame3, text="Appliquer", command=self.__change_dimensions).pack(side=TOP, anchor="w", padx=0, pady=0)
        Label(frame2, text="Clique gauche : bouger les points").pack(side=TOP, anchor="w", padx=0, pady=0)
        Label(frame2, text="Clique droit : bouger la caméra").pack(side=TOP, anchor="w", padx=0, pady=0)
        Label(frame2, text="Molette : zoomer/dézoomer").pack(side=TOP, anchor="w", padx=0, pady=0)
        Label(frame2, text="Suppr : supprimer un point").pack(side=TOP, anchor="w", padx=0, pady=0)
        frame2 = LabelFrame(frame, text="Arêtes :", padx=5, pady=5)
        frame2.pack(side=TOP, fill="both", expand="no", padx=0, pady=5)
        self.__list_edges = Listbox(frame2, width=34, height=10)
        self.__list_edges.pack(side=TOP, anchor="w", padx=0, pady=0)
        self.__list_edges.bind("<Delete>", self.__del_edge)
        Button(frame2, text="Supprimer", command=self.__del_edge).pack(side=TOP, anchor="w", padx=0, pady=0)
        frame3 = LabelFrame(frame2, text="Ajouter une arète (ex : A-B ou A>B) :", padx=5, pady=5)
        frame3.pack(side=TOP, anchor="w", fill="both", expand="no", padx=0, pady=5)
        self.__entry_edge = Entry(frame3, width=23)
        self.__entry_edge.pack(side=LEFT, padx=0, pady=0)
        self.__entry_edge.bind("<Return>", self.__add_edge)
        Button(frame3, text="Ajouter", command=self.__add_edge).pack(side=LEFT, padx=0, pady=0)
        frame = LabelFrame(self.__window, text="Simulation :", padx=5, pady=5)
        frame.pack(side=LEFT, anchor="n", expand="no", padx=5, pady=10)
        Button(frame, text="Simulation", command=self.__add_subwindow).pack(side=TOP, anchor="w", padx=0, pady=0)
        Label(frame, text="Fréquences :").pack(side=TOP, anchor="w", padx=0, pady=0)
        self.__list_frequences = Listbox(frame, width=30, height=30)
        self.__list_frequences.pack(side=TOP, anchor="w", padx=0, pady=0)
        self.__window.mainloop()

    def get_window(self):
        return self.__window

    def is_point(self, point):
        return point in self.__points

    def __change_dimensions(self, event=None):
        try:
            width = int(self.__entry_width.get())
            height = int(self.__entry_height.get())
            if width > 0 and height > 0:
                self.__SCREEN_WIDTH = width
                self.__SCREEN_HEIGHT = height
                self.__canvas["width"] = self.__SCREEN_WIDTH
                self.__canvas["height"] = self.__SCREEN_HEIGHT
                self.__show()
            else:
                showerror("Erreur", "Dimensions invalides")
        except:
            showerror("Erreur", "Dimensions invalides")

    def __mouse_left_down(self, event):
        self.__canvas.focus_set()
        for i in self.__points:
            if (self.__points[i].get_x()-self.__coords[0]-(self.__POINTS_RADIUS+51.2*len(i)/2))/self.__zoom < event.x < (self.__points[i].get_x()-self.__coords[0]+self.__POINTS_RADIUS+51.2*len(i)/2)/self.__zoom and (self.__points[i].get_y()-self.__coords[1]-self.__POINTS_RADIUS)/self.__zoom < event.y < (self.__points[i].get_y()-self.__coords[1]+self.__POINTS_RADIUS)/self.__zoom:
                self.__selection = i
                break

    def __mouse_left_up(self, event):
        if type(self.__selection) == str:
            self.__selection = ""

    def __mouse_right_down(self, event):
        self.__selection = [event.x, event.y]

    def __mouse_right_up(self, event):
        if type(self.__selection) == list:
            self.__selection = ""

    def __mouse_motion(self, event):
        if type(self.__selection) == list:
            self.__coords = [self.__coords[0]-(event.x-self.__selection[0])*self.__zoom, self.__coords[1]-(event.y-self.__selection[1])*self.__zoom]
            self.__selection = [event.x, event.y]
            self.__show()
        elif self.__selection != "":
            self.__points[self.__selection].set_coords(self.__coords[0]+event.x*self.__zoom, self.__coords[1]+event.y*self.__zoom)
            self.__show()

    def __mouse_wheel(self, event):
        if event.delta < 0:
            self.__zoom_out()
        else:
            self.__zoom_in()

    def __zoom_out(self):
        if self.__zoom < 32:
            self.__zoom *= 2
            self.__show()

    def __zoom_in(self):
        if self.__zoom > 1:
            self.__zoom /= 2
            self.__show()

    def __del_point(self, event):
        if type(self.__selection) == str and self.__selection != "":
            for i in self.__points:
                if i != self.__selection:
                    keys = list(self.__points[i].list_adjs.keys())
                    for j in keys:
                        if j[:-1] == self.__selection:
                            del self.__points[i].list_adjs[j]
            del self.__points[self.__selection]
            i = 0
            while i < self.__list_edges.size():
                if self.__selection in self.__list_edges.get(i):
                    self.__list_edges.delete(i)
                else:
                    i += 1
            self.__selection = ""
            self.__show()

    def __del_edge(self, event=None):
        edge = self.__list_edges.get("active")
        if edge:
            for i in range(self.__list_edges.size()):
                if self.__list_edges.get(i) == edge:
                    self.__list_edges.delete(i)
                    break
            if "-" in edge:
                edge = edge.split("-")+["-"]
            else:
                edge = edge.split(">")+[">"]
            self.__points[edge[0]].del_adj(edge[1]+edge[2])
            if edge[2] == "-" and edge[0] != edge[1]:
                self.__points[edge[1]].del_adj(edge[0]+edge[2])
            self.__show()

    def __add_edge(self, event=None):
        if self.__entry_edge.get().count("-")+self.__entry_edge.get().count(">") == 1:
            if "-" in self.__entry_edge.get():
                inpt = self.__entry_edge.get().split("-")+["-"]
            else:
                inpt = self.__entry_edge.get().split(">")+[">"]
        else:
            inpt = []
        if not (len(inpt) == 3 and inpt[0] != "" and inpt[1] != ""):
            inpt = False
            showerror("Erreur", "Entrée invalide")
        elif inpt:
            if not inpt[0] in self.__points:
                self.__points[inpt[0]] = Point(inpt[0])
            if not inpt[1] in self.__points:
                self.__points[inpt[1]] = Point(inpt[1])
            self.__points[inpt[0]].add_adj(inpt[1]+inpt[2])
            if inpt[2] == "-" and inpt[0] != inpt[1]:
                self.__points[inpt[1]].add_adj(inpt[0]+inpt[2])
            self.__list_edges.insert("end", inpt[0]+inpt[2]+inpt[1])
            self.__show()
            self.__entry_edge.delete(0, END)

    def __show(self):
        self.__canvas.delete("all")
        already = []
        for i in self.__points:
            x = (self.__points[i].get_x()-self.__coords[0])/self.__zoom
            y = (self.__points[i].get_y()-self.__coords[1])/self.__zoom
            adjs = {}
            for j in self.__points[i].list_adjs:
                if not j[:-1] in already:
                    if not j[:-1] in adjs:
                        adjs[j[:-1]] = [0, 0, 0]
                    if j[-1] == "-":
                        adjs[j[:-1]][0] += self.__points[i].list_adjs[j]
                    else:
                        adjs[j[:-1]][1] += self.__points[i].list_adjs[j]
            for j in self.__points:
                if j != i and i+">" in self.__points[j].list_adjs:
                    if not j in adjs:
                        adjs[j] = [0, 0, self.__points[j].list_adjs[i+">"]]
                    else:
                        adjs[j][2] += self.__points[j].list_adjs[i+">"]
            for j in adjs:
                if not j in already:
                    if j == i:
                        multi = (self.__POINTS_RADIUS+51.2*len(j)/2)*2/self.__zoom
                        for k in range(sum(adjs[j])):
                            x2 = x+cos(2*pi/sum(adjs[j])*k)*multi
                            y2 = y+sin(2*pi/sum(adjs[j])*k)*multi
                            x3 = x+cos(2*pi/sum(adjs[j])*(k+0.25))*multi
                            y3 = y+sin(2*pi/sum(adjs[j])*(k+0.25))*multi
                            self.__canvas.create_line(x, y, x2, y2)
                            self.__canvas.create_line(x, y, x3, y3)
                            self.__canvas.create_line(x2, y2, x3, y3)
                            if k >= adjs[j][0]:
                                angle = pi/2-atan(abs(x2-x3)/abs(y2-y3))
                                if x2 < x3 and y2 > y3:
                                    angle = pi-angle
                                elif x2 > x3 and y2 < y3:
                                    angle = 2*pi-angle
                                elif x2 < x3 and y2 < y3:
                                    angle += pi
                                self.__canvas.create_line(x3, y3, x3+cos(angle-pi/12)*self.__POINTS_RADIUS/self.__zoom, y3+sin(angle-pi/12)*self.__POINTS_RADIUS/self.__zoom)
                                self.__canvas.create_line(x3, y3, x3+cos(angle+pi/12)*self.__POINTS_RADIUS/self.__zoom, y3+sin(angle+pi/12)*self.__POINTS_RADIUS/self.__zoom)
                    else:
                        x2 = (self.__points[j].get_x()-self.__coords[0])/self.__zoom
                        y2 = (self.__points[j].get_y()-self.__coords[1])/self.__zoom
                        if x == x2:
                            if y <= y2:
                                angle = 3*pi/2
                            else:
                                angle = pi/2
                        elif y == y2:
                            if x <= x2:
                                angle = pi
                            else:
                                angle = 0
                        else:
                            angle = pi/2-atan(abs(x-x2)/abs(y-y2))
                            if x < x2 and y > y2:
                                angle = pi-angle
                            elif x > x2 and y < y2:
                                angle = 2*pi-angle
                            elif x < x2 and y < y2:
                                angle += pi
                        for k in range(sum(adjs[j])):
                            multi = (self.__POINTS_RADIUS*k/sum(adjs[j]))*(k%2*2-1)/self.__zoom
                            self.__canvas.create_line(x+cos(angle+pi/2)*multi, y+sin(angle+pi/2)*multi, x2+cos(angle+pi/2)*multi, y2+sin(angle+pi/2)*multi)
                            x3 = (x+x2)/2+cos(angle+pi/2)*multi
                            y3 = (y+y2)/2+sin(angle+pi/2)*multi
                            if k >= adjs[j][0]+adjs[j][1]:
                                self.__canvas.create_line(x3, y3, x3+cos(angle-13*pi/12)*self.__POINTS_RADIUS/self.__zoom, y3+sin(angle-13*pi/12)*self.__POINTS_RADIUS/self.__zoom)
                                self.__canvas.create_line(x3, y3, x3+cos(angle+13*pi/12)*self.__POINTS_RADIUS/self.__zoom, y3+sin(angle+13*pi/12)*self.__POINTS_RADIUS/self.__zoom)
                            elif k >= adjs[j][0]:
                                self.__canvas.create_line(x3, y3, x3+cos(angle-pi/12)*self.__POINTS_RADIUS/self.__zoom, y3+sin(angle-pi/12)*self.__POINTS_RADIUS/self.__zoom)
                                self.__canvas.create_line(x3, y3, x3+cos(angle+pi/12)*self.__POINTS_RADIUS/self.__zoom, y3+sin(angle+pi/12)*self.__POINTS_RADIUS/self.__zoom)
            if 0 < x+(self.__POINTS_RADIUS+51.2*len(i)/2)/self.__zoom and x-(self.__POINTS_RADIUS+51.2*len(i)/2)/self.__zoom < self.__SCREEN_WIDTH and 0 < y+self.__POINTS_RADIUS/self.__zoom and y-self.__POINTS_RADIUS/self.__zoom < self.__SCREEN_HEIGHT:
                self.__canvas.create_oval(x-(self.__POINTS_RADIUS+51.2*len(i)/2)/self.__zoom, y-self.__POINTS_RADIUS/self.__zoom, x+(self.__POINTS_RADIUS+51.2*len(i)/2)/self.__zoom, y+self.__POINTS_RADIUS/self.__zoom, fill="blue")
                self.__canvas.create_text(x, y, text=i, font="Consolas "+str(int(64/self.__zoom)))
            already += [i]

    def __add_subwindow(self):
        self.__subwindow = SubWindow(self)

    def close_subwindow(self):
        del self.__subwindow
        self.__subwindow = None

    def simulate(self, start_point, nb_jumps, nb_simulations):
        results = {i : 0 for i in self.__points}
        for i in range(nb_simulations):
            if start_point == 0:
                point = list(self.__points.keys())[randint(0, len(self.__points.keys())-1)]
            else:
                point = start_point
            for j in range(nb_jumps):
                list_next = [k[:-1] for k in self.__points[point].list_adjs for l in range(self.__points[point].list_adjs[k])]
                if list_next:
                    point = list_next[randint(0, len(list_next)-1)]
                else:
                    break
            results[point] += 1
        self.__list_frequences.delete(0, self.__list_frequences.size())
        for i in results:
            self.__list_frequences.insert("end", i+" : "+str(results[i]/nb_simulations))

class SubWindow:
    def __init__(self, mainwindow):
        self.__mainwindow = mainwindow
        self.__window = Toplevel(mainwindow.get_window())
        self.__window.grab_set()
        self.__window.resizable(width=False, height=False)
        self.__window.protocol("WM_DELETE_WINDOW",self.__close)
        self.__window.title("Simulation")
        frame = LabelFrame(self.__window, text="Point de départ :", padx=5, pady=5)
        frame.pack(side=TOP, fill="both", expand="no", padx=5, pady=5)
        self.__mode_start = StringVar()
        Radiobutton(frame, variable=self.__mode_start, text="Point aléatoire", value="1").pack(side=TOP, anchor="w", padx=0, pady=0)
        frame2 = LabelFrame(frame, borderwidth=0, padx=0, pady=0)
        frame2.pack(side=TOP, fill="both", expand="no", padx=0, pady=0)
        Radiobutton(frame2, variable=self.__mode_start, text="Point défini : ", value="2").pack(side=LEFT, anchor="w", padx=0, pady=0)
        self.__entry_point = Entry(frame2, width=10)
        self.__entry_point.pack(side=LEFT, padx=0, pady=0)
        self.__mode_start.set("1")
        frame = LabelFrame(self.__window, borderwidth=0, padx=0, pady=0)
        frame.pack(side=TOP, fill="both", expand="no", padx=5, pady=5)
        Label(frame, text="Nombre de sauts : ").pack(side=LEFT, padx=0, pady=0)
        self.__entry_jumps = Entry(frame, width=10)
        self.__entry_jumps.pack(side=LEFT, padx=0, pady=0)
        frame = LabelFrame(self.__window, borderwidth=0, padx=0, pady=0)
        frame.pack(side=TOP, fill="both", expand="no", padx=5, pady=5)
        Label(frame, text="Nombre de simulations : ").pack(side=LEFT, padx=0, pady=0)
        self.__entry_simulations = Entry(frame, width=10)
        self.__entry_simulations.pack(side=LEFT, padx=0, pady=0)
        Button(self.__window, text="Valider", command=self.__simulate).pack(side=TOP, anchor="w", padx=0, pady=0)
        self.__window.mainloop()

    def __close(self):
        self.__window.destroy()
        self.__mainwindow.close_subwindow()

    def __simulate(self):
        is_valid = 1
        start_point = self.__mode_start.get()
        if start_point == "2" and not self.__mainwindow.is_point(self.__entry_point.get()):
            is_valid = 0
            showerror("Erreur", "Point de départ invalide")
        if is_valid:
            if start_point == "1":
                start_point = 0
            else:
                start_point = self.__entry_point.get()
        if is_valid:
            try:
                nb_jumps = int(self.__entry_jumps.get())
            except:
                is_valid = 0
                showerror("Erreur", "Nombre de sauts invalide")
        if is_valid and nb_jumps < 1:
            is_valid = 0
            showerror("Erreur", "Nombre de sauts invalide")
        if is_valid:
            try:
                nb_simulations = int(self.__entry_simulations.get())
            except:
                is_valid = 0
                showerror("Erreur", "Nombre de simulations invalide")
        if is_valid and nb_simulations < 1:
            is_valid = 0
            showerror("Erreur", "Nombre de simulations invalide")
        if is_valid:
            self.__mainwindow.simulate(start_point, nb_jumps, nb_simulations)
            self.__close()

class Point:
    def __init__(self, name):
        self.__name = name
        self.__coords = [0, 0]
        self.list_adjs = {}

    def set_coords(self, x, y):
        self.__coords = [x, y]

    def get_self_links(self):
        total = [0, 0]
        if self.__name+"-" in self.list_adjs:
            total[0] = self.list_adjs[self.__name+"-"][0]
        if self.__name+">" in self.list_adjs:
            total[1] = self.list_adjs[self.__name+">"][0]
        return total

    def get_x(self):
        return self.__coords[0]

    def get_y(self):
        return self.__coords[1]

    def del_adj(self, adj):
        self.list_adjs[adj] -= 1
        if self.list_adjs[adj] == 0:
            del self.list_adjs[adj]

    def add_adj(self, adj):
        if adj in self.list_adjs:
            self.list_adjs[adj] += 1
        else:
            self.list_adjs[adj] = 1

window = MainWindow()
