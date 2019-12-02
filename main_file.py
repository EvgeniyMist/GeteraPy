from tkinter import*
from tkinter import messagebox as mb 

import labs


def config_lab1_widow():
    pass


def config_lab2_window():
    pass


def config_lab3_window():
    pass


def config_lab4_window():
    pass


def config_lab5_window():
    lab5_w = Toplevel(bg='lightgrey')
    lab5_w.title('Лабораторная работа №5')
    lab5_w.resizable(False, False)
    lab5_w.geometry('530x340+700+150')

    frame1 = LabelFrame(lab5_w, text='Значения плотностей веществ, г/см\N{SUPERSCRIPT THREE}', bg='lightgrey')
    frame1.place(x=10,y=10)    
    Label(frame1, width=71, height=5, bg='lightgrey').pack()
    Label(frame1, text='Топливо', bg='lightgrey').place(x=40, y=10)
    Label(frame1, text='Диоксид урана', bg='lightgrey').place(x=200, y=10)
    gamma_fuel = Entry(frame1, width=15)
    gamma_fuel.insert(0, '10.4')
    gamma_fuel.place(x=360, y=10)
    Label(frame1, text='Теплоноситель', bg='lightgrey').place(x=40, y=40)
    Label(frame1, text='Вода', bg='lightgrey').place(x=200, y=40)
    gamma_cool = Entry(frame1, width=15)
    gamma_cool.insert(0, '0.7')
    gamma_cool.place(x=360, y=40)

    frame2 = LabelFrame(lab5_w, text='Параметры реактора ВВЭР', bg='lightgrey')
    frame2.place(x=10, y=120)
    Label(frame2, width=71, height=10, bg='lightgrey').pack()
    Label(frame2, text='Обогащения (через запятую, от 0 до 1)', bg='lightgrey').place(x=40, y=10)
    x = Entry(frame2, width=30)
    x.place(x=300, y=10)
    Label(frame2, text='Диаметр ТВЭЛа, мм', bg='lightgrey').place(x=40, y=40)
    d = Entry(frame2, width=15)
    d.place(x=300, y=40)
    Label(frame2, text='Толщина ТВЭЛа, мм', bg='lightgrey').place(x=40, y=70) 
    delta = Entry(frame2, width=15)
    delta.place(x=300, y=70)
    Label(frame2, text='Диапазон значений шага решетки (мм) от', bg='lightgrey').place(x=10, y=115)
    R_left = Entry(frame2, width=5)
    R_left.place(x=270, y=115)
    R_left.insert(0, '5')
    Label(frame2, text='до',bg='lightgrey').place(x=310, y=115)
    R_right = Entry(frame2, width=5)
    R_right.insert(0, '15')
    R_right.place(x=340, y=115)
    Label(frame2, text='с шагом', bg='lightgrey').place(x=380, y=115)
    R_delta = Entry(frame2, width=5)
    R_delta.insert(0, '0.5')
    R_delta.place(x=440, y=115)

    func = lambda: start_lab5(d, delta, x, gamma_fuel, gamma_cool,
                              R_left, R_right, R_delta)
    Button(lab5_w, width=15, text='Старт', bg='grey', command=func).place(x=220, y=300)  


def config_lab6_window():
    lab6_w = Toplevel(bg='lightgrey')
    lab6_w.title('Лабораторная работа №6')
    lab6_w.resizable(False, False)
    lab6_w.geometry('530x485+700+150')

    frame1 = LabelFrame(lab6_w, text='Значения плотностей веществ, г/см\N{SUPERSCRIPT THREE}', bg='lightgrey')
    frame1.place(x=10,y=10)    
    Label(frame1, width=71, height=7, bg='lightgrey').pack()  
    Label(frame1, text='Топливо', bg='lightgrey').place(x=40, y=10)
    Label(frame1, text='Диоксид урана', bg='lightgrey').place(x=170, y=10)
    gamma_fuel = Entry(frame1, width=15)
    gamma_fuel.insert(0, '10.4')
    gamma_fuel.place(x=360, y=10)
    Label(frame1, text='Теплоноситель', bg='lightgrey').place(x=40, y=40)
    cool = IntVar()
    cool.set(0)
    Radiobutton(frame1, text='H\N{SUBSCRIPT TWO}O', bg='lightgrey', variable=cool, value=1).place(x=170, y=40)
    Radiobutton(frame1, text='D\N{SUBSCRIPT TWO}O', bg='lightgrey', variable=cool, value=2).place(x=250, y=40)
    gamma_cool = Entry(frame1, width=15)
    gamma_cool.place(x=360, y=40)
    Label(frame1, text='Замедлитель', bg='lightgrey').place(x=40, y=70)   
    mod = IntVar()
    mod.set(0)
    Radiobutton(frame1, text='C', bg='lightgrey', variable=mod, value=1).place(x=170, y=70)
    Radiobutton(frame1, text='D\N{SUBSCRIPT TWO}O', bg='lightgrey', variable=mod, value=2).place(x=250, y=70)
    gamma_mod = Entry(frame1, width=15)
    gamma_mod.place(x=360, y=70)

    frame2 = LabelFrame(lab6_w, text='Параметры канального реактора', bg='lightgrey')
    frame2.place(x=10, y=155)    
    Label(frame2, width=71, height=17, bg='lightgrey').pack()
    Label(frame2, text='Обогащения (через запятую, от 0 до 1)', bg='lightgrey').place(x=10, y=10)
    x = Entry(frame2, width=15)
    x.place(x=360, y=10)
    Label(frame2, text='Диаметр ТВС, мм', bg='lightgrey').place(x=10, y=40)
    D = Entry(frame2, width=15)
    D.insert(0, '100')
    D.place(x=360, y=40)
    Label(frame2, text='Толщина оболочки ТВС, мм', bg='lightgrey').place(x=10, y=70)
    δ_tr = Entry(frame2, width=15)
    δ_tr.insert(0, '2.5')
    δ_tr.place(x=360, y=70)
    Label(frame2, text='Количество ТВЭЛов', bg='lightgrey').place(x=10, y=100)
    N = Entry(frame2, width=15)
    N.insert(0, '18')
    N.place(x=360, y=100)
    Label(frame2, text='Диаметр ТВЭЛа, мм', bg='lightgrey').place(x=10, y=130)
    d = Entry(frame2, width=15)
    d.place(x=360, y=130)
    Label(frame2, text='Толщина оболочки ТВЭЛа, мм', bg='lightgrey').place(x=10, y=160)
    δ_t = Entry(frame2, width=15)
    δ_t.place(x=360, y=160)
    Label(frame2, text='Диапазон значений шага решетки (мм) от', bg='lightgrey').place(x=10, y=190)
    a_left = Entry(frame2, width=5)
    a_left.place(x=270, y=190)
    a_left.insert(0, '120')
    Label(frame2, text='до',bg='lightgrey').place(x=310, y=190)
    a_right = Entry(frame2, width=5)
    a_right.insert(0, '400')
    a_right.place(x=335, y=190)
    Label(frame2, text='с шагом', bg='lightgrey').place(x=380, y=190)
    a_delta = Entry(frame2, width=5)
    a_delta.insert(0, '20')
    a_delta.place(x=450, y=190)
    Label(frame2, text='Кол-во колец, на которые разбивается замедлитель', bg='lightgrey').place(x=10, y=220)
    n = Entry(frame2, width=15)
    n.insert(0, '5')
    n.place(x=360, y=220) 

    func = lambda: start_lab6(d, δ_t, D, δ_tr, N, x, gamma_fuel, cool, mod,
                              gamma_cool, gamma_mod, n, a_left, a_right,
                              a_delta)

    Button(lab6_w, width=15, text='Старт', bg='grey', command=func).place(x=220, y=445)



def config_lab7_window():
    lab7_w = Toplevel(bg='lightgrey')
    lab7_w.title('Лабораторная работа №7')
    lab7_w.resizable(False, False)
    lab7_w.geometry('1080x480+100+150')
    
    frame1 = LabelFrame(lab7_w, text='Параметры и топливный состав реактора ВВЭР', bg='lightgrey')
    frame1.place(x=10,y=10)    
    Label(frame1, width=72, height=21, bg='lightgrey').pack()
    
    Label(frame1,text='Значения плотностей веществ, г/см\N{SUPERSCRIPT THREE}',bg='lightgrey',relief=GROOVE).place(x=135, y=15)
    Label(frame1, text='Топливо', bg='lightgrey').place(x=40, y=50)
    Label(frame1, text='Диоксид урана', bg='lightgrey').place(x=200, y=50)
    gamma_fuel_korp = Entry(frame1, width=15)
    gamma_fuel_korp.insert(0, '10.4')
    gamma_fuel_korp.place(x=360, y=50)
    Label(frame1, text='Теплоноситель', bg='lightgrey').place(x=40, y=80)
    Label(frame1, text='Вода', bg='lightgrey').place(x=200, y=80)
    gamma_cool_korp = Entry(frame1, width=15)
    gamma_cool_korp.insert(0, '0.7')
    gamma_cool_korp.place(x=360, y=80)
    Label(frame1, text='Параметры реакторной установки ВВЭР', bg='lightgrey', relief=GROOVE).place(x=130, y=130)
    Label(frame1, text='Обогащение', bg='lightgrey').place(x=40, y=165)
    Label(frame1, text='Диаметр ТВЭЛа, мм', bg='lightgrey').place(x=40, y=200)
    Label(frame1, text='Толщина ТВЭЛа, мм', bg='lightgrey').place(x=40, y=235)
    x_korp = Entry(frame1, width=15)
    x_korp.place(x=360, y=165)
    d_korp = Entry(frame1, width=15)
    d_korp.place(x=360, y=200)
    δ_t_korp = Entry(frame1, width=15)
    δ_t_korp.place(x=360, y=235)    
    Label(frame1, text='Значение энергонапряженности, кВт/л', bg='lightgrey').place(x=40, y=270)
    qv_korp = Entry(frame1, width=15)
    qv_korp.insert(0, '110')
    qv_korp.place(x=360, y=270)

    frame2 = LabelFrame(lab7_w, text='Параметры и топливный состав канального реактора', bg='lightgrey')
    frame2.place(x=535, y=10)    
    Label(frame2, width=75, height=29, bg='lightgrey').pack()

    Label(frame2, text='Значения плотностей веществ, г/см\N{SUPERSCRIPT THREE}',bg='lightgrey', relief=GROOVE).place(x=150, y=10)
    Label(frame2, text='Топливо', bg='lightgrey').place(x=40, y=50)
    Label(frame2, text='Диоксид урана', bg='lightgrey').place(x=220, y=50)
    gamma_fuel_kan = Entry(frame2, width=15)
    gamma_fuel_kan.insert(0, '10.4')
    gamma_fuel_kan.place(x=390, y=50)
    Label(frame2, text='Теплоноситель', bg='lightgrey').place(x=40, y=80)
    cool = IntVar()
    cool.set(0)
    Radiobutton(frame2, text='H\N{SUBSCRIPT TWO}O', bg='lightgrey', variable=cool, value=1).place(x=200, y=80)
    Radiobutton(frame2, text='D\N{SUBSCRIPT TWO}O', bg='lightgrey', variable=cool, value=2).place(x=280, y=80)
    gamma_cool_kan = Entry(frame2, width=15)
    gamma_cool_kan.place(x=390, y=80)
    Label(frame2, text='Замедлитель', bg='lightgrey').place(x=40, y=110)   
    mod = IntVar()
    mod.set(0)
    Radiobutton(frame2, text='C', bg='lightgrey', variable=mod, value=1).place(x=200, y=110)
    Radiobutton(frame2, text='D\N{SUBSCRIPT TWO}O', bg='lightgrey', variable=mod, value=2).place(x=280, y=110)
    gamma_mod = Entry(frame2, width=15)
    gamma_mod.place(x=390, y=110)
    
    Label(frame2, text='Параметры канального реактора', bg='lightgrey', relief=GROOVE).place(x=145, y=150)
    Label(frame2, text='Обогащение', bg='lightgrey').place(x=40, y=180)
    x_kan = Entry(frame2, width=15)
    x_kan.place(x=390, y=180)
    Label(frame2, text='Диаметр ТВС, мм', bg='lightgrey').place(x=40, y=210)
    D = Entry(frame2, width=15)
    D.insert(0, '100')
    D.place(x=390, y=210)
    Label(frame2, text='Толщина оболочки ТВС, мм', bg='lightgrey').place(x=40, y=240)
    δ_tr = Entry(frame2, width=15)
    δ_tr.insert(0, '2.5')
    δ_tr.place(x=390, y=240)
    Label(frame2, text='Количество ТВЭЛов', bg='lightgrey').place(x=40, y=270)
    N = Entry(frame2, width=15)
    N.insert(0, '18')
    N.place(x=390, y=270)
    Label(frame2, text='Диаметр ТВЭЛа, мм', bg='lightgrey').place(x=40, y=300)
    d_kan = Entry(frame2, width=15)
    d_kan.place(x=390, y=300)
    Label(frame2, text='Толщина оболочки ТВЭЛа, мм', bg='lightgrey').place(x=40, y=330)
    δ_t_kan = Entry(frame2, width=15)
    δ_t_kan.place(x=390, y=330)
    Label(frame2, text='Значение энергонапряженности, кВт/л', bg='lightgrey').place(x=40, y=360)
    qv_kan = Entry(frame2, width=15)
    qv_kan.insert(0, '4.5')
    qv_kan.place(x=390, y=360)
    Label(frame2, text='Кол-во колец, на которые разбивается замедлитель', bg='lightgrey').place(x=40, y=390)
    n = Entry(frame2, width=15)
    n.insert(0, '5')
    n.place(x=390, y=390)

    Label(lab7_w, text='Шаг циклов расчета выгорания, сут', bg='lightgrey').place(x=50, y=390)
    step = Entry(lab7_w, width=15)
    step.insert(0, '0.25')
    step.place(x=370, y=390)

    func = lambda: start_lab7(d_korp, δ_t_korp, x_korp, gamma_fuel_korp,
                              gamma_cool_korp, qv_korp,
                              d_kan, δ_t_kan, D, δ_tr, N, x_kan, gamma_fuel_kan,
                              cool, mod, gamma_cool_kan, gamma_mod, n, qv_kan,
                              step)

    Button(lab7_w, text='Старт', width=15, bg='grey', command=func).place(x=230, y=430)


def config_lab8_window():
    pass


def config_window():
    window_num = var.get()
    if window_num <= 8:
        globals()['config_lab' + str(window_num) + '_window']()
    else:
        globals()['config_hw' + str(window_num - 8) + '_window']()


def start_lab1():
    pass


def start_lab2():
    pass


def start_lab3():
    pass


def start_lab4():
    pass


def start_lab5 (d, δ_t, x, gamma_fuel, gamma_cool, R_left, R_right,
                R_delta):
    x_str = x.get()
    x_lst = x_str.split(', ')
    x_lst = list(map(float, x_lst))
    labs.lab5(float(d.get())/10, float(δ_t.get())/10, x_lst,
              float(gamma_fuel.get()), float(gamma_cool.get()),
              float(R_left.get())/10, float(R_right.get())/10,
              float(R_delta.get())/10)
    mb.showinfo('Информация','Данные сохранены в директории ~bin\ФТЯР\LAB5')


def start_lab6(d, δ_t, D, δ_tr, N, x, gamma_fuel,
               cool, mod, gamma_cool, gamma_mod, n,
               a_left, a_right, a_delta):
    x_str = x.get()
    x_lst = x_str.split(', ')
    x_lst = list(map(float, x_lst))
    cool = 'h2o' if cool.get() == 1 else 'd2o'
    mod = 'c' if mod.get() == 1 else 'd2o'
    labs.lab6(float(d.get())/10, float(δ_t.get())/10, float(D.get())/10,
              float(δ_tr.get())/10, int(N.get()), x_lst,
              float(gamma_fuel.get()), cool, mod, float(gamma_cool.get()),
              float(gamma_mod.get()), int(n.get()), float(a_left.get())/10,
              float(a_right.get())/10, float(a_delta.get())/10)
    mb.showinfo('Информация','Данные сохранены в директории ~bin\ФТЯР\LAB6')


def start_lab7(d_korp, delta_korp, x_korp, gamma_fuel_korp, gamma_cool_korp,
               qv_korp,
               d_kan, delta_kan, D, Delta, num_of_fuel_rods, x_kan,
               gamma_fuel_kan, cool, mod, gamma_cool_kan, gamma_mod,
               num_of_mod_rings, qv_kan,
               step):
    cool = 'h2o' if cool.get() == 1 else 'd2o'
    mod = 'c' if mod.get() == 1 else 'd2o'
    labs.lab7(float(d_korp.get())/10, float(delta_korp.get())/10,
              float(x_korp.get()), float(gamma_fuel_korp.get()),
              float(gamma_cool_korp.get()), float(qv_korp.get()),

              float(d_kan.get())/10, float(delta_kan.get())/10,
              float(D.get())/10, float(Delta.get())/10,
              int(num_of_fuel_rods.get()), float(x_kan.get()),
              float(gamma_fuel_kan.get()), cool, mod,
              float(gamma_cool_kan.get()), float(gamma_mod.get()),
              int(num_of_mod_rings.get()), float(qv_kan.get()),

              float(step.get()))
    mb.showinfo('Информация','Данные сохранены в директории ~bin\ФТЯР\LAB7')


def start_lab8():
    pass


def start_hw1():
    pass


def start_hw2():
    pass


def start_hw3():
    pass


def start_hw4():
    pass


# создание главного окна и задание его параметров
root = Tk()
root.title('Лабораторные работы по ФТЯР на программном комплексе Getera')
root.resizable(False, False)
w = root.winfo_screenwidth() # ширина экрана
h = root.winfo_screenheight() # высота экрана
w = w//2 # середина экрана
h = h//2 
w = w - 450 # смещение от середины
h = h - 150
root.geometry('900x300+{}+{}'.format(w, h))
# создание радиокнопок на главном окне
var = IntVar()
var.set(0)
Radiobutton(text='Лабораторная работа №1', variable=var, value=1).place(relx=0.1, rely=0.1)
Radiobutton(text='Лабораторная работа №2', variable=var, value=2).place(relx=0.1, rely=0.3)
Radiobutton(text='Лабораторная работа №3', variable=var, value=3).place(relx=0.1, rely=0.5)
Radiobutton(text='Лабораторная работа №4', variable=var, value=4).place(relx=0.1, rely=0.7)
Radiobutton(text='Лабораторная работа №5', variable=var, value=5).place(relx=0.4, rely=0.1)
Radiobutton(text='Лабораторная работа №6', variable=var, value=6).place(relx=0.4, rely=0.3)
Radiobutton(text='Лабораторная работа №7', variable=var, value=7).place(relx=0.4, rely=0.5)
Radiobutton(text='Лабораторная работа №8', variable=var, value=8).place(relx=0.4, rely=0.7)
Radiobutton(text='Домашняя работа №1', variable=var, value=8).place(relx=0.7, rely=0.1)
Radiobutton(text='Домашняя работа №2', variable=var, value=8).place(relx=0.7, rely=0.3)
Radiobutton(text='Домашняя работа №3', variable=var, value=8).place(relx=0.7, rely=0.5)
Radiobutton(text='Домашняя работа №4', variable=var, value=8).place(relx=0.7, rely=0.7)
# создание кнопки "Далее" в нижней части главного окна(вызывает функцию
# config_window, которая отвечает за создание второстепенных окон)
Button(text='Далее', width=10,bg='lightgrey', command=config_window).place(relx=0.43, rely=0.85)
# метод запускает главный цикл обработки событий(в том числе отображает главное
# окно со всем содержимым на экране)
root.mainloop()
