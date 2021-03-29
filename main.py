# from tkinter import *
from tkinter import  StringVar
from tkinter import Label
from tkinter import messagebox
from tkinter import simpledialog
import pandas as pd
from tkinter.filedialog import askopenfile
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from tkinter import colorchooser
from tkinter import ttk
from ttkthemes import themed_tk as tk
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_string_dtype

# SINGLE LINED GRAPH
# single lined graph section is purposely seperated in order to prevent hassle of selecting graph title everytime to edit.

# attributes of SLG
x_points = []
y_points = []
line_style = 'solid'
marker_style = '.'
marker_size = 10
graph_color = 'Black'
graph_title = 'Line Graph'
s_graph_canvas_title = ''
xs_label = "X Axis"
y_label = "Y Axis"


# update
def update_graph():
    fig.clear()

    g = fig.add_subplot(title=s_graph_canvas_title, label=graph_title, xlabel=xs_label, ylabel=y_label)
    g.plot(x_points, y_points, linestyle=line_style, markersize=marker_size, markeredgecolor='black',
           marker=marker_style, color=graph_color, label=graph_title)
    g.legend()

    canvas.draw()


# change title
def change_axes_title():
    global xs_label, y_label
    xs_label = simpledialog.askstring("X axis", "Enter X axis title")
    y_label = simpledialog.askstring("Y axis", "Enter Y axis title")
    update_graph()


# add single point
def add_point():
    try:
        global x_points
        global y_points
        a, b = float(x.get()), float(y.get())
        x.delete(0, 'end')
        y.delete(0, 'end')
        x_points.append(a)
        y_points.append(b)
        xy = list(zip(x_points, y_points))
        xy.sort(key=lambda x: x[0])
        x_points = [x[0] for x in xy]
        y_points = [x[1] for x in xy]
        update_graph()
    except:
        messagebox.showwarning("ERROR", "Enter a Number")


# set title of graph
def set_title():
    global graph_title
    graph_title = simpledialog.askstring("Title", "Enter Title")
    update_graph()


# set attributes
def default_line():
    global line_style
    line_style = 'solid'
    update_graph()


def dashed_line():
    global line_style
    line_style = 'dashed'
    update_graph()


def dotted_line():
    global line_style
    line_style = 'dotted'
    update_graph()


def default_marker():
    global marker_style
    marker_style = '.'
    update_graph()


def plus_marker():
    global marker_style
    marker_style = '+'
    update_graph()


def x_marker():
    global marker_style
    marker_style = 'x'
    update_graph()


# clear canvas
def clear_graph():
    global x_points, y_points, line_style, marker_style, marker_size, graph_color, graph_title, xs_label, y_label, s_graph_canvas_title
    ans = messagebox.askyesno("Are You Sure ?", "Do You Want To Clear The Canvas ?")
    if (ans != True):
        return
    fig.clear()
    line_style = 'solid'
    marker_style = '.'
    marker_size = 10
    graph_color = 'Black'
    graph_title = 'Line Graph'
    xs_label = "X Axis"
    y_label = "Y Axis"
    s_graph_canvas_title = ""

    curr_graph_color.config(bg=graph_color)

    x_points, y_points = [], []
    canvas.draw()


# pick graph color
def pick_color():
    global graph_color
    try:
        graph_color = colorchooser.askcolor()[1]
        curr_graph_color.config(bg=graph_color)
    except:
        update_graph()

    update_graph()


def csv_single():
    try:
        file = askopenfile(mode='r', filetypes=[('CSV FILES', '*.csv')])
        if file is not None:
            rd = pd.read_csv(file)
            wm = tk.ThemedTk()
            wm.set_theme('radiance')
            wm.title('Import Graph From CSV')
            lst = list(rd.columns)
            ttk.Label(master=wm, text="Select attribute for X Axis ").pack(padx=10, pady=15)
            x = StringVar()
            y = StringVar()
            op1 = ttk.OptionMenu(wm, x, "DEFAULT VALUE", *lst)
            op1.config(width=20)
            op1.pack(padx=15, pady=15)
            ttk.Label(master=wm, text="Select attribute for Y Axis ").pack(padx=10, pady=15)
            op2 = ttk.OptionMenu(wm, y, "DEFAULT VALUE", *lst)
            op2.config(width=20)
            op2.pack(padx=15, pady=15)

            def plot_csv():
                try:
                    if not (is_numeric_dtype(rd[x.get()]) and is_numeric_dtype(rd[y.get()])):
                        raise Exception
                    x_points.extend(rd[x.get()])
                    y_points.extend(rd[y.get()])
                    update_graph()
                    wm.destroy()
                except:
                    messagebox.showerror("Error", "Enter Data Correctly.")
                    wm.destroy()
                    update_graph()
                    pass

            ttk.Button(master=wm, text="PLOT GRAPH", command=plot_csv).pack(padx=15, pady=15)
    except:
        wm.destroy()
        update_graph()
        messagebox.showerror("ERROR", "Enter Data Correctly.")


# add multiple points
def add_multi_points():
    try:
        s = simpledialog.askstring("Add Multiple Points",
                                   "Multiple points should be separated by a comma\nX and Y coordinates are separated using space\n\nFor example 2 3,8 9 will plot points as (2,3) & (8,9)")
        global x_points, y_points
        l = s.split(",")
        for i in l:
            j = i.split()
            a, b = float(j[0]), float(j[1])
            x_points.append(a)
            y_points.append(b)
            xy = list(zip(x_points, y_points))
            xy.sort(key=lambda x: x[0])
            x_points = [x[0] for x in xy]
            y_points = [x[1] for x in xy]
            update_graph()
    except:
        pass


def set_title_canvas():
    global s_graph_canvas_title
    x = simpledialog.askstring("Title", "Enter Graph Canvas Title")
    s_graph_canvas_title = x
    update_graph()


def delete_spoint():
    try:

        x = simpledialog.askfloat("X Axis", "Enter X co-ordinate of point to be deleted")
        y = simpledialog.askfloat("Y Axis", "Enter Y co-ordinate of point to be deleted")
        print(x)
        print(y)

        if x_points.index(x) == y_points.index(y):

            x_points.pop(x_points.index(x))
            y_points.pop(y_points.index(y))



        else:
            raise Exception
        update_graph()
    except:
        messagebox.showerror("ERROR", "No such point exists")


root = tk.ThemedTk()

root.title("Plotix 1.0")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.tk.call('tk', 'scaling', 1.5)

root.geometry("%dx%d" % (width, height))
try:
    root.iconbitmap('Plotix_logo.ico')
except:
    pass
root.set_theme('radiance')

my_notebook = ttk.Notebook(master=root)
my_notebook.pack(expand=1, fill="both")

# canvass and buttons
line_frame = ttk.LabelFrame(master=root, text="Single Line Graph")

ttk.Label(text="Edit Graph", width='50', master=line_frame).grid(row=0, column=0, columnspan=3)

fig = Figure(figsize=(6, 4), dpi=170)

canvas = FigureCanvasTkAgg(fig, master=line_frame)  # DrawingArea.
canvas.draw()
canvas.get_tk_widget().grid(column=7, columnspan=3, rowspan=100)

# toolbar
toolbar = NavigationToolbar2Tk(canvas, line_frame, pack_toolbar=False)
toolbar.update()
toolbar.grid(column=7, columnspan=3)

ttk.Label(text="Add Point", master=line_frame, borderwidth=2, relief="solid").grid(row=1, column=0, columnspan=6)

x = ttk.Entry(master=line_frame)
x.insert(0, '')
y = ttk.Entry(master=line_frame)
y.insert(0, '')
add_point_button = ttk.Button(master=line_frame, text='Add Point', width=40, command=add_point)
x.grid(row=2, column=0, padx=(15, 0))
y.grid(row=2, column=2, padx=(0, 20))
add_point_button.grid(row=3, columnspan=6)

ttk.Label(text="Line Style", master=line_frame).grid(row=5, column=0, columnspan=6, pady=(10, 5))
ttk.Button(master=line_frame, text='Default', command=default_line).grid(row=6, column=0, padx=5)
ttk.Button(master=line_frame, text='Dashed', command=dashed_line).grid(row=6, column=1, padx=5)
ttk.Button(master=line_frame, text='Dotted', command=dotted_line).grid(row=6, column=2, padx=5)

ttk.Label(text="Marker Style ", master=line_frame).grid(row=7, column=0, columnspan=6, pady=(10, 5))
ttk.Button(master=line_frame, text='Default Sign', command=default_marker).grid(row=8, column=0, padx=5)
ttk.Button(master=line_frame, text='Plus Sign', command=plus_marker).grid(row=8, column=1, padx=5)
ttk.Button(master=line_frame, text='X Sign', command=x_marker).grid(row=8, column=2, padx=5)

ttk.Label(text="Line Graph Color ", master=line_frame).grid(row=9, column=0, columnspan=6, pady=(10, 5))
curr_graph_color = Label(text="    ", width='10', master=line_frame, background=graph_color)
curr_graph_color.grid(row=10, column=0, pady=5)
ttk.Button(master=line_frame, text="Choose a color", command=pick_color).grid(row=10, column=1, columnspan=2, pady=5)

ttk.Button(master=line_frame, text='Set Graph Line Label', width=40, command=set_title).grid(row=14, columnspan=6,
                                                                                             padx=5, pady=(20, 5))

ttk.Button(master=line_frame, text='Set Axes Titles', width=40, command=change_axes_title).grid(row=15, columnspan=6,
                                                                                                padx=5, pady=5)
ttk.Button(master=line_frame, text='Set Graph Canvas Title', width=40, command=set_title_canvas).grid(row=16,
                                                                                                      columnspan=6,
                                                                                                      padx=5, pady=5)

ttk.Button(master=line_frame, text='Add Multiple Points', width=40, command=add_multi_points).grid(row=12, columnspan=6,
                                                                                                   padx=5, pady=5)
ttk.Button(master=line_frame, text='Add Points From CSV File', width=40, command=csv_single).grid(row=13, columnspan=6,
                                                                                                  padx=5, pady=(5, 10))
ttk.Button(master=line_frame, text='Delete A Point', width=40, command=delete_spoint).grid(row=99, columnspan=6, padx=5,
                                                                                           pady=5)

ttk.Button(master=line_frame, text='Clear Graph Canvas', width=40, command=clear_graph).grid(row=100, columnspan=6,
                                                                                             padx=5, pady=5)
line_frame.pack(expand=1, fill='both', padx=15, pady=5)
my_notebook.add(line_frame, text='Single Line Graph')

# Multi Line Graph

# multi line graph array format =[title,[x],[y],[linecolor],[marker_style],[line_style]]

mline = []
mline_canvas_title = " "
mline_frame = ttk.LabelFrame(master=my_notebook, text="Multi Line Graph")
ttk.Label(text="Edit MultiLine Graph", width='50', master=mline_frame).grid(row=0, column=0, columnspan=3)
mline_fig = Figure(figsize=(6, 4), dpi=170)

mline_canvas = FigureCanvasTkAgg(mline_fig, master=mline_frame)  # A tk.DrawingArea.

mline_canvas.get_tk_widget().grid(padx=10, column=7, rowspan=100)
mline_canvas.draw()

toolbar = NavigationToolbar2Tk(mline_canvas, mline_frame, pack_toolbar=False)
toolbar.update()
toolbar.grid(column=7)
x_axis, y_axis = 'X-Axis', 'Y-Axis'


# graph=[title,[x],[y],[linecolor],[marker_style],[line_style]]
def update_mline():
    mline_fig.clear()
    g = mline_fig.add_subplot(title=mline_canvas_title, xlabel=x_axis, ylabel=y_axis)
    for i in mline:
        xy = list(zip(i[1], i[2]))
        xy.sort(key=lambda x: x[0])
        x = [x[0] for x in xy]
        y = [x[1] for x in xy]
        # xlabel=x_label, ylabel=y_label
        g.plot(x, y, linestyle=i[5], markeredgecolor='black', marker=i[4], color=i[3], label=i[0])
    g.legend()
    mline_canvas.draw()


# set canvas title
def set_mtitle_canvas():
    global mline_canvas_title
    x = simpledialog.askstring("Title", "Enter Graph Canvas Title")
    mline_canvas_title = x
    update_mline()


# create new graph line
def add_mline_graph():
    # graph=[title,[x],[y],[linecolor],[marker_style],[line_style]]
    try:
        new_graph = tk.ThemedTk()
        new_graph.set_theme('radiance')
        new_graph.title('Create New Graph')
        ttk.Label(master=new_graph, text="Enter Graph Line Title ").pack(padx=20)
        mline_title = ttk.Entry(master=new_graph)
        mline_title.config(width=25)
        mline_title.pack(padx=20, pady=(5, 20))
        mline_x, mline_y = [], []
        ttk.Label(master=new_graph,
                  text="Enter co-ordinates in x1 y1,x2 y2...format\nFor example. 1 3,8 7 will plot points at(1,3) and (8,7)").pack(
            padx=20)
        mline_xy = ttk.Entry(master=new_graph)
        mline_xy.config(width=25)
        mline_xy.pack(padx=20, pady=(5, 20))
        mline_color = StringVar()
        mline_color.set('blue')
        ttk.Label(master=new_graph, text="Pick Graph Line Color").pack(padx=20)
        opc = ttk.OptionMenu(new_graph, mline_color, "black",
                             *['Red', 'Orange', 'Yellow', 'Black', 'Gray', 'Blue', 'Green'])
        opc.config(width=25)
        opc.pack(padx=20, pady=(5, 20))
        mline_marker = StringVar()
        mline_marker.set(".")
        ttk.Label(master=new_graph, text="Pick a Marker Style").pack(padx=20)
        opm = ttk.OptionMenu(new_graph, mline_marker, ".", *['o', '.', '+', '*'])
        opm.config(width=25)
        opm.pack(padx=20, pady=(5, 20))
        ttk.Label(master=new_graph, text="Pick a Line Style").pack(padx=20)
        mline_linestyle = StringVar()
        mline_linestyle.set("solid")
        opl = ttk.OptionMenu(new_graph, mline_linestyle, "solid", *['solid', 'dotted', 'dashed'])
        opl.config(width=25)
        opl.pack(padx=20, pady=(5, 20))

        def add_line_graph():
            for x in mline:

                if x[0] == mline_title.get():
                    messagebox.showerror("ERROR", 'Please Pick A Unique Title')
                    new_graph.destroy()
                    add_mline_graph()
                    return
            try:
                xy = mline_xy.get().split(',')
                for i in xy:
                    j = i.split()
                    xp = float(j[0])
                    yp = float(j[1])
                    mline_x.append(xp)
                    mline_y.append(yp)
                mline.append(
                    [mline_title.get(), mline_x, mline_y, mline_color.get(), mline_marker.get(), mline_linestyle.get()])
                update_mline()
                new_graph.destroy()
            except:
                new_graph.destroy()
                messagebox.showerror("ERROR", "Please input correct data")

                update_mline()

        ttk.Button(master=new_graph, text="Add Line Graph", width=25, command=add_line_graph).pack(padx=10, pady=15)
    except:
        update_mline()


# add point to existing line
def add_point_ex():
    try:
        ex = tk.ThemedTk()
        ex.set_theme('radiance')
        ex.title('Add New Points To Existing Graph Line')
        ttk.Label(master=ex, text="Select Graph Line Title").pack(padx=20)
        existing_g = StringVar()
        titles = [x[0] for x in mline]

        o = ttk.OptionMenu(ex, existing_g, "DEFAULT", *titles)
        o.config(width=20)
        o.pack(padx=10, pady=(5, 15))

        ttk.Label(master=ex,
                  text="Multiple points should be separated by a comma\nX and Y coordinates are separated using space\n\nFor example 2 3,8 9 will plot points as (2,3) & (8,9)").pack(
            padx=20)
        xy = ttk.Entry(master=ex, width=20)
        xy.pack(padx=20, pady=(10, 20))

        def add_p():
            try:
                index = titles.index(existing_g.get())
                xy_p = xy.get().split(",")
                xc, yc = [], []
                for i in xy_p:
                    z = i.split()
                    a = float(z[0])
                    b = float(z[1])
                    mline[index][1].append(a)
                    mline[index][2].append(b)

                update_mline()
                ex.destroy()
            except:
                messagebox.showerror("ERROR", "Please Enter Data Correctly.")
                ex.destroy()
                pass

        ttk.Button(master=ex, text="Add Point", command=add_p, width=20).pack(padx=20, pady=(20, 20))
    except:
        messagebox.showerror("ERROR", "Please Enter Data Correctly")
        ex.destroy()


# change attributes
def change_mline_att():
    wm = tk.ThemedTk()
    wm.set_theme('radiance')
    wm.title('Set Attributes')
    ttk.Label(master=wm, text="Select Graph Line Title").pack(padx=20)
    existing_g = StringVar()
    titles = [x[0] for x in mline]

    o = ttk.OptionMenu(wm, existing_g, "DEFAULT", *titles)
    o.config(width=20)
    o.pack(padx=10, pady=(5, 15))

    def change_att():
        # graph=[title,[x],[y],[linecolor],[marker_style],[line_style]]
        try:
            wm.destroy()
            ex = tk.ThemedTk()
            ex.set_theme('radiance')
            ex.title('Set Attributes')
            index = titles.index(existing_g.get())
            mline_color = StringVar()
            mline_color.set('blue')
            ttk.Label(master=ex, text="Pick Graph Line Color").pack(padx=20)
            opc = ttk.OptionMenu(ex, mline_color, mline[index][3],
                                 *['Red', 'Orange', 'Yellow', 'Black', 'Gray', 'Blue', 'Green'])
            opc.config(width=25)
            opc.pack(padx=20, pady=(5, 20))
            mline_marker = StringVar()
            mline_marker.set(".")
            ttk.Label(master=ex, text="Pick a Marker Style").pack(padx=20)
            opm = ttk.OptionMenu(ex, mline_marker, mline[index][4], *['o', '.', '+', '*'])
            opm.config(width=25)
            opm.pack(padx=20, pady=(5, 20))
            ttk.Label(master=ex, text="Pick a Line Style").pack(padx=20)
            mline_linestyle = StringVar()
            mline_linestyle.set("solid")
            opl = ttk.OptionMenu(ex, mline_linestyle, mline[index][5], *['solid', 'dotted', 'dashed'])
            opl.config(width=25)
            opl.pack(padx=20, pady=(5, 20))

            def done():

                mline[index][3] = mline_color.get()
                mline[index][4] = mline_marker.get()
                mline[index][5] = mline_linestyle.get()

                update_mline()
                ex.destroy()

            ttk.Button(master=ex, text="Save Changes", command=done, width=20).pack(padx=10, pady=20)
        except:
            messagebox.showerror("ERROR", "Select Title")
            ex.destroy()

    ttk.Button(master=wm, text="Select Graph Title", command=change_att, width=20).pack(padx=10, pady=20)


# axes kabek
def axes_label():
    x = simpledialog.askstring("X Axis", "Enter Label for X Axis")
    y = simpledialog.askstring("Y Axis", "Enter Label for Y Axis")
    global x_axis, y_axis
    x_axis = x
    y_axis = y
    update_mline()


# delete graph
def del_graph():
    t = tk.ThemedTk()
    t.set_theme('radiance')
    t.title('Delete Graph Line')
    title = StringVar()
    titles = [x[0] for x in mline]
    ttk.Label(master=t, text="Select A Graph From DropDown Below").pack(padx=25, pady=10)
    op = ttk.OptionMenu(t, title, "DEFAULT", *titles)
    op.config(width=20)
    op.pack(padx=10, pady=20)

    def delete():
        try:

            ans = messagebox.askyesno("Are You Sure ?", "Do You Want to Delete The Graph Line ?")
            if ans != True:
                return
            index = titles.index(title.get())
            mline.pop(index)
            update_mline()
            t.destroy()
        except:
            messagebox.showerror("ERROR", "Select a title")
            t.destroy()

    ttk.Button(master=t, text="Delete Graph", command=delete).pack(padx=10, pady=20)


# del point
def del_point():
    try:
        t = tk.ThemedTk()
        t.set_theme('radiance')
        t.title('Delete Point')
        title = StringVar()
        titles = [x[0] for x in mline]
        ttk.Label(master=t, text="Select A Graph From DropDown Below").pack(padx=25, pady=10)
        op = ttk.OptionMenu(t, title, "DEFAULT", *titles)
        op.config(width=20)
        op.pack(padx=10, pady=20)

        def delete():
            try:
                t.destroy()
                index = titles.index(title.get())
                x = simpledialog.askfloat("X Axis", "Enter X co-ordinate of point to be deleted")
                y = simpledialog.askfloat("Y Axis", "Enter Y co-ordinate of point to be deleted")
                print(x)
                print(y)

                if mline[index][1].index(x) == mline[index][2].index(y):

                    mline[index][1].pop(mline[index][1].index(x))
                    mline[index][2].pop(mline[index][2].index(y))
                    if len(mline[index][1]) == 0:
                        mline.pop(index)

                    update_mline()
                else:
                    raise Exception
            except:
                messagebox.showerror("ERROR", "No such point exists")

        ttk.Button(master=t, text="Select Graph", command=delete).pack(padx=10, pady=20)
    except:
        messagebox.showerror("ERROR", "Select a title")


# clear graph
def clear_graph():
    global mline_canvas_title
    ans = messagebox.askyesno("Are You Sure ?", "Do You Want to Clear The Canvas ?")
    if ans != True:
        return
    global mline
    mline = []
    mline_canvas_title = ''
    update_mline()


# csv import
def add_csv():
    try:
        file = askopenfile(mode='r', filetypes=[('CSV FILES', '*.csv')])
        if file is not None:
            rd = pd.read_csv(file)
            wm = tk.ThemedTk()
            wm.set_theme('radiance')
            wm.title('Import Graph From CSV')
            lst = list(rd.columns)
            ttk.Label(master=wm, text="Select attribute for X Axis ").pack(padx=10, pady=15)
            x = StringVar()
            y = StringVar()
            op1 = ttk.OptionMenu(wm, x, "DEFAULT VALUE", *lst)
            op1.config(width=20)
            op1.pack(padx=15, pady=15)
            ttk.Label(master=wm, text="Select attribute for Y Axis ").pack(padx=10, pady=15)
            op2 = ttk.OptionMenu(wm, y, "DEFAULT VALUE", *lst)
            op2.config(width=20)
            op2.pack(padx=15, pady=15)

            ttk.Label(master=wm, text="Enter Graph Line Title ").pack(padx=20)
            mline_title = ttk.Entry(master=wm)
            mline_title.config(width=25)
            mline_title.pack(padx=20, pady=(5, 20))

            mline_color = StringVar()
            mline_color.set('blue')
            ttk.Label(master=wm, text="Pick Graph Line Color").pack(padx=20)
            opc = ttk.OptionMenu(wm, mline_color, "black",
                                 *['Red', 'Orange', 'Yellow', 'Black', 'Gray', 'Blue', 'Green'])
            opc.config(width=25)
            opc.pack(padx=20, pady=(5, 20))
            mline_marker = StringVar()
            mline_marker.set(".")
            ttk.Label(master=wm, text="Pick a marker style").pack(padx=20)
            opm = ttk.OptionMenu(wm, mline_marker, ".", *['o', '.', '+', '*'])
            opm.config(width=25)
            opm.pack(padx=20, pady=(5, 20))
            ttk.Label(master=wm, text="Pick a line style").pack(padx=20)
            mline_linestyle = StringVar()
            mline_linestyle.set("solid")
            opl = ttk.OptionMenu(wm, mline_linestyle, "solid", *['solid', 'dotted', 'dashed'])
            opl.config(width=25)
            opl.pack(padx=20, pady=(5, 20))

            def plot_csv():
                try:
                    if not (is_numeric_dtype(rd[x.get()]) and is_numeric_dtype(rd[y.get()])):
                        raise Exception
                    for i in mline:
                        if mline_title.get() == i[0]:
                            wm.destroy()
                            messagebox.showerror("ERROR", "Enter Unique Title.")
                            return

                    mline.append([mline_title.get(), rd[x.get()], rd[y.get()], mline_color.get(), mline_marker.get(),
                                  mline_linestyle.get()])
                    update_mline()
                    wm.destroy()
                except:
                    messagebox.showerror("Error", "Enter Details Correctly")
                    wm.destroy()

            ttk.Button(master=wm, text="PLOT GRAPH", command=plot_csv).pack(padx=15, pady=15)
    except:
        wm.destroy()
        messagebox.showerror("ERROR", "Enter Data Correctly.")


ttk.Button(master=mline_frame, text='Add New Graph Line', width=40, command=add_mline_graph).grid(row=2, columnspan=6,
                                                                                                  padx=5, pady=5)

ttk.Button(master=mline_frame, text='Add New Points to Existing Line', width=40, command=add_point_ex).grid(row=4,
                                                                                                            columnspan=6,
                                                                                                            padx=5,
                                                                                                            pady=5)

ttk.Button(master=mline_frame, text='Add Graph Line Using CSV File', width=40, command=add_csv).grid(row=5,
                                                                                                     columnspan=6,
                                                                                                     padx=5,
                                                                                                     pady=(5, 20))

ttk.Button(master=mline_frame, text='Change Graph Line Attributes', width=40, command=change_mline_att).grid(row=6,
                                                                                                             columnspan=6,
                                                                                                             padx=5,
                                                                                                             pady=(
                                                                                                             15, 5))

ttk.Button(master=mline_frame, text='Set Axes Labels', width=40, command=axes_label).grid(row=8, columnspan=6, padx=5,
                                                                                          pady=5)
ttk.Button(master=mline_frame, text='Set Graph Canvas Title', width=40, command=set_mtitle_canvas).grid(row=9,
                                                                                                        columnspan=6,
                                                                                                        padx=5, pady=5)

ttk.Button(master=mline_frame, text='Delete A Graph Line', width=40, command=del_graph).grid(row=99, columnspan=6,
                                                                                             padx=5, pady=5)

ttk.Button(master=mline_frame, text='Delete A Point ', width=40, command=del_point).grid(row=97, columnspan=6, padx=5,
                                                                                         pady=5)

ttk.Button(master=mline_frame, text='Clear Graph Canvas', width=40, command=clear_graph).grid(row=100, columnspan=6,
                                                                                              padx=5, pady=5)

my_notebook.add(mline_frame, text="Multi Line Graph")

# Bar Graph
xb_axis, yb_axis = 'X-Axis', 'Y-Axis'
x_label = []
y_value = []
hatch = []
colors = []
bar_title = " "


# update bar
def update_bargraph():
    bar_fig.clear()
    bars = bar_fig.add_subplot(title=bar_title, xlabel=xb_axis, ylabel=yb_axis).bar(x_label, y_value)
    for i in range(len(x_label)):
        bars[i].set_facecolor(colors[i])
        bars[i].set_hatch(hatch[i])
    bar_canvas.draw()


# add bar
def add_bar():
    global x_label, y_label
    try:
        a = simpledialog.askstring("Title", 'Enter Bar Title')
        if a not in x_label:
            x_label.append(a)
        else:
            messagebox.showerror("Enter A Unique Title", "Title should always be unique")
            add_bar()
            pass
        b = simpledialog.askfloat("Value", "Enter Value for the Bar")
        b = float(b)
        y_value.append(b)
        hatch.append(' ')
        colors.append('Blue')
    except:
        messagebox.showerror("ERROR", "Please input correct data")
    update_bargraph()


# add hatch
def add_hatching():
    try:
        hatch_window = tk.ThemedTk()
        hatch_window.set_theme('radiance')
        hatch_window.title('Add Hatching')
        hatch_title = StringVar()
        hatch_title.set("DEFAULT")
        ttk.Label(master=hatch_window, text="Pick a bar from Dropdown Below").pack()
        op = ttk.OptionMenu(hatch_window, hatch_title, "DEFAULT VALUE", *x_label)
        op.config(width=25)
        op.pack()
        hatch_op = ['/', r'\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']
        selected_hatch = StringVar()

        ttk.Label(master=hatch_window, text="Pick a Hatching Style from Dropdown Below").pack(pady=(15, 5))

        h_op = ttk.OptionMenu(hatch_window, selected_hatch, *hatch_op)
        h_op.config(width=25)
        h_op.pack(padx=20, pady=(0, 20))

        def add_hatch_button():
            try:
                global x_label, hatch
                bar_fig.clear()
                hatch[x_label.index(hatch_title.get())] = selected_hatch.get()

                update_bargraph()

                hatch_window.destroy()
            except:
                pass

        ttk.Button(master=hatch_window, text="Add Hatch", command=add_hatch_button).pack(padx=10, pady=10)
        op.pack(padx=10, pady=10)
    except:
        pass


# set color
def set_color():
    try:
        clr = tk.ThemedTk()
        clr.set_theme('radiance')
        clr.title('Set Color')
        color_title = StringVar()
        ttk.Label(master=clr, text="Pick A Bar From Dropdown Below").pack(padx=20, pady=(15, 10))
        op = ttk.OptionMenu(clr, color_title, "DEFAULT VALUE", *x_label)
        op.config(width=25)
        op.pack(padx=20, pady=(10, 20))
        ttk.Label(master=clr, text="Pick A Color From Dropdown Below").pack()
        color = StringVar()
        color.set("Blue")
        opc = ttk.OptionMenu(clr, color, "DEFAULT VALUE",
                             *['Red', 'Orange', 'Yellow', 'Black', 'Gray', 'Blue', 'Green'])
        opc.config(width=25)
        opc.pack(pady=(10, 20))

        def set_bar_color():
            try:
                colors[x_label.index(color_title.get())] = color.get()
                update_bargraph()
                clr.destroy()
            except:
                pass

        ttk.Button(master=clr, text="Set Color", command=set_bar_color).pack(padx=10, pady=10)
    except:
        pass


def delete_bar():
    try:
        clr = tk.ThemedTk()
        clr.set_theme('radiance')
        clr.title('Delete Bar Stick')
        del_title = StringVar()
        ttk.Label(master=clr, text="Pick A Bar To Delete ").pack()
        op = ttk.OptionMenu(clr, del_title, "DEFAULT VALUE", *x_label)
        op.config(width=25)
        op.pack(padx=15, pady=(5, 15))

        def del_bar():
            try:
                ans = messagebox.askyesno("Are You Sure ?", "Do you want to delete the bar stick ?")
                if (ans == True):
                    y_value.pop(x_label.index(del_title.get()))
                    colors.pop(x_label.index(del_title.get()))
                    hatch.pop(x_label.index(del_title.get()))
                    x_label.pop(x_label.index(del_title.get()))
                    clr.destroy()
                else:

                    pass
                update_bargraph()
            except:
                clr.destroy()
                pass

        ttk.Button(master=clr, text="DELETE BAR STICK", command=del_bar).pack(padx=10, pady=10)
    except:
        clr.destroy()
        pass


def change_bar_title():
    try:
        clr = tk.ThemedTk()
        clr.set_theme('radiance')
        clr.title('Change Bar Title')
        del_title = StringVar()
        ttk.Label(master=clr, text="Pick A Bar To Change Title of ").pack()
        op = ttk.OptionMenu(clr, del_title, "DEFAULT VALUE", *x_label)
        op.config(width=25)
        op.pack(padx=15, pady=(5, 15))
        ttk.Label(master=clr, text=" Type New Title below ").pack()
        e = ttk.Entry(master=clr)
        e.config(width=20)
        e.pack()

        def tit_bar():
            try:
                x_label[x_label.index(del_title.get())] = e.get()
                update_bargraph()
                clr.destroy()
            except:
                clr.destroy()
                pass

        ttk.Button(master=clr, text="Change Title", command=tit_bar).pack(padx=10, pady=10)
    except:
        clr.destroy()


def add_bar_csv():
    try:
        file = askopenfile(mode='r', filetypes=[('CSV FILES', '*.csv')])
        if file is not None:
            rd = pd.read_csv(file, nrows=50)
            wm = tk.ThemedTk()
            wm.title("Add Bar From CSV")
            wm.set_theme('radiance')
            lst = list(rd.columns)
            ttk.Label(master=wm, text="Select attribute for Labels  ").pack(padx=10, pady=15)
            x = StringVar()
            y = StringVar()
            op1 = ttk.OptionMenu(wm, x, "DEFAULT VALUE", *lst)
            op1.config(width=20)
            op1.pack(padx=15, pady=15)
            ttk.Label(master=wm, text="Select attribute for Values ").pack(padx=10, pady=15)
            op2 = ttk.OptionMenu(wm, y, "DEFAULT VALUE", *lst)
            op2.config(width=20)
            op2.pack(padx=15, pady=15)

            def plot_csv():
                try:
                    if not (is_numeric_dtype(rd[y.get()])):
                        raise Exception
                    c = len(rd.index)
                    x_label.extend(rd[x.get()])
                    y_value.extend(rd[y.get()])
                    colors.extend(['blue'] * c)
                    hatch.extend([' '] * c)
                    update_bargraph()
                    wm.destroy()
                except:
                    messagebox.showerror("ERROR", "Enter Data correctly")
                    wm.destroy()

            ttk.Button(master=wm, text="PLOT GRAPH", command=plot_csv).pack(padx=20, pady=15)
    except:
        messagebox.showerror("ERROR", "Enter Data correctly")
        wm.destroy()
        return


def edit_bar_val():
    try:
        wm = tk.ThemedTk()
        wm.set_theme('radiance')
        wm.title('Edit Bar Stick')
        ttk.Label(master=wm, text="Select A Bar Stick From Dropdown Below ").pack(padx=15, pady=(15, 5))
        edit_label = StringVar()

        ope = ttk.OptionMenu(wm, edit_label, 'default', *x_label)
        ope.config(width=25)
        ope.pack(padx=15, pady=(5, 15))
        ttk.Label(master=wm, text="Enter Value For The Stick ").pack(padx=15, pady=(15, 5))
        e = ttk.Entry(master=wm)
        e.config(width=25)
        e.pack(padx=15, pady=(15, 5))

        def edit_p():
            try:

                index1 = x_label.index(edit_label.get())
                y_value[index1] = float(e.get())

                wm.destroy()

                if y_value[index1] == 0:
                    x_label.pop(index1)
                    y_value.pop(index1)
                    colors.pop(index1)
                    hatch.pop(index1)
                update_bargraph()

            except:

                messagebox.showerror("Error", "Please Enter Details Correctly")

        ttk.Button(master=wm, text='Set Bar Stick Value', command=edit_p, width=25).pack(padx=15, pady=15)
    except:
        pass


def clear_bargraph():
    ans = messagebox.askyesno("Are You Sure ?", "Do You Want to Clear The Canvas ?")
    if ans != True:
        return
    global x, x_label, y_value, hatch, colors, bar_title
    x_label = []
    y_value = []
    hatch = []
    colors = []
    bar_title = ''
    update_bargraph()


def set_baraxis_label():
    global xb_axis, yb_axis
    x = simpledialog.askstring("X Axis ", "Enter Label For X Axis")
    y = simpledialog.askstring("Y Axis", "Enter Label For Y Axis")
    xb_axis = x
    yb_axis = y
    update_bargraph()


def set_bar_title():
    global bar_title
    x = simpledialog.askstring("Title", "Enter Bar Graph Title ")
    bar_title = x
    update_bargraph()


bar_frame = ttk.LabelFrame(master=my_notebook, text="Bar Graph")
ttk.Label(text="Edit Bar Graph", width='50', master=bar_frame).grid(row=0, column=0, columnspan=3)
bar_fig = Figure(figsize=(6, 4), dpi=170)

bar_canvas = FigureCanvasTkAgg(bar_fig, master=bar_frame)  # A tk.DrawingArea.

bar_canvas.get_tk_widget().grid(column=7, columnspan=3, rowspan=100)
bar_canvas.draw()

toolbar = NavigationToolbar2Tk(bar_canvas, bar_frame, pack_toolbar=False)
toolbar.update()
toolbar.grid(column=7, columnspan=3)

ttk.Button(master=bar_frame, text='Add Bar', width=40, command=add_bar).grid(row=2, columnspan=6, padx=5, pady=5)
ttk.Button(master=bar_frame, text='Add Bar Graph Using CSV File', width=40, command=add_bar_csv).grid(row=3,
                                                                                                      columnspan=6,
                                                                                                      padx=5,
                                                                                                      pady=(5, 15))
ttk.Button(master=bar_frame, text='Edit Value of Existing Bar Stick', width=40, command=edit_bar_val).grid(row=6,
                                                                                                           columnspan=6,
                                                                                                           padx=5,
                                                                                                           pady=5)

ttk.Button(master=bar_frame, text='Set Bar Stick Hatching', width=40, command=add_hatching).grid(row=7, columnspan=6,
                                                                                                 padx=5, pady=5)

ttk.Button(master=bar_frame, text='Set Bar Stick Color', width=40, command=set_color).grid(row=8, columnspan=6, padx=5,
                                                                                           pady=5)

ttk.Button(master=bar_frame, text='Change Bar Stick Label', width=40, command=change_bar_title).grid(row=5,
                                                                                                     columnspan=6,
                                                                                                     padx=5,
                                                                                                     pady=(10, 5))
ttk.Button(master=bar_frame, text='Set Axes Labels', width=40, command=set_baraxis_label).grid(row=9, columnspan=6,
                                                                                               padx=5, pady=5)
ttk.Button(master=bar_frame, text='Set Bar Graph Title', width=40, command=set_bar_title).grid(row=10, columnspan=6,
                                                                                               padx=5, pady=5)

ttk.Button(master=bar_frame, text='Delete A Bar Stick', width=40, command=delete_bar).grid(row=98, columnspan=6, padx=5,
                                                                                           pady=5)

ttk.Button(master=bar_frame, text='Clear Graph Canvas', width=40, command=clear_bargraph).grid(row=99, columnspan=6,
                                                                                               padx=5, pady=5)

my_notebook.add(bar_frame, text='Bar Graph')

# pie chart
pie_labels = []
pie_values = []
explode_values = []
pie_canvas_title = ""

pie_frame = ttk.LabelFrame(master=my_notebook, text="Pie Chart")
ttk.Label(text="Edit Pie Chart", width='50', master=pie_frame).grid(row=0, column=0, columnspan=3)
pie_fig = Figure(figsize=(6, 4), dpi=170)

pie_canvas = FigureCanvasTkAgg(pie_fig, master=pie_frame)  # A tk.DrawingArea.

pie_canvas.get_tk_widget().grid(column=7, columnspan=3, rowspan=100)
pie_canvas.draw()

toolbar = NavigationToolbar2Tk(pie_canvas, pie_frame, pack_toolbar=False)
toolbar.update()
toolbar.grid(column=7, columnspan=3)

pie_canvas.draw()


# update pie
def update_pie():
    pie_fig.clear()
    pie_subplot = pie_fig.add_subplot(title=pie_canvas_title)
    pie_subplot.axis("equal")
    pie_subplot.pie(pie_values, labels=pie_labels, wedgeprops={'linewidth': 3}, autopct='%0.2f%%',
                    explode=explode_values)
    pie_canvas.draw()


# pie title
def set_pie_title():
    global pie_canvas_title
    x = simpledialog.askstring("Title", "Enter Pie Chart Title ")
    pie_canvas_title = x
    update_pie()


# add pie
def add_pie():
    try:
        l = simpledialog.askstring("Title", "Enter Title")
        if l in pie_labels:
            messagebox.showerror("Error", "Enter Unique Name")
            add_pie()
            return
        v = simpledialog.askfloat("Value", "Enter Pie Value")
        if v <= 0:
            raise Exception
        pie_labels.append(l)
        pie_values.append(v)
        explode_values.append(0)
        update_pie()
    except:
        messagebox.showerror("Error", "Enter Details Correctly.")


# explode
def add_explode():
    try:
        wm = tk.ThemedTk()
        wm.set_theme('radiance')
        wm.title('Explode Pie Chart')
        ttk.Label(master=wm, text="Select a pie from dropdown below ").pack(padx=15, pady=(15, 5))
        explode_label = StringVar()

        ope = ttk.OptionMenu(wm, explode_label, 'default', *pie_labels)
        ope.config(width=25)
        ope.pack(padx=15, pady=(5, 15))
        ttk.Label(master=wm, text="Select explode value from dropdown below ").pack(padx=15, pady=(15, 5))
        exp_val = StringVar()

        opexplode = ttk.OptionMenu(wm, exp_val, 'default', *[0.0, 0.1, 0.2, 0.3, 0.4, 0.5])
        opexplode.config(width=25)
        opexplode.pack(padx=15, pady=(5, 15))

        def add_e():
            try:
                index = pie_labels.index(explode_label.get())
                explode_values[index] = float(exp_val.get())
                update_pie()
                wm.destroy()
            except:
                wm.destroy()
                messagebox.showerror("Error", "Please enter details correctly")

        ttk.Button(master=wm, text='SET EXPLODE', command=add_e, width=25).pack(padx=15, pady=15)
    except:
        pass


# edit pie chart
def edit_pie_val():
    try:
        wm = tk.ThemedTk()
        wm.set_theme('radiance')
        wm.title('Edit Pie')
        ttk.Label(master=wm, text="Select a pie from dropdown below ").pack(padx=15, pady=(15, 5))
        edit_label = StringVar()

        ope = ttk.OptionMenu(wm, edit_label, 'default', *pie_labels)
        ope.config(width=25)
        ope.pack(padx=15, pady=(5, 15))
        ttk.Label(master=wm, text="Enter Value for Pie ").pack(padx=15, pady=(15, 5))
        e = ttk.Entry(master=wm)
        e.config(width=25)
        e.pack(padx=15, pady=(5, 15))

        def edit_p():
            try:
                index = pie_labels.index(edit_label.get())
                pie_values[index] = int(e.get())
                if pie_values[index] == 0:
                    pie_labels.pop(index)
                    pie_values.pop(index)
                    explode_values.pop(index)
                update_pie()
                wm.destroy()
            except:
                wm.destroy()
                messagebox.showerror("Error", "Please enter details correctly")

        ttk.Button(master=wm, text='SET PIE VALUE', command=edit_p, width=25).pack(padx=15, pady=15)
    except:
        pass


# del pie
def del_pie():
    try:
        wm = tk.ThemedTk()
        wm.set_theme('radiance')
        wm.title('Delete Pie')
        ttk.Label(master=wm, text="Select a pie from dropdown below ").pack(padx=15, pady=(15, 5))
        edit_label = StringVar()

        ope = ttk.OptionMenu(wm, edit_label, 'default', *pie_labels)
        ope.config(width=25)
        ope.pack(padx=15, pady=(5, 15))

        def del_p():
            wm.destroy()
            ans = messagebox.askyesno("Are You Sure ?", "Do You Want to Delete The Pie Slice ?")
            if ans != True:
                return
            try:
                index = pie_labels.index(edit_label.get())
                pie_labels.pop(index)
                pie_values.pop(index)
                explode_values.pop(index)
                update_pie()

            except:

                messagebox.showerror("Error", "Please enter details correctly")

        ttk.Button(master=wm, text='DELETE PIE', command=del_p, width=25).pack(padx=15, pady=15)
    except:
        pass


# del pie chart
# clear chart
def del_pie_chart():
    global pie_values, pie_labels, explode_values, pie_canvas_title
    rep = messagebox.askyesno("Are You Sure ?", "Click Yes To Delete Whole Pie Chart")
    if rep == True:
        pie_labels = []
        pie_values = []
        explode_values = []
        pie_canvas_title = ""
        update_pie()
    else:
        pass


# csv import
def add_pie_csv():
    try:
        file = askopenfile(mode='r', filetypes=[('CSV FILES', '*.csv')])
        if file is not None:
            rd = pd.read_csv(file)
            wm = tk.ThemedTk()
            wm.title('Add Pie Chart From CSV')
            wm.set_theme('radiance')
            lst = list(rd.columns)
            ttk.Label(master=wm, text="Select attribute for Labels ").pack(padx=10, pady=(5, 10))
            x = StringVar()
            y = StringVar()
            op1 = ttk.OptionMenu(wm, x, "DEFAULT VALUE", *lst)
            op1.config(width=20)
            op1.pack(padx=20)
            ttk.Label(master=wm, text="Select attribute for Values ").pack(padx=10, pady=(10, 5))
            op2 = ttk.OptionMenu(wm, y, "DEFAULT VALUE", *lst)
            op2.config(width=20)
            op2.pack(padx=15, pady=(0, 15))

            def plot_csv():
                try:
                    if not (is_numeric_dtype(rd[y.get()]) and is_string_dtype(rd[x.get()])):
                        raise Exception
                    for i in rd[x.get()]:
                        if i in pie_labels:
                            pie_values.pop(pie_labels.index(i))
                            explode_values.pop(pie_labels.index(i))
                            pie_labels.pop(pie_labels.index(i))
                    c = len(rd.index)
                    pie_labels.extend(rd[x.get()])
                    pie_values.extend(rd[y.get()])
                    explode_values.extend([0.0] * c)

                    update_pie()
                    wm.destroy()
                except:
                    wm.destroy()
                    messagebox.showerror("Error", "Enter Data Correctly")

            ttk.Button(master=wm, text="PLOT GRAPH", command=plot_csv).pack(padx=15, pady=15)
    except:
        pass


ttk.Button(master=pie_frame, text='Add New Pie Slice', width=40, command=add_pie).grid(row=2, columnspan=6, padx=5,
                                                                                       pady=5)

ttk.Button(master=pie_frame, text='Add Pie Slices From CSV File', width=40, command=add_pie_csv).grid(row=3,
                                                                                                      columnspan=6,
                                                                                                      padx=5, pady=5)

ttk.Button(master=pie_frame, text='Edit Value of A Pie Slice', width=40, command=edit_pie_val).grid(row=5, columnspan=6,
                                                                                                    padx=5,
                                                                                                    pady=(15, 5))

ttk.Button(master=pie_frame, text='Set Explode Value', width=40, command=add_explode).grid(row=6, columnspan=6, padx=5,
                                                                                           pady=5)
ttk.Button(master=pie_frame, text='Set Pie Chart Title', width=40, command=set_pie_title).grid(row=7, columnspan=6,
                                                                                               padx=5, pady=5)

ttk.Button(master=pie_frame, text='Delete A Pie Slice', width=40, command=del_pie).grid(row=99, columnspan=6, padx=5,
                                                                                        pady=5)

ttk.Button(master=pie_frame, text='Clear Pie Chart Canvas', width=40, command=del_pie_chart).grid(row=100, columnspan=6,
                                                                                                  padx=5, pady=5)

my_notebook.add(pie_frame, text="Pie Chart")

root.mainloop()
