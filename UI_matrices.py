# -*- coding: UTF-8 -*-
from Tkinter import *
from matrices import *
from math import *
from copy import *


class mainUI(Frame):
	"""docstring for mainUI"""
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.start()
		
	def start(self):
		"""Fonction éxécutée à la création de la fenètre, on affiche le canvas, les boutons pour accéder aux différentes boites de dialogue (saisie du polygone, création de
			la matrice de transformation. On initialise les différentes variables du programme, et on lance la boucle de tkinter."""
		self.master.title('Affichage des figures')
		self.master.configure(width=700, height=500, bg="ivory")
		self.can = Canvas(self.master, height=400, width=400, bg="light yellow", cursor="trek")
		self.can.pack(side=LEFT)
		self.traceRepere()
		self.quitter = Button(self.master, text="Quitter", command=self.quit, bg="ivory")
		self.quitter.pack(side=BOTTOM)
		self.commencer = Button(self.master, text="Éditer le polygone", command=self.askUserP, bg="ivory")
		self.commencer.pack(side=TOP)
		self.transformer = Button(self.master, text="Éditer la transformation", command=self.askUserT, bg="ivory")
		self.transformer.pack(side=TOP)
		self.drawB = Button(self.master, text="Figure de base", command=self.drawBase, bg="ivory")
		self.drawB.pack(side=TOP)
		self.drawT = Button(self.master, text="Figure transformée", command=self.drawTrans, bg="ivory")
		self.drawT.pack(side=TOP)
		self.demo = Button(self.master, text="Démonstration", command=self.interactivite, bg="ivory")
		self.demo.pack(side=TOP)

		self.matriceTransfo = []
		self.matriceFinale = []
		self.transformRadio=IntVar()
		self.figureBase = createFigure()
		self.figureTrans = createFigure()
		self.oldFigure = []
		self.polygone = []
		self.mainloop()
		

	def traceRepere(self):
		"""Fonction qui permet de tracer le repère dans le canvas, elle trace également un cadrillage."""
		
		for i in xrange(0,41):
			self.can.create_line(i*10, 0, i*10, 400, fill="yellow")
			self.can.create_line(0, i*10, 400, i*10, fill="yellow")

		self.can.create_line(0, 200, 400, 200, fill ='orange')
		self.can.create_line(200, 400, 200, 0, fill ='orange')
	
	def coordPoint(self, valeur, x=True):
		"""Fonction qui corrige les coordonnées pour centrer le (0,0) sur le canvas."""
		if x:
			return valeur + 200
		else:
			return 200 - valeur

	def drawBase(self):
		"""Fonction qui dessine la figure entrée par l'utilisateur"""
		self.traceFigure(self.figureBase)

	def drawTrans(self):
		"""Fonction qui affiche la figure transformée par la matrice"""
		self.traceFigure(self.figureTrans)

	def traceLigne(self, pointa, pointb):
		"""trace une ligne sur le Canvas en prenant en compte que (0,0) est au centre de ce dernier"""
		self.can.create_line(self.coordPoint(pointa[0]), self.coordPoint(pointa[1], False), self.coordPoint(pointb[0]), self.coordPoint(pointb[1], False), fill='black')

	def tracePoly(self, poly):
		"""Trace les lignes entre tous les points d'un polygone"""
		for j in xrange(1,len(poly)):
			self.traceLigne(poly[j-1], poly[j])
		self.traceLigne(poly[0], poly[-1])

	def traceFigure(self, figure, clear=True):
		"""Trace la figure. Si clear vaut True, on nettoie le canvas et on retrace le repère, sinon on écrit par dessus."""
		if clear :
			self.can.delete(ALL)
			self.traceRepere()
		for j in xrange(0,len(figure)):
			self.tracePoly(figure[j])
		self.update()

	def interactivite(self):
		"""Fonction qui affiche une petite démonstration"""
		figure = [[[-1, 1, 0], [1,1,0], [1,-1,0], [-1,-1,0]]]
		self.traceFigure(figure)
		foisdeux = matriceHom(20)
		self.traceFigure(transformerFigure(figure, foisdeux))
		self.traceFigure(transformerFigure(figure, matriceRot(pi/4)), False)
		foisdeux = matriceHom(2)
		self.traceFigure(transformerFigure(figure, foisdeux), False)
		self.traceFigure(transformerFigure(figure, matriceRot(pi/4)), False)
		self.traceFigure(transformerFigure(figure, foisdeux), False)
		self.traceFigure(transformerFigure(figure, matriceRot(pi/4)), False)
		self.traceFigure(transformerFigure(figure, foisdeux), False)
		self.traceFigure(transformerFigure(figure, matriceRot(pi/4)), False)


	def askUserP(self):
		"""Affiche la fenètre d'entrée de la figure. On ajoute chaque point à un polygone puis le polygone à la figure."""
		self.prompt = Toplevel()
		self.prompt.minsize(500, 300)
		self.prompt.title("Pimp My Polygon")
		self.prompt.config(bg="ivory")
		self.prompt.labX = Label(self.prompt, width=3, text="X =", bg="ivory")
		self.prompt.labX.pack(side=LEFT)
		self.prompt.inputX = Entry(self.prompt, width=5, bg="white")
		self.prompt.inputX.pack(side=LEFT)
		self.prompt.labY = Label(self.prompt, width=3, text="Y =", bg="ivory")
		self.prompt.labY.pack(side=LEFT)
		self.prompt.inputY = Entry(self.prompt, width=5, bg="white")
		self.prompt.inputY.pack(side=LEFT)
		self.prompt.addP = Button(self.prompt, text="Ajouter ce point au polygone", command=self.postPointPoly, bg="ivory")
		self.prompt.addP.pack(side=LEFT)
		self.prompt.addF = Button(self.prompt, text="Ajouter ce polygone à la figure", command=self.postPolyFigure, bg="ivory")
		self.prompt.addF.pack(side=BOTTOM)
		self.prompt.resetP = Button(self.prompt, text="Remettre à zéro", command=self.resetPoly, bg="ivory")
		self.prompt.resetP.pack(side=BOTTOM)
		self.prompt.resume = Text(self.prompt, bg="white", height=20, width=60,foreground='dark green')
		self.prompt.resume.pack(side=TOP)
		self.prompt.resume.insert('1.0', "Entrez les coordonnées des points ci contre")
		self.prompt.resume.config(state=DISABLED)
		self.refreshResume()

	def postPointPoly(self):
		"""Ajoute le point au polygone"""
		x = int(self.prompt.inputX.get())
		y = int(self.prompt.inputY.get())
		ajouterPoint(self.polygone, [x, y, 1])
		self.refreshResume()

	def postPolyFigure(self):
		"""Ajouter la le point à la figure"""
		if len(self.polygone) > 1:
			addPolygone(self.figureBase, self.polygone)
			self.polygone = []
			self.refreshResume()

	def resetPoly(self):
		"""Remet à zero le polygone"""
		self.polygone = []
		self.figureBase = []
		self.refreshResume()

	def refreshResume(self):
		"""Afficher les informations du polygone et la figure actuelle"""
		resume_poly_figure = "Polygone actuel : \n"
		resume_poly_figure += raw_afficherPolygone(self.polygone)
		resume_poly_figure += "\n\nFigure :\n"
		resume_poly_figure += raw_afficherFigure(self.figureBase)
		self.prompt.resume.config(state=NORMAL)
		self.prompt.resume.delete('0.0', END)
		self.prompt.resume.insert('1.0', resume_poly_figure)
		self.prompt.resume.config(state=DISABLED)
		resume_poly_figure = ""

	def askUserT(self):
		"""Affiche la fenetre permettant de choisir les transformations à appliquer"""
		self.prompt2 = Toplevel()
		self.prompt2.minsize(500, 300)
		self.prompt2.title("Pimp My Matrice")
		self.prompt2.config(bg="ivory")

		self.prompt2.frame1 = Frame(self.prompt2, width=350, bg="ivory")
		self.prompt2.frame1.pack(side=LEFT, fill=BOTH)
		self.prompt2.rad1 = Radiobutton(self.prompt2.frame1, bg="ivory", variable=self.transformRadio, value=1, command=self.updateAfterRadio)
		self.prompt2.rad1.grid(row=0, column=0)
		self.prompt2.lab1 = Label(self.prompt2.frame1, bg="ivory", width=18, text="Translation")
		self.prompt2.lab1.grid(row=0, column=1)
		self.prompt2.rad2 = Radiobutton(self.prompt2.frame1, bg="ivory", variable=self.transformRadio, value=2, command=self.updateAfterRadio)
		self.prompt2.rad2.grid(row=1, column=0)
		self.prompt2.lab2 = Label(self.prompt2.frame1, bg="ivory", width=18, text="Rotation")
		self.prompt2.lab2.grid(row=1, column=1)
		self.prompt2.rad3 = Radiobutton(self.prompt2.frame1, bg="ivory", variable=self.transformRadio, value=3, command=self.updateAfterRadio)
		self.prompt2.rad3.grid(row=2, column=0)
		self.prompt2.lab3 = Label(self.prompt2.frame1, bg="ivory", width=18, text="Homothétie")
		self.prompt2.lab3.grid(row=2, column=1)
		self.prompt2.rad4 = Radiobutton(self.prompt2.frame1, bg="ivory", variable=self.transformRadio, value=4, command=self.updateAfterRadio)
		self.prompt2.rad4.grid(row=3, column=0)
		self.prompt2.lab4 = Label(self.prompt2.frame1, bg="ivory", width=18, text="Rotation décalée")
		self.prompt2.lab4.grid(row=3, column=1)
		self.prompt2.rad5 = Radiobutton(self.prompt2.frame1, bg="ivory", variable=self.transformRadio, value=5, command=self.updateAfterRadio)
		self.prompt2.rad5.grid(row=4, column=0)
		self.prompt2.lab5 = Label(self.prompt2.frame1, bg="ivory", width=18, text="Homothétie décalée")
		self.prompt2.lab5.grid(row=4, column=1)
		

		self.prompt2.labX = Label(self.prompt2.frame1, bg="ivory", width=3, text="X =")
		self.prompt2.labX.grid(row=5, column=0)
		self.prompt2.TransX = Entry(self.prompt2.frame1, bg="white", width=5)
		self.prompt2.TransX.grid(row=5, column=1)
		self.prompt2.labY = Label(self.prompt2.frame1, bg="ivory", width=3, text="Y =")
		self.prompt2.labY.grid(row=6, column=0)
		self.prompt2.TransY = Entry(self.prompt2.frame1, bg="white", width=5)
		self.prompt2.TransY.grid(row=6, column=1)
		self.prompt2.labK = Label(self.prompt2.frame1, bg="ivory", width=3, text="K =")
		self.prompt2.labK.grid(row=7, column=0)
		self.prompt2.coef = Entry(self.prompt2.frame1, bg="white", width=5)
		self.prompt2.coef.grid(row=7, column=1)
		self.prompt2.labAngle = Label(self.prompt2.frame1, bg="ivory", text="Angle =", width=7)
		self.prompt2.labAngle.grid(row=8, column=0)
		self.prompt2.angle = Entry(self.prompt2.frame1, bg="white", width=5)
		self.prompt2.angle.grid(row=8, column=1)
		self.prompt2.MatApp = Button(self.prompt2.frame1, bg="ivory", text="Générer la matrice", command=self.genreMatrice)
		self.prompt2.MatApp.grid(row=10, column=0)
		self.prompt2.MatVal = Button(self.prompt2.frame1, bg="ivory", text="Valider la matrice", command=self.validateMatrice)
		self.prompt2.MatVal.grid(row=11, column=0)


		self.prompt2.TransX.config(state=DISABLED)
		self.prompt2.TransY.config(state=DISABLED)
		self.prompt2.coef.config(state=DISABLED)
		self.prompt2.angle.config(state=DISABLED)
		self.prompt2.MatVal.config(state=DISABLED)



		self.prompt2.transB = Button(self.prompt2, bg="ivory", text="Appliquer cette matrice", command=self.Transforme)
		self.prompt2.transB.pack(side=BOTTOM)
		self.prompt2.resetT = Button(self.prompt2, bg="ivory", text="Remettre à zéro", command=self.ResetMatrices)
		self.prompt2.resetT.pack(side=BOTTOM)
		self.prompt2.resumeM = Text(self.prompt2, bg="white", height=20, width=50,foreground='dark green')
		self.prompt2.resumeM.pack(side=TOP)
		self.prompt2.resumeM.insert('1.0', "Créer votre matrice de transformation ci contre")
		self.prompt2.resumeM.config(state=DISABLED)
		self.refreshResumeM()

	def genreMatrice(self):
		"""Recupère le type de transformation et les paramètres correspondants"""
		c = self.transformRadio.get()

		if c==1:
			x= eval(self.prompt2.TransX.get())
			y= eval(self.prompt2.TransY.get())
			self.matriceTransfo=matriceTrans(x, y)
		elif c==2:
			angle= eval(self.prompt2.angle.get())
			self.matriceTransfo=matriceRot(angle)
		elif c==3:
			k= eval(self.prompt2.coef.get())
			self.matriceTransfo=matriceHom(k)
		elif c==4:
			x= eval(self.prompt2.TransX.get())
			y= eval(self.prompt2.TransY.get())
			angle= eval(self.prompt2.angle.get())
			self.matriceTransfo=matriceRotAt(angle, x, y)
		elif c==5:
			x= eval(self.prompt2.TransX.get())
			y= eval(self.prompt2.TransY.get())
			k= eval(self.prompt2.coef.get())
			self.matriceTransfo=matriceHomAt(k, x, y)
		else:
			pass

		self.prompt2.MatVal.config(state=NORMAL)
		self.refreshResumeM()

	def validateMatrice(self):
		"""Genere une matrice équivalente à toutes les transformations voulues"""
		if len(self.matriceFinale)==0:
			self.matriceFinale = self.matriceTransfo
		else :
			self.matriceFinale = produitMatrices(self.matriceTransfo, self.matriceFinale)
		self.matriceTransfo = []
		self.refreshResumeM()

	def updateAfterRadio(self):
		"""Affiche les champs qu'il faut remplir pour la transformation sélectionnée"""
		c = self.transformRadio.get()
		self.prompt2.TransX.config(state=DISABLED)
		self.prompt2.TransY.config(state=DISABLED)
		self.prompt2.coef.config(state=DISABLED)
		self.prompt2.angle.config(state=DISABLED)
		if c==1:
			self.prompt2.TransX.config(state=NORMAL)
			self.prompt2.TransY.config(state=NORMAL)
		elif c==2:
			self.prompt2.angle.config(state=NORMAL)
		elif c==3:
			self.prompt2.coef.config(state=NORMAL)
		elif c==4:
			self.prompt2.TransX.config(state=NORMAL)
			self.prompt2.TransY.config(state=NORMAL)
			self.prompt2.angle.config(state=NORMAL)
		elif c==5:
			self.prompt2.TransX.config(state=NORMAL)
			self.prompt2.TransY.config(state=NORMAL)
			self.prompt2.coef.config(state=NORMAL)
		else:
			pass

	def refreshResumeM(self):
		"""Affiche les informations des matrices de transformation"""
		resume_Matrices = "Matrice générée: \n"
		resume_Matrices += raw_afficherMatrice(self.matriceTransfo)
		resume_Matrices += "\nMatrice finale: \n"
		resume_Matrices += raw_afficherMatrice(self.matriceFinale)

		self.prompt2.resumeM.config(state=NORMAL)
		self.prompt2.resumeM.delete('0.0', END)
		self.prompt2.resumeM.insert('1.0', resume_Matrices)
		self.prompt2.resumeM.config(state=DISABLED)

	def ResetMatrices(self):
		"""Remet les deux matrices à zéro"""
		self.matriceTransfo = []
		self.matriceFinale = []
		self.refreshResumeM()

	def Transforme(self):
		"""Applique la transformation"""
		self.oldFigure=deepcopy(self.figureBase)
		self.figureTrans = transformerFigure(self.figureBase, self.matriceFinale)
		self.figureBase = deepcopy(self.oldFigure)

test = mainUI()
