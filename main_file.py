import tkinter as tk
from tkinter import messagebox as mb

import labs
import homeworks as hw


bg_color = 'lightgrey'


def config_lab1_widow():

    def start_lab1():
        pass

    pass


def config_lab2_window():

    def start_lab2():
        pass

    pass


def config_lab3_window():

    def start_lab3():
        pass

    pass


def config_lab4_window():

    def start_lab4():
        pass

    pass


def config_lab5_window():

    def start_lab5():
        x_lst = list(map(float, x.get().split(', ')))
        labs.lab5(float(d.get())/10, float(delta.get())/10,
                  float(r_left.get())/10, float(r_right.get())/10,
                  float(r_delta.get())/10, x_lst,
                  float(gamma_fuel.get()), float(gamma_cool.get()))
        mb.showinfo('Информация',
                    'Данные сохранены в директории ~lab5_result',
                    parent=lab5_w)

    lab5_w = tk.Toplevel(bg=bg_color)
    lab5_w.title('Лабораторная работа №5')
    lab5_w.resizable(False, False)
    lab5_w.geometry('530x340+700+150')

    frame_title = 'Значения плотностей веществ, г/см\N{SUPERSCRIPT THREE}'
    gamma_frame = tk.LabelFrame(lab5_w, text=frame_title, bg=bg_color)
    gamma_frame.place(x=10, y=10)
    tk.Label(gamma_frame, width=71, height=5, bg=bg_color).pack()
    tk.Label(gamma_frame, text='Топливо', bg=bg_color).place(x=40, y=10)
    tk.Label(gamma_frame, text='Диоксид урана', bg=bg_color).place(x=200, y=10)
    gamma_fuel = tk.Entry(gamma_frame, width=15)
    gamma_fuel.insert(0, '10.4')
    gamma_fuel.place(x=360, y=10)
    tk.Label(gamma_frame, text='Теплоноситель', bg=bg_color).place(x=40, y=40)
    tk.Label(gamma_frame, text='Вода', bg=bg_color).place(x=200, y=40)
    gamma_cool = tk.Entry(gamma_frame, width=15)
    gamma_cool.insert(0, '0.7')
    gamma_cool.place(x=360, y=40)

    frame_title = 'Параметры реактора ВВЭР'
    main_frame = tk.LabelFrame(lab5_w, text=frame_title, bg=bg_color)
    main_frame.place(x=10, y=120)
    tk.Label(main_frame, width=71, height=10, bg=bg_color).pack()
    tk.Label(main_frame, text='Обогащения (через запятую, от 0 до 1)',
             bg=bg_color).place(x=40, y=10)
    x = tk.Entry(main_frame, width=30)
    x.place(x=300, y=10)
    tk.Label(main_frame, text='Диаметр ТВЭЛа, мм',
             bg=bg_color).place(x=40, y=40)
    d = tk.Entry(main_frame, width=15)
    d.place(x=300, y=40)
    tk.Label(main_frame, text='Толщина ТВЭЛа, мм',
             bg=bg_color).place(x=40, y=70)
    delta = tk.Entry(main_frame, width=15)
    delta.place(x=300, y=70)
    tk.Label(main_frame, text='Диапазон значений шага решетки (мм) от',
             bg=bg_color).place(x=10, y=115)
    r_left = tk.Entry(main_frame, width=5)
    r_left.place(x=270, y=115)
    r_left.insert(0, '5')
    tk.Label(main_frame, text='до', bg=bg_color).place(x=310, y=115)
    r_right = tk.Entry(main_frame, width=5)
    r_right.insert(0, '15')
    r_right.place(x=340, y=115)
    tk.Label(main_frame, text='с шагом', bg=bg_color).place(x=380, y=115)
    r_delta = tk.Entry(main_frame, width=5)
    r_delta.insert(0, '0.5')
    r_delta.place(x=440, y=115)

    tk.Button(lab5_w, width=15, text='Старт', bg='grey',
              command=start_lab5).place(x=220, y=300)


def config_lab6_window():

    def start_lab6():
        x_lst = list(map(float, x.get().split(', ')))
        cool_name = 'h2o' if cool.get() == 1 else 'd2o'
        mod_name = 'c' if mod.get() == 1 else 'd2o'
        labs.lab6(float(d.get())/10, float(delta.get())/10,
                  int(fuel_rods_num.get()), float(d_assly.get())/10,
                  float(delta_assly.get())/10, float(a_left.get())/10,
                  float(a_right.get())/10, float(a_delta.get())/10,
                  int(mod_rings_num.get()), x_lst, float(gamma_fuel.get()),
                  cool_name, mod_name, float(gamma_cool.get()),
                  float(gamma_mod.get()))
        mb.showinfo('Информация',
                    'Данные сохранены в директории ~lab6_result',
                    parent=lab6_w)

    lab6_w = tk.Toplevel(bg=bg_color)
    lab6_w.title('Лабораторная работа №6')
    lab6_w.resizable(False, False)
    lab6_w.geometry('530x485+700+150')

    frame_title = 'Значения плотностей веществ, г/см\N{SUPERSCRIPT THREE}'
    gamma_frame = tk.LabelFrame(lab6_w, text=frame_title, bg=bg_color)
    gamma_frame.place(x=10, y=10)
    tk.Label(gamma_frame, width=71, height=7, bg=bg_color).pack()
    tk.Label(gamma_frame, text='Топливо', bg=bg_color).place(x=40, y=10)
    tk.Label(gamma_frame, text='Диоксид урана', bg=bg_color).place(x=170, y=10)
    gamma_fuel = tk.Entry(gamma_frame, width=15)
    gamma_fuel.insert(0, '10.4')
    gamma_fuel.place(x=360, y=10)
    tk.Label(gamma_frame, text='Теплоноситель', bg=bg_color).place(x=40, y=40)
    cool = tk.IntVar()
    cool.set(0)
    tk.Radiobutton(gamma_frame, text='H\N{SUBSCRIPT TWO}O', bg=bg_color,
                   variable=cool, value=1).place(x=170, y=40)
    tk.Radiobutton(gamma_frame, text='D\N{SUBSCRIPT TWO}O', bg=bg_color,
                   variable=cool, value=2).place(x=250, y=40)
    gamma_cool = tk.Entry(gamma_frame, width=15)
    gamma_cool.place(x=360, y=40)
    tk.Label(gamma_frame, text='Замедлитель', bg=bg_color).place(x=40, y=70)
    mod = tk.IntVar()
    mod.set(0)
    tk.Radiobutton(gamma_frame, text='C', bg=bg_color, variable=mod,
                   value=1).place(x=170, y=70)
    tk.Radiobutton(gamma_frame, text='D\N{SUBSCRIPT TWO}O', bg=bg_color,
                   variable=mod, value=2).place(x=250, y=70)
    gamma_mod = tk.Entry(gamma_frame, width=15)
    gamma_mod.place(x=360, y=70)

    frame_title = 'Параметры канального реактора'
    main_frame = tk.LabelFrame(lab6_w, text=frame_title, bg=bg_color)
    main_frame.place(x=10, y=155)
    tk.Label(main_frame, width=71, height=17, bg=bg_color).pack()
    tk.Label(main_frame, text='Обогащения (через запятую, от 0 до 1)',
             bg=bg_color).place(x=10, y=10)
    x = tk.Entry(main_frame, width=15)
    x.place(x=360, y=10)
    tk.Label(main_frame, text='Диаметр ТВС, мм', bg=bg_color).place(x=10, y=40)
    d_assly = tk.Entry(main_frame, width=15)
    d_assly.insert(0, '100')
    d_assly.place(x=360, y=40)
    tk.Label(main_frame, text='Толщина оболочки ТВС, мм',
             bg=bg_color).place(x=10, y=70)
    delta_assly = tk.Entry(main_frame, width=15)
    delta_assly.insert(0, '2.5')
    delta_assly.place(x=360, y=70)
    tk.Label(main_frame, text='Количество ТВЭЛов',
             bg=bg_color).place(x=10, y=100)
    fuel_rods_num = tk.Entry(main_frame, width=15)
    fuel_rods_num.insert(0, '18')
    fuel_rods_num.place(x=360, y=100)
    tk.Label(main_frame, text='Диаметр ТВЭЛа, мм',
             bg=bg_color).place(x=10, y=130)
    d = tk.Entry(main_frame, width=15)
    d.place(x=360, y=130)
    tk.Label(main_frame, text='Толщина оболочки ТВЭЛа, мм',
             bg=bg_color).place(x=10, y=160)
    delta = tk.Entry(main_frame, width=15)
    delta.place(x=360, y=160)
    tk.Label(main_frame, text='Диапазон значений шага решетки (мм) от',
             bg=bg_color).place(x=10, y=190)
    a_left = tk.Entry(main_frame, width=5)
    a_left.place(x=270, y=190)
    a_left.insert(0, '120')
    tk.Label(main_frame, text='до', bg=bg_color).place(x=310, y=190)
    a_right = tk.Entry(main_frame, width=5)
    a_right.insert(0, '400')
    a_right.place(x=335, y=190)
    tk.Label(main_frame, text='с шагом', bg=bg_color).place(x=380, y=190)
    a_delta = tk.Entry(main_frame, width=5)
    a_delta.insert(0, '20')
    a_delta.place(x=450, y=190)
    tk.Label(main_frame, text='Кол-во колец замедлителя',
             bg=bg_color).place(x=10, y=220)
    mod_rings_num = tk.Entry(main_frame, width=15)
    mod_rings_num.insert(0, '5')
    mod_rings_num.place(x=360, y=220)

    tk.Button(lab6_w, width=15, text='Старт', bg='grey',
              command=start_lab6).place(x=220, y=445)

'''
def config_lab7_window():

    def start_lab7():
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
                  float(step.get()), mode.get())
        mb.showinfo('Информация','Данные сохранены в директории ~lab7_result',
                    parent=lab7_w)

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

    Label(lab7_w, text='Шаг циклов расчета выгорания, сут', bg='lightgrey').place(x=50, y=400)
    step = Entry(lab7_w, width=15)
    step.insert(0, '0.25')
    step.place(x=370, y=400)

    Label(lab7_w, text='Режим работы', bg='lightgrey').place(x=50, y=370)
    mode = IntVar()
    mode.set(0)
    Radiobutton(lab7_w, text='1', variable=mode, value=1, bg='lightgrey').place(x=370, y=370)
    Radiobutton(lab7_w, text='2', variable=mode, value=2, bg='lightgrey').place(x=430, y=370)

    func = lambda: start_lab7(lab7_w, d_korp, δ_t_korp, x_korp, gamma_fuel_korp,
                              gamma_cool_korp, qv_korp, d_kan, δ_t_kan, D,
                              δ_tr, N, x_kan, gamma_fuel_kan, cool, mod,
                              gamma_cool_kan, gamma_mod, n, qv_kan, step, mode)

    Button(lab7_w, text='Старт', width=15, bg='grey', command=func).place(x=230, y=430)
'''

def config_lab8_window():

    def start_lab8():
        cool_name = 'h2o' if cool.get() == 1 else 'd2o'
        mod_name = 'c' if mod.get() == 1 else 'd2o'
        labs.lab8(float(d_korp.get())/10, float(delta_korp.get())/10,
                  float(x_korp.get()), float(gamma_fuel_korp.get()),
                  float(gamma_cool_korp.get()), float(qv_korp.get()),
                  float(d_kan.get())/10, float(delta_kan.get())/10,
                  int(fuel_rods_num.get()), float(d_assly.get())/10,
                  float(delta_assly.get())/10, int(mod_rings_num.get()),
                  float(x_kan.get()), float(gamma_fuel_kan.get()), cool_name,
                  mod_name, float(gamma_cool_kan.get()),
                  float(gamma_mod.get()), float(qv_kan.get()))
        mb.showinfo('Информация', 'Данные сохранены в директории ~lab8_result',
                    parent=lab8_w)

    lab8_w = tk.Toplevel(bg=bg_color)
    lab8_w.title('Лабораторная работа №8')
    lab8_w.resizable(False, False)
    lab8_w.geometry('1080x460+100+150')

    frame_title = 'Параметры и топливный корпусного реактора'
    korp_frame = tk.LabelFrame(lab8_w, text=frame_title, bg=bg_color)
    korp_frame.place(x=10, y=10)
    tk.Label(korp_frame, width=72, height=21, bg=bg_color).pack()
    frame_title = 'Значения плотностей веществ, г/см\N{SUPERSCRIPT THREE}'
    tk.Label(korp_frame, text=frame_title, bg=bg_color).place(x=135, y=15)
    tk.Label(korp_frame, text='Топливо', bg=bg_color).place(x=40, y=50)
    tk.Label(korp_frame, text='Диоксид урана', bg=bg_color).place(x=200, y=50)
    gamma_fuel_korp = tk.Entry(korp_frame, width=15)
    gamma_fuel_korp.insert(0, '10.4')
    gamma_fuel_korp.place(x=360, y=50)
    tk.Label(korp_frame, text='Теплоноситель', bg=bg_color).place(x=40, y=80)
    tk.Label(korp_frame, text='Вода', bg=bg_color).place(x=200, y=80)
    gamma_cool_korp = tk.Entry(korp_frame, width=15)
    gamma_cool_korp.insert(0, '0.7')
    gamma_cool_korp.place(x=360, y=80)
    tk.Label(korp_frame, text='Параметры корпусного реактора',
             bg=bg_color).place(x=130, y=130)
    tk.Label(korp_frame, text='Обогащение', bg=bg_color).place(x=40, y=165)
    tk.Label(korp_frame, text='Диаметр ТВЭЛа, мм',
             bg=bg_color).place(x=40, y=200)
    tk.Label(korp_frame, text='Толщина ТВЭЛа, мм',
             bg=bg_color).place(x=40, y=235)
    x_korp = tk.Entry(korp_frame, width=15)
    x_korp.place(x=360, y=165)
    d_korp = tk.Entry(korp_frame, width=15)
    d_korp.place(x=360, y=200)
    delta_korp = tk.Entry(korp_frame, width=15)
    delta_korp.place(x=360, y=235)
    tk.Label(korp_frame, text='Значение энергонапряженности, кВт/л',
             bg=bg_color).place(x=40, y=270)
    qv_korp = tk.Entry(korp_frame, width=15)
    qv_korp.insert(0, '110')
    qv_korp.place(x=360, y=270)

    frame_title = 'Параметры и топливный состав канального реактора'
    kan_frame = tk.LabelFrame(lab8_w, text=frame_title, bg=bg_color)
    kan_frame.place(x=535, y=10)
    tk.Label(kan_frame, width=75, height=28, bg=bg_color).pack()
    frame_title = 'Значения плотностей веществ, г/см\N{SUPERSCRIPT THREE}'
    tk.Label(kan_frame, text=frame_title, bg=bg_color).place(x=150, y=10)
    tk.Label(kan_frame, text='Топливо', bg=bg_color).place(x=40, y=50)
    tk.Label(kan_frame, text='Диоксид урана', bg=bg_color).place(x=220, y=50)
    gamma_fuel_kan = tk.Entry(kan_frame, width=15)
    gamma_fuel_kan.insert(0, '10.4')
    gamma_fuel_kan.place(x=390, y=50)
    tk.Label(kan_frame, text='Теплоноситель', bg=bg_color).place(x=40, y=80)
    cool = tk.IntVar()
    cool.set(0)
    tk.Radiobutton(kan_frame, text='H\N{SUBSCRIPT TWO}O', bg=bg_color,
                   variable=cool, value=1).place(x=200, y=80)
    tk.Radiobutton(kan_frame, text='D\N{SUBSCRIPT TWO}O', bg=bg_color,
                   variable=cool, value=2).place(x=280, y=80)
    gamma_cool_kan = tk.Entry(kan_frame, width=15)
    gamma_cool_kan.place(x=390, y=80)
    tk.Label(kan_frame, text='Замедлитель', bg=bg_color).place(x=40, y=110)
    mod = tk.IntVar()
    mod.set(0)
    tk.Radiobutton(kan_frame, text='C', bg=bg_color,
                   variable=mod, value=1).place(x=200, y=110)
    tk.Radiobutton(kan_frame, text='D\N{SUBSCRIPT TWO}O', bg=bg_color,
                   variable=mod, value=2).place(x=280, y=110)
    gamma_mod = tk.Entry(kan_frame, width=15)
    gamma_mod.place(x=390, y=110)
    tk.Label(kan_frame, text='Параметры канального реактора',
             bg=bg_color).place(x=145, y=150)
    tk.Label(kan_frame, text='Обогащение', bg=bg_color).place(x=40, y=180)
    x_kan = tk.Entry(kan_frame, width=15)
    x_kan.place(x=390, y=180)
    tk.Label(kan_frame, text='Диаметр ТВС, мм', bg=bg_color).place(x=40, y=210)
    d_assly = tk.Entry(kan_frame, width=15)
    d_assly.insert(0, '100')
    d_assly.place(x=390, y=210)
    tk.Label(kan_frame, text='Толщина оболочки ТВС, мм',
             bg=bg_color).place(x=40, y=240)
    delta_assly = tk.Entry(kan_frame, width=15)
    delta_assly.insert(0, '2.5')
    delta_assly.place(x=390, y=240)
    tk.Label(kan_frame, text='Количество ТВЭЛов',
             bg=bg_color).place(x=40, y=270)
    fuel_rods_num = tk.Entry(kan_frame, width=15)
    fuel_rods_num.insert(0, '18')
    fuel_rods_num.place(x=390, y=270)
    tk.Label(kan_frame, text='Диаметр ТВЭЛа, мм',
             bg=bg_color).place(x=40, y=300)
    d_kan = tk.Entry(kan_frame, width=15)
    d_kan.place(x=390, y=300)
    tk.Label(kan_frame, text='Толщина оболочки ТВЭЛа, мм',
             bg=bg_color).place(x=40, y=330)
    delta_kan = tk.Entry(kan_frame, width=15)
    delta_kan.place(x=390, y=330)
    tk.Label(kan_frame, text='Значение энергонапряженности, кВт/л',
             bg=bg_color).place(x=40, y=360)
    qv_kan = tk.Entry(kan_frame, width=15)
    qv_kan.insert(0, '4.5')
    qv_kan.place(x=390, y=360)
    tk.Label(kan_frame, text='Кол-во колец замедлителя',
             bg=bg_color).place(x=40, y=390)
    mod_rings_num = tk.Entry(kan_frame, width=15)
    mod_rings_num.insert(0, '5')
    mod_rings_num.place(x=390, y=390)

    tk.Button(lab8_w, text='Старт', width=15, bg='grey',
              command=start_lab8).place(x=230, y=415)

'''
def config_hw1_window():

    def start_hw1():
        pass

    pass


def config_hw2_window():

    def start_hw2():
        pass

    pass


def config_hw3_window():

    def start_hw3():
        x_lst = list(map(float, x.get().split(', ')))
        cool = 'h2o' if cool.get() == 1 else 'd2o'
        mod = 'c' if mod.get() == 1 else 'd2o'
        labs.lab6(float(d.get())/10, float(δ_t.get())/10, float(D.get())/10,
                  float(δ_tr.get())/10, int(N.get()), x_lst,
                  float(gamma_fuel.get()), cool, mod, float(gamma_cool.get()),
                  float(gamma_mod.get()), int(n.get()), float(a_left.get())/10,
                  float(a_right.get())/10, float(a_delta.get())/10)
        mb.showinfo('Информация','Данные сохранены в директории ~hw3_result,
                    parent=hw3_w)

    hw3_w = Toplevel(bg='lightgrey')
    hw3_w.title('Домашнее задание №3')
    hw3_w.resizable(False, False)
    hw3_w.geometry('530x485+700+150')
    
    frame1 = LabelFrame(hw3_w, text='Значения плотностей веществ, г/см\N{SUPERSCRIPT THREE}', bg='lightgrey')
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

    frame2 = LabelFrame(hw3_w, text='Параметры канального реактора', bg='lightgrey')
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

    func = lambda: start_hw3(hw3_w, d, δ_t, D, δ_tr, N, x, gamma_fuel, cool,
                             mod,gamma_cool, gamma_mod, n, a_left, a_right,
                             a_delta)

    Button(hw3_w, width=15, text='Старт', bg='grey', command=func).place(x=220, y=445)
    

def config_hw4_window():

    def start_hw4():
        cool = 'h2o' if cool.get() == 1 else 'd2o'
        mod = 'c' if mod.get() == 1 else 'd2o'
        hw.hw4(float(d.get())/10, float(delta.get())/10, float(x_u.get()),
               float(x_pu.get()), float(gamma_fuel.get()),
               float(gamma_cool_korp.get()), float(qv_korp.get()),
               float(D.get())/10, float(Delta.get())/10,
               int(num_of_fuel_rods.get()), cool, mod,
               float(gamma_cool_kan.get()), float(gamma_mod.get()),
               int(num_of_mod_rings.get()), float(qv_kan.get()))
        mb.showinfo('Информация','Данные сохранены в директории ~hw4_result',
                    parent=hw4_w)

    hw4_w = Toplevel(bg='lightgrey')
    hw4_w.title('Домашнее задание №4')
    hw4_w.resizable(False, False)
    hw4_w.geometry('1080x440+100+150')

    frame1 = LabelFrame(hw4_w, text='Параметры и топливный состав реактора ВВЭР', bg='lightgrey')
    frame1.place(x=10,y=10)    
    Label(frame1, width=72, height=18, bg='lightgrey').pack()
    
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
    Label(frame1, text='Обогащение по U\N{SUPERSCRIPT TWO}\N{SUPERSCRIPT THREE}\N{SUPERSCRIPT FIVE}', bg='lightgrey').place(x=40, y=165)
    Label(frame1, text='Обогащение по Pu\N{SUPERSCRIPT TWO}\N{SUPERSCRIPT THREE}\N{SUPERSCRIPT NINE}', bg='lightgrey').place(x=40, y=200)
    x_korp_u = Entry(frame1, width=15)
    x_korp_u.place(x=360, y=165)
    x_korp_pu = Entry(frame1, width=15)
    x_korp_pu.place(x=360, y=200)   
    Label(frame1, text='Значение энергонапряженности, кВт/л', bg='lightgrey').place(x=40, y=235)
    qv_korp = Entry(frame1, width=15)
    qv_korp.insert(0, '110')
    qv_korp.place(x=360, y=235)

    frame2 = LabelFrame(hw4_w, text='Параметры и топливный состав канального реактора', bg='lightgrey')
    frame2.place(x=535, y=10)    
    Label(frame2, width=75, height=24, bg='lightgrey').pack()

    Label(frame2, text='Значения плотностей веществ, г/см\N{SUPERSCRIPT THREE}',bg='lightgrey', relief=GROOVE).place(x=150, y=10)
    Label(frame2, text='Теплоноситель', bg='lightgrey').place(x=40, y=55)
    cool = IntVar()
    cool.set(0)
    Radiobutton(frame2, text='H\N{SUBSCRIPT TWO}O', bg='lightgrey', variable=cool, value=1).place(x=200, y=55)
    Radiobutton(frame2, text='D\N{SUBSCRIPT TWO}O', bg='lightgrey', variable=cool, value=2).place(x=280, y=55)
    gamma_cool_kan = Entry(frame2, width=15)
    gamma_cool_kan.place(x=390, y=55)
    Label(frame2, text='Замедлитель', bg='lightgrey').place(x=40, y=95)   
    mod = IntVar()
    mod.set(0)
    Radiobutton(frame2, text='C', bg='lightgrey', variable=mod, value=1).place(x=200, y=95)
    Radiobutton(frame2, text='D\N{SUBSCRIPT TWO}O', bg='lightgrey', variable=mod, value=2).place(x=280, y=95)
    gamma_mod = Entry(frame2, width=15)
    gamma_mod.place(x=390, y=95)
    
    Label(frame2, text='Параметры канального реактора', bg='lightgrey', relief=GROOVE).place(x=145, y=150)
    Label(frame2, text='Диаметр ТВС, мм', bg='lightgrey').place(x=40, y=185)
    D = Entry(frame2, width=15)
    D.insert(0, '100')
    D.place(x=390, y=185)
    Label(frame2, text='Толщина оболочки ТВС, мм', bg='lightgrey').place(x=40, y=220)
    δ_tr = Entry(frame2, width=15)
    δ_tr.insert(0, '2.5')
    δ_tr.place(x=390, y=220)
    Label(frame2, text='Количество ТВЭЛов', bg='lightgrey').place(x=40, y=255)
    N = Entry(frame2, width=15)
    N.insert(0, '18')
    N.place(x=390, y=255)
    Label(frame2, text='Значение энергонапряженности, кВт/л', bg='lightgrey').place(x=40, y=290)
    qv_kan = Entry(frame2, width=15)
    qv_kan.insert(0, '4.5')
    qv_kan.place(x=390, y=290)
    Label(frame2, text='Кол-во колец, на которые разбивается замедлитель', bg='lightgrey').place(x=40, y=325)
    n = Entry(frame2, width=15)
    n.insert(0, '5')
    n.place(x=390, y=325)
    
    Label(hw4_w, text='Диаметр ТВЭЛа, мм', bg='lightgrey').place(x=50, y=325)
    d = Entry(hw4_w, width=15)
    d.insert(0, '11')
    d.place(x=370, y=325)
    Label(hw4_w, text='Толщина ТВЭЛа, мм', bg='lightgrey').place(x=50, y=360)
    δ_t = Entry(hw4_w, width=15)
    δ_t.insert(0, '0.5')
    δ_t.place(x=370, y=360)
    
    func = lambda: start_hw4(hw4_w, d, δ_t, x_korp_u, x_korp_pu,
                             gamma_fuel_korp, gamma_cool_korp, qv_korp, D,
                             δ_tr, N, cool, mod, gamma_cool_kan, gamma_mod, n,
                             qv_kan)
    
    Button(hw4_w, text='Старт', width=15, bg='grey', command=func).place(x=480, y=405)
'''

def config_window(var):
    window_num = var.get()
    if window_num <= 8:
        globals()['config_lab' + str(window_num) + '_window']()
    else:
        globals()['config_hw' + str(window_num - 8) + '_window']()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Лабораторные работы по ФТЯР на программном комплексе Getera')
    root.resizable(False, False)
    w = root.winfo_screenwidth() // 2 - 450
    h = root.winfo_screenheight() // 2 - 150
    root.geometry('900x300+{}+{}'.format(w, h))
    var = tk.IntVar()
    var.set(0)
    for i in range(8):
        tk.Radiobutton(text='Лабораторная работа №' + str(i+1), variable=var,
                       value=1+i).place(relx=0.1+i//4*0.3, rely=0.1+i%4*0.2)
    for i in range(4):
        tk.Radiobutton(text='Домашняя работа №' + str(i+1), variable=var,
                       value=9+i).place(relx=0.7, rely=0.1+i%4*0.2)
    func = lambda: config_window(var)
    tk.Button(text='Далее', width=10, bg=bg_color,
              command=func).place(relx=0.43, rely=0.85)
    root.mainloop()
