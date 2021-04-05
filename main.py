from tkinter import *
import tkinter.messagebox as mb


# Подключение к базе данных
def create_connection():
    import pyodbc
    server = 'sql-serverartem.ddns.net\ARTEM_HOME_SQL'
    database = 'Kursovaya'
    username = 'kursach'
    password = 'kursach'
    driver = '{SQL Server}'
    port = '54432'
    conn = pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';PORT=' + port + ';DATABASE=' + database + ';UID=' + username +
        ';PWD=' + password)
    return conn


c = create_connection()
print('ok')


def add_item():
    if len(styp_name.get()) > 4 and len(styp_money.get()) > 0:
        try:
            maxz = c.execute("SELECT TOP 1 stipendia_id FROM stipendia_list ORDER BY stipendia_id DESC").fetchone()[0]
            maxz += 1
            c.execute("INSERT INTO stipendia_list VALUES (?,?,?)", (maxz, str(styp_name.get()), str(styp_money.get())))
            c.commit()
            box.insert(END, styp_name.get())
            styp_name.delete(0, END)
            styp_money.delete(0, END)
        except:
            from tkinter import messagebox as mb
            mb.showerror(title="ОШИБКА!",
                         message="ПРОВЕРЬТЕ ВВЕДЕНЫЕ ДАННЫЕ!\n"
                                 "Автора данного проекта заставляют работать за бесплатно")


def del_list():
    global chose_stip
    select = list(box.curselection())
    select.reverse()
    if len(select) > 0:
        for i in select:
            sela = box.get(i)
            c.execute("DELETE FROM stipendia_list WHERE stipendia_type = '" + str(sela) + "'")
            c.commit()
            box.delete(i)
            chose_stip = 'не выбрана'


chose_stip = 'не выбрана'
chose_stud = 'никто'
stud_id = ''


def choose_stip():
    global chose_stip
    select = list(box.curselection())
    select.reverse()
    if len(select) > 0:
        chose_stip = box.get(select[0])
        show_info('Выбран: ' + str(chose_stud) + ' и ' + str(chose_stip) + ' стипендия')


def show_info(text):
    msg = text
    mb.showinfo("Информация", msg)


def choose_stud():
    global chose_stud, stud_id
    select = list(boxst.curselection())
    select.reverse()
    if len(select) > 0:
        chose_stud = boxst.get(select[0])
        spl_string = chose_stud.split()
        stud_id = spl_string[-1]
        rm = spl_string[:-1]
        chose_stud = ' '.join([str(elem) for elem in rm])
        show_info('Выбран: ' + str(chose_stud) + ' и ' + str(chose_stip) + ' стипендия')


def give_stud_stip():
    if chose_stip != 'не выбрана' and chose_stud != 'никто':
        stip_id = c.execute("SELECT stipendia_id FROM stipendia_list WHERE stipendia_type = '" + str(chose_stip) + "'").fetchall()[0][0]
        check = c.execute("SELECT kod_student, stipendia_id FROM stud_money WHERE kod_student = '" + str(stud_id) + "' AND stipendia_id = '" + str(stip_id) + "'").fetchall()
        if len(check) == 0:
            c.execute("INSERT INTO stud_money VALUES (?,?)", (str(stud_id), str(stip_id)))
            c.commit()
            show_info('Стипендия успешно выдана данному студенту!')
        else:
            mb.showerror(title="ОШИБКА!",
                         message="Данный студент уже получает этот вид стипендии!")
    else:
        mb.showwarning(title="Осторожнее с кнопочками!",
                       message="Выберите студента или тип стипендии!")


def del_stud_stip():
    if chose_stip != 'не выбрана' and chose_stud != 'никто':
        stip_id = c.execute("SELECT stipendia_id FROM stipendia_list WHERE stipendia_type = '" + str(chose_stip) + "'").fetchall()[0][0]
        check = c.execute("SELECT kod_student, stipendia_id FROM stud_money WHERE kod_student = '" + str(stud_id) + "' AND stipendia_id = '" + str(stip_id) + "'").fetchall()
        if len(check) != 0:
            c.execute("DELETE FROM stud_money WHERE kod_student = '" + str(stud_id) + "' AND stipendia_id = '" + str(stip_id) +"'")
            c.commit()
            show_info('Данный студент больше не получает этот вид стипендии')
        else:
            mb.showerror(title="ОШИБКА!",
                         message="Данный студент не получает этот вид стипендии!")
    else:
        mb.showwarning(title="Осторожнее с кнопочками!",
                       message="Выберите студента или тип стипендии!")


def check_stud_stip():
    if stud_id != 'никто':
        check = c.execute("SELECT stipendia_list.stipendia_type, stipendia_list.stipendia_money "
                          "FROM stipendia_list, stud_money "
                          "WHERE stud_money.stipendia_id = stipendia_list.stipendia_id "
                          "AND stud_money.kod_student = '" + str(stud_id) + "'").fetchall()
        sum_stip = 0
        for i in check:
            sum_stip += i[1]
        stip_text = ''
        for i in range(len(check)):
            stip_text += check[i][0]
            if i != len(check) - 1:
                stip_text += ', '
        show_info('Стипендии студента: ' + str(stip_text) + '\nна сумму: ' + str(sum_stip) + ' рублей')
    else:
        mb.showwarning(title="Осторожнее с кнопочками!",
                       message="Выберите студента или тип стипендии!")


def del_stud():
    global chose_stud
    select = list(boxst.curselection())
    select.reverse()
    if len(select) > 0:
        for i in select:
            sela = boxst.get(i)
            c.execute("DELETE FROM dannie WHERE kod_student = '" + str(sela.split()[3]) + "'")
            c.commit()
            boxst.delete(i)
            chose_stud = 'никто'


def add_student():
    if len(stud_sb.get()) > 0:
        try:
            c.execute("INSERT INTO dannie VALUES (?,?,?,?,?,?,?,?)", (stud_sb.get(), stud_fam.get(), stud_name.get(),
                                                                      stud_otch.get(), stud_dr.get(), stud_pd.get(),
                                                                      stud_num.get(), stud_gp.get()))
            c.commit()
            boxst.insert(END, (stud_fam.get() + ' ' + stud_name.get() + ' ' + stud_otch.get() + '                                       ' + str(stud_sb.get())))
            stud_sb.delete(0, END)
            stud_fam.delete(0, END)
            stud_name.delete(0, END)
            stud_otch.delete(0, END)
            stud_dr.delete(0, END)
            stud_pd.delete(0, END)
            stud_num.delete(0, END)
            stud_gp.delete(0, END)
        except:
            mb.showerror(title="ОШИБКА!",
                         message="ПРОВЕРЬТЕ ВВЕДЕНЫЕ ДАННЫЕ!\n"
                                 "Автора данного проекта заставляют работать за бесплатно")


def stud_list():
    list_stud = c.execute("SELECT fam, name, otch, kod_student FROM dannie").fetchall()
    for i in range(len(list_stud)):
        boxst.insert(END, (list_stud[i][0] + ' ' + list_stud[i][1] + ' ' + list_stud[i][2] + '                                       ' + str(list_stud[i][3])))


def stip_list():
    list_st = c.execute("SELECT stipendia_type FROM stipendia_list").fetchall()
    for i in range(len(list_st)):
        box.insert(END, (list_st[i][0]))


root = Tk()

f = Frame()
f.pack(side=LEFT, padx=10)
Label(f, text="Название стипендии").pack(fill=X)
styp_name = Entry(f)
styp_name.pack(anchor=N)
Label(f, text="Сумма стипендии").pack(fill=X)
styp_money = Entry(f)
styp_money.pack(anchor=N)
Button(f, text="Добавить новый тип стипендии", command=add_item).pack(fill=X)
Button(f, text="Удалить тип стипендии", command=del_list).pack(fill=X)
# Button(f, text="Save", command=save_list) \
#     .pack(fill=X)
box = Listbox(width=30, height=10)
box.pack(side=LEFT)
scroll = Scrollbar(command=box.yview)
scroll.pack(side=LEFT, fill=Y)
box.config(yscrollcommand=scroll.set)
fs = Frame()
fs.pack(side=LEFT, padx=10)
Button(fs, text="Выбрать стипендию", command=choose_stip).pack(fill=X)
Button(fs, text="Выбрать студента", command=choose_stud).pack(fill=X)
Button(fs, text="Дать студенту стипендию", command=give_stud_stip).pack(fill=X)
Button(fs, text="Забрать стиппендию у студента", command=del_stud_stip).pack(fill=X)
Button(fs, text="Показать стипендии студента", command=check_stud_stip).pack(fill=X)

boxst = Listbox(width=30, height=10)
boxst.pack(side=LEFT)
scrollst = Scrollbar(command=boxst.yview)
scrollst.pack(side=LEFT, fill=Y)
boxst.config(yscrollcommand=scrollst.set)

fa = Frame()
fa.pack(side=LEFT, padx=30)
Label(fa, text="Имя").pack(fill=X)
stud_name = Entry(fa)
stud_name.pack()
Label(fa, text="Фамилия").pack(fill=X)
stud_fam = Entry(fa)
stud_fam.pack()
Label(fa, text="Отчество").pack(fill=X)
stud_otch = Entry(fa)
stud_otch.pack()
Label(fa, text="День рождения").pack(fill=X)
stud_dr = Entry(fa)
stud_dr.pack()
Label(fa, text="Паспортные данные").pack(fill=X)
stud_pd = Entry(fa)
stud_pd.pack()
Label(fa, text="Номер телефона").pack(fill=X)
stud_num = Entry(fa)
stud_num.pack()
Label(fa, text="Номер группы").pack(fill=X)
stud_gp = Entry(fa)
stud_gp.pack()
Label(fa, text="Номер студенческого").pack(fill=X)
stud_sb = Entry(fa)
stud_sb.pack()
fa = Frame()
fa.pack(side=LEFT, padx=30)
Button(fa, text="Добавить студента", command=add_student).pack(fill=X)
Button(fa, text="Удалить студента", command=del_stud).pack(fill=X)
stip_list()
stud_list()
root.mainloop()
