



from datetime import datetime
from email import message



from fpdf import FPDF
import sqlite3
import pickle
from io import open

from tkinter import *
from tkinter import messagebox as MessageBox
from tkinter.ttk import Combobox


from tkcalendar import Calendar, DateEntry




###################################################BASE DE DATIS PRACTICA#######################
conexion = sqlite3.connect("basedatos.db")
cursor = conexion.cursor()
try:
        cursor.execute("""
                CREATE TABLE viajes2 (
                Aviso INTEGER PRIMARY KEY,
                Origen VARCHAR(30),
                Destino VARCHAR(30),
                Km INTEGER,
                Descripcion VARCHAR(50),
                Precio REAL,
                Fecha DATE
            )
        """)
except:
        pass
#cursor.execute("INSERT INTO viajes2 VALUES ('87655646','Jaen','Granada','123','Un viaje ameno','0,25','11-12-1981')")



#cursor.execute( "INSERT INTO viajes VALUES (98765463,'Madrid','Jaen',345)")
#TRAVEL = [
#    ("jAEN","Ubeda",45),
#    ("Ubeda","Linares",67),
#    ("Linares","retorno",56)
#]

#cursor.executemany("INSERT INTO viajes VALUES (?,?,?)",TRAVEL) #insertar masivamente datos

#cursor.execute("SELECT * FROM viajes ") #recuperar datos masivos en una sola consulta
#viajesss = cursor.fetchall()
#print(viajesss)

                


###############################################################################################
raiz = Tk()
raiz.geometry("800x600")
raiz.config(bg="black")
raiz.title("Mi ventana")
raiz.resizable(FALSE,FALSE)
def IntroducirPrecio():
        
        def GrabaPrecio():
                
                fichero = open("precio.pck","wb")
                fichero.seek(0)
                pickle.dump(PrecioGas.get(),fichero)
                fichero.close()
                MessageBox.showinfo("Agregar vehiculo","Precio Establecido")
                VentanaPrecio.destroy()
        VentanaPrecio = Toplevel(raiz)
        VentanaPrecio.geometry("300x200")
        Label(VentanaPrecio,text="Introduzca Precio Gasoil").pack(side="top")
        PrecioGas = Entry(VentanaPrecio,text="")
        PrecioGas.pack(side="top")
        Button(VentanaPrecio,text="Aceptar",command=GrabaPrecio).pack(side="top")
        

def callback(eventObject):
       conexion = sqlite3.connect("basedatos.db")
       cursor = conexion.cursor()

       cursor.execute("SELECT * FROM coches WHERE matri='{}'".format(CuadroCombo.get()))
       cadena = cursor.fetchone()
       
       conexion.commit()
       cursor.close()
       fichero = open("precio.pck","ab+")
       fichero.seek(0)
       p = pickle.load(fichero)
       

       fichero.close()
       letrerocoche.config(text=cadena[0] + " " + cadena[1] + "\nPrecio{}/KM".format(p) )


def ValidaDatos():
        fichero = open("precio.pck","ab+")
        fichero.seek(0)
        p = pickle.load(fichero)
        fichero.close()
        numerico = Aviso.get()
        Kilometrico = Kmm.get()
        if numerico.isdigit() and Kilometrico.isdigit():

                conexion = sqlite3.connect("basedatos.db")
                cursor = conexion.cursor()
                cursor.execute("INSERT INTO viajes2 VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(Aviso.get(),Origen.get(),Destino.get(),Kmm.get(),0,p,cal.get_date(),CuadroCombo.get()))
                texto.insert(INSERT,"\nAVISO {}\n{}=====>{}  ({})Km\n\n".format(Aviso.get(),Origen.get(),Destino.get(), Kmm.get() ))
                conexion.commit()
                cursor.close()
                BorraCampos()
        else:
                MessageBox.showerror("Error","El campo Aviso y el campo Kilometros debe ser numérico")
                

                
def BorraCampos():
        Aviso.delete(0,"end")
        Origen.delete(0,"end")
        Destino.delete(0,"end")
        #Notas.delete(0,"end")
        Kmm.delete(0,"end")
        
        

def informes():
        


        def InformePDF(lista):
                """
                p: Portrait
                l: Landscape
                a4: 210x297mm
                
                """
                
                pdf = FPDF(orientation="P", unit="mm", format="A4")
                pdf.add_page()
                pdf.set_text_color(r=185,g=16,b=16) #red

                pdf.set_font("Arial","B",20)
                pdf.set_fill_color(r=176,g=174,b=227)

                pdf.image("Visual Code\Kilometros\dn.jpg",x=6,y=7,w=50,h=25)
                pdf.cell(w=50,h=1,border=0)
                pdf.multi_cell(w=0,h=9,border=0,align="C",fill=0 ,txt="Relacion de viajes comprendidos entre {} Y {}".format(b.get_date(),a.get_date()))
                pdf.set_text_color(r=0,g=0,b=0)
                pdf.set_font("Arial","",10)
                #pdf.line(10,20,200,20)
                pdf.set_top_margin(10)
                pdf.set_fill_color(r=36,g=51,b=159)
                pdf.cell(w=0,h=5,align="C",ln=3)
                pdf.set_font("Arial","",15)
                pdf.cell(w=30,h=5,txt="Aviso",align="C",border=1,fill=1)
                pdf.cell(w=50,h=5,txt="Origen",align="C",border=1,fill=1)
                pdf.cell(w=50,h=5,txt="Destino",align="C",border=1,fill=1)
                pdf.cell(w=20,h=5,txt="Fecha",align="C",border=1,fill=1)

                pdf.multi_cell(w=0,h=5,txt="Kilómetros",align="C",border=1,fill=1)
                pdf.set_font("Arial","",10)
                pdf.set_fill_color(r=234,g=233,b=255)
                for i,lis in enumerate(lista):
                        
                        pdf.cell(w=30,h=5,txt=str(lis[0]),align="C",fill=1,border=1)
                        pdf.cell(w=50,h=5,txt=lis[1],align="C",fill=1,border=1)
                        pdf.cell(w=50,h=5,txt=lis[2],align="C",fill=1,border=1)
                        pdf.cell(w=20,h=5,txt=lis[6],align="C",fill=1,border=1)

                        pdf.multi_cell(w=0,h=5,txt=str(lis[3]),align="C",fill=1,border=1)


                """pdf.cell(w=30,h=10,txt="HOla",align="C",border=1)
                pdf.cell(w=30,h=10,txt="HOla",align="C",border=1)
                pdf.cell(w=30,h=10,txt="HOla",align="C",border=1)
                pdf.multi_cell(w=0,h=10,txt="HOla",align="C",border=1)
                """
                sumakm = []
                for l in lista:
                        sumakm.append(l[3])
                pdf.set_font("Arial","B",26)
                pdf.cell(w=30,h=40,txt="{} kilómetros en total".format(sum(sumakm)))
                pdf.output("rafa.pdf")
                
        def HazInforme(*args):
               
                lista = []
                print(a.get_date(),b.get_date())
                
                conexion = sqlite3.connect("basedatos.db")
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM viajes2 WHERE coche='{}' AND Fecha BETWEEN '{}' AND '{}' ORDER BY Fecha ".format(CuadroCombo.get(),b.get_date(),a.get_date()))
                lista = cursor.fetchall()
                conexion.commit()
                cursor.close()
                
                #Button(v_informes,text="Salir",background="black",foreground="orange", font=("Fixedsys",24)).place(x=100,y=260)
                if len(lista)!=0:
                        if MessageBox.askyesnocancel("Registros encontrardos","Se han encontrado {} registros\n\n¿Desea descargarlo en PDF?".format(len(lista))) == True:
                               InformePDF(lista)
                               
                        else:
                                print("no queremos descargarlo")
        
        v_informes = Toplevel(raiz,background="black")
        v_informes.geometry("500x500")
        Frame(v_informes,relief="groove",border=2,background="black").place(x=100,y=100,width=300,height=180)
        Label(v_informes,background="orange",text="INFORMES",font=("Fixedsys",26), border="13", relief="sunken",width=10,height=1).pack(side="top", pady=15)
        Label(v_informes,text="Seleccione periodo de avisos",background="black",foreground="orange", font=("Fixedsys",14)).pack(pady=5)
        SV1 = StringVar()
        SV2 = StringVar()
        
        b = DateEntry(v_informes,textvariable = SV1,date_pattern="yyyy/mm/dd", bordercolor="black", normalbackground="orange", foreground='white', weekendbackground="black",normalforeground='white', headersforeground='black')
        b.place(x=230,y=170,width=100,height=20)
        b._set_text("Elije fecha")
        Label(v_informes,text="Desde",background="black",foreground="orange", font=("Fixedsys",14)).place(x=130,y=170,width=100,height=20)
        Label(v_informes,text="Hasta",background="black",foreground="orange", font=("Fixedsys",14)).place(x=130,y=200,width=100,height=20)
        a = DateEntry(v_informes,textvariable = SV2, bordercolor="black",date_pattern="yyyy/mm/dd", normalbackground="orange", foreground='white', weekendbackground="black",normalforeground='white', headersforeground='black')
        a.place(x=230,y=200,width=100,height=20)
        a._set_text("Elije fecha")
        
        Button(v_informes,command = HazInforme ,text = "Buscar",background="black",foreground="orange",font=("Fixedsys",14)).place(x=220,y=240,width=80,height=30)

        #SV1.trace("w",yo que se) #YA LO ENTIENDO, cuando sv1 que es stringvar cambia de valor se ejecuta tal funcion
        



def AgregarCoche():
        def GuardarCoche():
                try:
                        idviaje = int(0)
                        ListaVehiculos = []
                        ListaVehiculos.append(matricula.get())
                        ListaVehiculos.append(marca.get())
                        ListaVehiculos.append(modelo.get())
                        
                        conexion = sqlite3.connect("basedatos.db")
                        cursor = conexion.cursor()
                        cursor.execute("INSERT INTO coches VALUES ('{}','{}','{}')".format(matricula.get(),marca.get(),modelo.get(),0))

                        conexion.commit()
                        cursor.close()
                        MessageBox.showinfo("Agregar vehiculo","Vehiculo dado de alta")
                except sqlite3.IntegrityError:
                        MessageBox.showerror("Error","Matricula existente")

        matricula = StringVar()
        marca = StringVar()
        modelo = StringVar()
        ventana = Toplevel(raiz) 
        ventana.title("Agregar coche") 
        ventana.geometry("350x300") 
        ventana.config(background="black")
        
        Label(ventana,text="Introducir vehiculo",background="black",foreground="orange",relief="sunken",font=("Fixedsys",24),border=3).pack(side="top")
        Frame(ventana,background="orange",relief="sunken",border=5).place(x=40,y=60,width=260,height=200)
        Button(ventana,text="Guardar",background="black",foreground="orange",command=GuardarCoche).place(x=125,y=200,width=90,height=40 )
        Label(ventana,text ="Matricula",background="black",foreground="orange",font=("Fixedsys",14),relief="groove",border=1).place(x=50,y=100,width=120,height=25) 
        Label(ventana,text ="Marca",background="black",foreground="orange",font=("Fixedsys",14),relief="groove",border=1).place(x=50,y=130,width=120,height=25) 
        Label(ventana,text ="Modelo",background="black",foreground="orange",font=("Fixedsys",14),relief="groove",border=1).place(x=50,y=160,width=120,height=25) 
        Entry(ventana,width=10,background="orange",textvariable=matricula).place(x=180,y=100,width=100,height=25)
        Entry(ventana,width=10,background="orange",textvariable=marca).place(x=180,y=130,width=100,height=25)
        Entry(ventana,width=10,background="orange",textvariable=modelo).place(x=180,y=160,width=100,height=25)


def hola():
        print("hola")
                
        
def Alclicar():

    letreto.config(text="Datos a fecha {}".format(str(cal.get_date())))
    Fecha.delete(0,"end")
    Fecha.config(textvariable=Fecha)
    Fecha.insert(0,cal.get_date() )
def CambioLetreros():

        letreto.config(text="Datos a fecha {}".format(str(cal.get_date())))
        Fecha.delete(0,"end")
        Fecha.config(textvariable=Fecha)
        Fecha.insert(0,cal.get_date() )

def my_upd(*args): # triggered when value of string varaible changes se activa cuando cambia el valor de la variable
    
    
    letreto.config(text="Datos a fecha {}".format(str(cal.get_date())))
    texto.delete(1.0,"end")
    #Fecha.delete(0,"end")
    Fecha.config(text=cal.get_date())
    
    conexion = sqlite3.connect("basedatos.db")
    cursor = conexion.cursor()
        #cursor.execute("INSERT INTO viajes2 VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(Aviso.get(),Origen.get(),Destino.get(),Kmm.get(),0,0,Fecha.get(),CuadroCombo.get()))
        
    cursor.execute("SELECT * FROM viajes2 WHERE fecha ='{}' AND coche='{}' ORDER BY Fecha".format(cal.get_date(),CuadroCombo.get()))
    resultado = cursor.fetchall()
    if len(resultado)!=0:
            texto.insert(INSERT,"DATOS A FECHA {}\n\n".format(cal.get_date()) )
            for i,re in enumerate (resultado):
                #print("\nAVISO {}\n{}=====>{}  ({})Km".format(re[0],re[1],re[2],re[3]) )
                texto.insert(INSERT,"\nAVISO nº {}\n{}=====>{}  ({})Km\n".format(re[0],re[1],re[2],re[3])) #
                
         ########################################aqui te has quedado , debes intenar llenar este cuadro de texo con viajes
    else:
            texto.insert(INSERT,"No hay datos")
    conexion.commit()
def BorraVehiculo():
        def BorrarVe():
                
                if MessageBox.askyesno("Borrar Vehiculo","¿Desea borrar vehiculo con matricula {}".format(ComboVehiculo.get())):
                        conexion = sqlite3.connect("basedatos.db")
                        cursor = conexion.cursor()
                        cursor.execute("Delete FROM viajes2 WHERE coche='{}'".format(ComboVehiculo.get()))
                        conexion.commit()
                        cursor.execute("Delete FROM coches WHERE matri='{}'".format(ComboVehiculo.get()))
                        conexion.commit()
                        cursor.close()
                        MessageBox.showinfo("Aviso","Vehiculo Borrado")
                        Ventanaborra.destroy()
                else:
                        Ventanaborra.destroy()
                                
        Ventanaborra = Toplevel(raiz,background="black")
        Ventanaborra.geometry("300x200")
        
        Label(Ventanaborra,text="Borrar Vehiculo",foreground="orange",background="black" ,font=("Fixedsys",23)).pack(side="top")
        conexion = sqlite3.connect("basedatos.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT matri FROM coches")
        listavehiculo = cursor.fetchall()
        ComboVehiculo = Combobox(Ventanaborra,text="",values=listavehiculo)
        ComboVehiculo.pack(side="top")
        Button(Ventanaborra,text="Aceptar",command=BorrarVe).pack(side="top")
        conexion.commit()
        cursor.close()
        
        conexion.commit()
        cursor.close()

"""Aviso = StringVar()
Origen = StringVar()
Destino = StringVar()
km = IntVar()
Fecha = StringVar()
Notas = StringVar()
Precio = StringVar()
"""


#Aqui vamos a configurar el calendario
SV = StringVar()

cal = Calendar(raiz,textvariable = SV, bordercolor="black", date_pattern="yyyy-mm-dd", normalbackground="orange", foreground='white', weekendbackground="black",normalforeground='white', headersforeground='black', selectmode = 'day')

cal.place(x=420,y=60,width=320,height=200)
SV.trace('w',my_upd) 
#lupa2 = PhotoImage(file="Visual Code\Kilometros\lupa.png")
#lupa = lupa2.subsample(8,8)
Button(raiz,text="Actualiza",command=Alclicar,background="black",foreground="orange",compound="top").place(x=155,y=190,width=80,height=80)
LabelFecha = StringVar()
LabelFecha = cal.get_date()

calendario = PhotoImage(file="Visual Code\Kilometros\cruzverde.png")
calendario2 = calendario.subsample(8,8)
# Configurarmos la GUI en general
Button(raiz,bd=3,text="Agregar vehiculo",foreground = "black",background="orange",command=AgregarCoche).place(x=60,y=190,width=100,height=40)
Frame(raiz,border=4,relief="groove",bg="black").place(x=60,y=280,width=320,height=250)
Label(raiz,text="Aviso",foreground="orange",font=("Fixedsys",14),justify= "right",background="black",border=1,relief="groove").place(x=80,y=300,width=120,height=25)
Aviso = Entry(raiz,width=10,background="black",foreground="orange", cursor="hand2",font=("Fixedsys",14))
Aviso.place(x=230,y=300,width=120,height=20)
Label(raiz,text="Origen",foreground="orange",font=("Fixedsys",14),justify= "right",background="black",border=1,relief="groove").place(x=80,y=330,width=120,height=25)
Origen = Entry(raiz,width=10,background="black", foreground="orange",font=("Fixedsys",14))
Origen.place(x=230,y=330,width=120,height=20)
Label(raiz,text="Destino",foreground="orange",font=("Fixedsys",14),justify= "right",background="black",border=1,relief="groove").place(x=80,y=360,width=120,height=25)
Destino = Entry(raiz,width=10,background="black",foreground="orange",font=("Fixedsys",14))
Destino.place(x=230,y=360,width=120,height=20)
Label(raiz,text="Fecha",foreground="orange",font=("Fixedsys",14),justify= "right",background="black",border=1,relief="groove").place(x=80,y=390,width=120,height=25)
Fecha = Label(raiz,width=10,background="black", foreground="orange",border=1,relief="groove",font=("Fixedsys",14))
Fecha.place(x=230,y=390,width=120,height=20)

#Fecha.insert(INSERT,cal.get_date())
Label(raiz,text="km",foreground="orange",font=("Fixedsys",14),justify= "right",background="black",border=1,relief="groove").place(x=80,y=420,width=120,height=25)
Kmm = Entry(raiz,width=10,background="black",foreground="orange",font=("Fixedsys",14))
Kmm.place(x=230,y=420,width=120,height=20)
Label(raiz,text="Notas",foreground="orange",font=("Fixedsys",14),justify= "right",background="black",border=1,relief="groove").place(x=80,y=450,width=120,height=25)
Notas = Text(raiz,width=10,background="black",foreground="orange",font=("Fixedsys",14))
Notas.place(x=230,y=450,width=120,height=70)

#imagevalidar = PhotoImage(file="Visual Code/Kilometros/validar.png")
#photo = imagevalidar.subsample(8,8)
Button(raiz,compound="left",text="Validar",font = ("Fixedsys",14),bg="orange",foreground="black",command=ValidaDatos).place(x=90,y=485,width=105,height=40)
letreto = Label(raiz,text="Datos a fecha {}".format(LabelFecha),font=("Fixedsys",20),background="black",foreground="orange",border=2,relief="groove")
letreto.pack(side="top")
texto = Text(raiz,border=4,background="black",foreground="orange",font=("Fixedsys",10))
texto.place(x=420,y=280,width=320,height=250)

#texto.insert(INSERT,"No hay datos..")


#texto.config(state="disabled")
#borrar = PhotoImage(file="Visual Code\Kilometros/borrar.png")
#borrar2 = borrar.subsample(8,8)
Button(raiz,bg="orange",text="Borrar Vehiculo",background="orange",foreground="black",command=BorraVehiculo).place(x=60,y=237,width=100,height=40)

furgoneta = PhotoImage(file="Visual Code\Kilometros/furgoneta.gif")
furgoneta2 = furgoneta.subsample(3,3)
#Label(raiz,image=furgoneta2,background="black").place(x=110,y=60, width=120, height=80)
letrerocoche = "Elija un coche..."
letrerocoche = Label(raiz,font=("Fixedsys",24),image=furgoneta2, compound="top", background="black",foreground="orange",text=letrerocoche)
letrerocoche.place(x=60,y=60)

conexion = sqlite3.connect("basedatos.db")
cursor = conexion.cursor()
cursor.execute("SELECT matri FROM coches")
vehiculos = cursor.fetchall()
conexion.commit()
cursor.close()


CuadroCombo = Combobox(raiz,values=vehiculos)

CuadroCombo.set ("Elije un coche")

CuadroCombo.place(x=250,y=190,width=128,height=20)
CuadroCombo.bind("<<ComboboxSelected>>", callback)





#Frame(raiz,width=400,height=100,bg="Red").grid(row=0,column=3)
#Button(raiz,text="Seleccionar vehiculo",command=SeleccionCoche ,background="black",font=("Fixedsys",10),foreground="orange",relief="groove",border=4).pack()

menubar = Menu(raiz)
raiz.config(menu=menubar)
menubar.config(background="orange")



archivo = Menu(menubar,tearoff=False)
opciones = Menu(menubar,tearoff=False)
ayuda = Menu(menubar,tearoff=False)

menubar.add_cascade(label="Archivo",menu=archivo)
menubar.add_cascade(label="Opciones",menu=opciones)
menubar.add_cascade(label="Ayuda",menu=ayuda)

archivo.add_command(label="Nuevo")
archivo.add_command(label="Abrir")
archivo.add_command(label="Guardar")
archivo.add_command(label="Guardar como")
archivo.add_separator()
archivo.add_command(label="Salir",command=raiz.quit())

opciones.add_command(label="Introducir viajes")
opciones.add_command(label="Busqueda")
opciones.add_command(label="Establecer precio del gasoil",command=IntroducirPrecio)
opciones.add_command(label="Seleccion vehiculo")
opciones.add_command(label="Informes",command=informes)


raiz.mainloop()



"""ESTE CODIGO ES PARA QUE AL PULSAR VALIDAR APAREZCA EN EL TEXT TODA LA INFO DE ESE DIA FORMATEADA CON ORIGEN DETINO Y KM
onexion = sqlite3.connect("basedatos.db")
        cursor = conexion.cursor()
        #cursor.execute("INSERT INTO viajes2 VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(Aviso.get(),Origen.get(),Destino.get(),Kmm.get(),0,0,Fecha.get(),CuadroCombo.get()))
        
        cursor.execute("SELECT * FROM viajes2 WHERE fecha ='{}' AND coche='{}'".format(cal.get_date(),CuadroCombo.get()))
        resultado = cursor.fetchall()
        for i,re in enumerate (resultado):
                #print("\nAVISO {}\n{}=====>{}  ({})Km".format(re[0],re[1],re[2],re[3]) )
                texto.insert(INSERT,"\nAVISO {}\n{}=====>{}  ({})Km".format(re[0],re[1],re[2],re[3])) #
                
         ########################################aqui te has quedado , debes intenar llenar este cuadro de texo con viajes

        conexion.commit()


"""