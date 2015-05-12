# -*- coding: UTF-8 -*-
from math import *

def entrerMatrice():
	M=[[0,0,0],[0,0,0],[0,0,0]]
	for l in xrange(0,3):
		for i in xrange(0,3):
			print "Chiffre en (", l, ", ", i,")"
			M[l][i]=input()
	return M

def entrerPoint():
	P =[0,0,1]
	P[0]=input("X:")
	P[1]=input("Y:")
	return P

def additionMatrices(M1, M2):
	M=[[0,0,0],[0,0,0],[0,0,0]]
	for l in xrange(0,3):
		for i in xrange(0,3):
			M[l][i]=M1[l][i]+M2[l][i]
	return M

def afficherMatrice(M):
	for line in M:
		for x in line:
			print x, 
		print "\n"

def afficherPoint(P):
	print "point en (", P[0],",", P[1],",", P[2],")"

def afficherPolygone(poly):
	for j in xrange(0,len(poly)):
		afficherPoint(poly[j])

def afficherFigure(figure):
	for j in xrange(0, len(figure)):
		afficherPolygone(figure[j])

def raw_afficherMatrice(M):
	string=""
	for line in M:
		for x in line:
			string += str(round(x, 2))
			string += "\t"
		string += "\n"
	return string

def raw_afficherPoint(P):
	string = "("+str(P[0])+","+str(P[1])+","+str(P[2])+")"
	return string

def raw_afficherPolygone(poly):
	string="[ "
	for j in xrange(0,len(poly)):
		string += raw_afficherPoint(poly[j])
		if j < len(poly)-1:
			string += ","
	string += " ]"
	return string

def raw_afficherFigure(figure):
	string="[ "
	for j in xrange(0,len(figure)):
		string += raw_afficherPolygone(figure[j])
		if j < len(figure)-1:
			string += ", "
	string += " ]"
	return string

def produitMatrices(M1, M2):
	M=[[0,0,0],[0,0,0],[0,0,0]]
	for l in xrange(0,3):
		for i in xrange(0,3):
			s=0
			for p1 in xrange(0,3):
				s+= M1[l][p1]*M2[p1][i]
			M[l][i]=s
	return M

def produitMatricePoint(M, P):
	Pbis=[0,0,0]
	Pbis[0]=M[0][0]*P[0]+M[0][1]*P[1]+M[0][2]*P[2]
	Pbis[1]=M[1][0]*P[0]+M[1][1]*P[1]+M[1][2]*P[2]
	Pbis[2]=M[2][0]*P[0]+M[2][1]*P[1]+M[2][2]*P[2]

	return Pbis

def puissanceMatrice(M1, n):
	M=M1
	while n>=2:
		M = produitMatrices(M, M1)
		n-=1
	return M

def matriceRot(angle):
	M=[[cos(angle),-sin(angle),0],[sin(angle),cos(angle),0],[0,0,1]]
	return M

def matriceHom(k):
	M=[[k,0,0],[0,k,0],[0,0,1]]
	return M

def matriceTrans(x,y):
	M=[[1,0,x],[0,1,y],[0,0,1]]
	return M

def matriceRotAt(angle, x, y):
	M1 = matriceTrans(x, y)
	M2 = matriceRot(angle)
	M3 = matriceTrans(-x, -y)

	return produitMatrices(M1, produitMatrices(M2, M3))

def matriceHomAt(k, x, y):
	M1 = matriceTrans(x, y)
	M2 = matriceHom(k)
	M3 = matriceTrans(-x, -y)

	return produitMatrices(M1, produitMatrices(M2, M3))

def saisiePolygone():
	n = input("Combien de points contient ce polygone ?")
	poly = []
	for x in xrange(0,n):
		poly.append(entrerPoint())
	return poly

def ajouterPoint(poly, point):
	poly.append(point)
	return poly

def createFigure():
	return []

def addPolygone(figure, polygone):
	figure.append(polygone)
	return figure

def transformerFigure(figure, matrice):
	for j in xrange(0,len(figure)):
		for i in xrange(0,len(figure[j])):
			figure[j][i]=produitMatricePoint(matrice, figure[j][i])
	return figure
