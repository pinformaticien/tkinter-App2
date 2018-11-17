from tkinter import *
from tkinter import ttk
import sqlite3

class Etudiant:
    con = 0
    cur = 0
    etudiant_selected = 0


    #creation de la base de donnees et la table Etudiants.
    def create_db(self):
        self.con = sqlite3.connect('etudiant.db')
        self.cur = self.con.cursor()

        try:
            self.con.execute("CREATE TABLE if not exists Etudiants (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Prenom TEXT NOT NULL, Nom TEXT NOT NULL);")
            self.con.commit()
        except sqlite3.OperationalError:
            print("Echec de creation de la table Etudiants.")


    def register(self):
        self.con.execute("INSERT INTO Etudiants (Prenom, Nom) VALUES (?, ?)", (self.fn_entry_value.get(), self.ln_entry_value.get()))
        self.con.commit()

        self.fn_entry.delete(0, "end")
        self.ln_entry.delete(0, "end")
        

        self.mise_a_jour()
    
    
    def mise_a_jour(self):
        self.list_box.delete(0, END)

        try:
            result = self.cur.execute("SELECT ID, Prenom, Nom FROM Etudiants")

            for row in result:
                id_etu = row[0]
                prenom_etu = row[1]
                nom_etu = row[2]

                self.list_box.insert(id_etu, prenom_etu + " " + nom_etu)
        

        except sqlite3.OperationalError:
            print("Erreur Table inexistante.")
        except:
            print("1: Donnees non existantes.")

    

    def charge_etudiant(self, event = None):
        lb_widget = event.widget
        index = str(lb_widget.curselection()[0] + 1)


        self.etudiant_selected = index

        try:
            result = self.cur.execute("SELECT ID, Prenom, Nom FROM Etudiants WHERE ID="+self.etudiant_selected)

            for row in result:
                prenom_etu = row[1]
                nom_etu = row[2]

                
                self.fn_entry_value.set(prenom_etu)
                self.ln_entry_value.set(nom_etu)

        
        except sqlite3.OperationalError:
            print("Table inexistante.")

        
        except:
            print("2 : Donnees non trouvees.")

        




    def mise_a_jour_etudiant(self, event=None):
        try:
            self.con.execute("UPDATE Etudiants SET Prenom = '" + self.fn_entry_value.get() + "', Nom='" + self.ln_entry_value.get() + "' WHERE ID=" + self.etudiant_selected)
            self.con.commit()

        
        except sqlite3.OperationalError:
            print("Database couldn't be updated.")

        
        self.fn_entry.delete(0, "end")
        self.ln_entry.delete(0, "end")
        
        self.mise_a_jour()






    def __init__(self, root):
        root.title("Systeme de Gestion des Etudiants")
        root.iconbitmap('university.ico')
        root.geometry("650x500+120+160")

        formEtudiant = LabelFrame(root, text='Formulaire', width=250, height=150, fg='blue')
        lb_space = Label(root)

        lb_space.grid(row=0, column=0)
        formEtudiant.place(x=40, y=40)
        formEtudiant.grid_propagate(0)

        fn_label = ttk.Label(formEtudiant, text='prenom')
        fn_label.grid(row=0, column=0)

        ln_label = ttk.Label(formEtudiant, text='nom')
        ln_label.grid(row=2, column=0)

        self.fn_entry_value = StringVar(root, value="")
        self.fn_entry = ttk.Entry(formEtudiant, textvariable=self.fn_entry_value)
        self.fn_entry.grid(row=0, column=1)

        en_space = Label(formEtudiant).grid(row=1, column=1)

        self.ln_entry_value = StringVar(root, value="")
        self.ln_entry = ttk.Entry(formEtudiant, textvariable=self.ln_entry_value)
        self.ln_entry.grid(row=2, column=1)

        btn_space = Label(formEtudiant).grid(row=3)

        submit = ttk.Button(formEtudiant, text="Enregistrer", command = self.register)
        submit.grid(row=4, column=0)

        update = ttk.Button(formEtudiant, text='Modifier', command = self.mise_a_jour_etudiant)
        update.grid(row=4, column=1)

        formListe = LabelFrame(root, text='RESULTATS', width=270, height=270)
        formListe.place(x=40, y=200)
        formListe.grid_propagate(0)



        scrollbar = Scrollbar(formListe)

        self.list_box = Listbox(formListe, width=40, height=15)
        self.list_box.grid(row=0, column=0, columnspan=7, rowspan=7)
        self.list_box.bind('<<ListboxSelect>>', self.charge_etudiant)


        scrollbar.grid(row=0, column=7)
        self.list_box.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.list_box.yview)

        self.create_db()

        self.mise_a_jour()

       


root = Tk()
etudiant = Etudiant(root)

root.mainloop()