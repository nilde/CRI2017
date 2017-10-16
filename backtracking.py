
#objetos a guardar
'''
self.dictionary=[]
self.D=[ [ [ pal1,pal2,pal3] , [ipal11,ipal12,...] ],[...],... ]
self.restdict=[[4,[poscom1]]
self.lva=[]
self.lvna=list(range(11, 17))
words_list=[[pos1,pos2,...,pos,],[...]]

'''

import numpy as np

class Backtracking:
	def __init__(self,R,lvna,file_dict,longitudes_apuntadores,longitudes_conjuntas,orient_word_list,crosses):
		#
		#
		#

		
		self.dictionary=open(file_dict, 'r')
		self.R=R
		self.D=[[] for i in range(len(longitudes))]
		self.lva={}
		self.lvna=lvna
		#Hay que generar
		self.words_list=[]
		self.num_words=len(n2r)
		self.longitudes=[[]]
		self.orient_word_list
		self.longitudes_apuntadores=longitudes_apuntadores
		self.longitudes_conjuntas=longitudes_conjuntas
		self.big_dictionary_list=[]

		generateCorrectDict()
	
		self.dictionary.close()

		self.all_crosses={}
		generateDomains()


	def generateCorrectDict(self):
		for word in self.dictionary:
			self.big_dictionary_list.append(word)

	def generateDomains(self):
		#En teoria genera los indices en las posiciones correctas
		for index,each_word in enumerate(self.big_dictionary_list):
			for indice,conjunto in enumerate(self.D):
				if len each_word == self.longitudes[indice]:
					self.D[conjunto].append[index]



	def generate_cruces_dict(self):
		for i in self.orient_word_list:
			self.all_crosses[i]=[]
			for each_cross in self.cruces:
				if i in each_word:
					aux=aux.append(self.all_crosses[i])[:]
					aux.append(i)


	def satisfiesConstraints(self,asignacion,palabra):
		#REEScribir
		# En teoria en este punto no puede haber palabras de longitud diferente a la adecuada
		all_crosses_word=self.all_croses[palabra]
		for cross in all_crosses_word:
			#Busco el cruce
			cross=self.crosses[i]
			#Miro si mi palabra esta la primera o la ultima en el cruce
			if cross[0]==palabra:
				x=cross[1]
				pos_x=cross[3]
				pos_y=cross[2]
			else:
				x=cross[0]
				pos_x=cross[2]
				pos_y=cross[3]

			#En teoria tiene que estar ordenado y si no lo esta lo ordeno previamente
			if x not in self.lvna:
				break
				for i in self.lva:
					#Si se encuentra la palabra en la lista pero no cumple las condiciones de cruce
					if i[0]==x and asignacion[pos_x]!=i[1][pos_y]:
					return False 
		return True

	def isCompleteSolution(self,solution):
		# Mira si la longitud de la lista de soluciones es correcta(T / F)
		
		if len(solution)==self.num_words:
			return True
		return False

	def domain(self,var):
		return all_possibilities

	def resolve_backtracking(self, lva, lvna):
		#Funcion que va a resolver el backtracking
		#
		#Output:

		# We cant assign more values
		if not self.lvna:
			return self.lva
		# Get variable to assign and its D
		var = [self.lvna[0],'']
		# Loop over the possibilities of the domain(that function returns a list)
		for asignableValue in self.domain(var[0]):
			if self.satisfiesConstraints(asignableValue,var[0]):
				res = self.backtracking(lva.append([var,asignableValue]),lvna[1:],self.R,self.D)
				if self._isCompleteSolution(res):
					return res
		return None

	def updateDomains(self):
		#
		#
		#

		if llista_buida:
			return false


	def __str__(self):
		#
		#
		#

		print "Solucionando el backtracking: "
		solution_backtracking=self.resolve_backtracking(self.lva,self.lvna,self.R,self.D)
		if solution_backtracking is not None:

			print "Solucion backtracking: " + "\n"
			auxiliar=99
			for index,word in zip(self.lvna,self.lva):
   				if index != auxiliar:
   					print index + " : " + auxiliar + "\n"
   				else:
   					print "(Vertical)" + index + " : " + auxiliar + "\n"

   				auxiliar = index
   			lva=[]
   			print "Solucionando el backtracking con forward checking: " + "\n"
		solution_backtracking_w_forward=self.resolve_backtracking_w_forward(self.lva,self.lvna,self.R,self.D)
			if solution_backtracking_w_forward is not None:
				
			for index,word in zip(self.lvna,self.lva):
   				if index != auxiliar:
   					print index + " : " + auxiliar + "\n"
   				else:
   					print "(Vertical)" + index + " : " + auxiliar + "\n"

   				auxiliar = index


	
	def resolve_backtracking_w_forward(self, lva, lvna, R, D):
		#
		#
		#

		# We cant assign more values
		if not self.lvna:
			return self.lva
		# Get variable to assign and its D
		var = [self.lvna[0],""]
		# Loop over the possibilities of the domain(that function returns a list)
		for asignableValue in self.domain(var):
			if self.satisfiesConstraints(asignableValue,var[0]):
				#if DA
				#if (DA=ActualitzarDominis(((Var valor), LVNA,R)<>fals) llavors
				res = self.backtracking(lva.append([var,asignableValue]),lvna[1:],R,D)
				if self.isCompleteSolution(res):
					return res
		return None 

	'''
	ActualitzarDominis((X v),L,R): Retorna la llista dels dominis per a les variables no assignades de L considerant les restriccions de R
	 despres dassignar X amb v, retorna fals si algun domini actualitzat es buit.

	def generateSeparatedList(self):
		#REVISADA
		#
		#Output:
		words_max_len=0

		#Buscamos la longitud maxima.
		for eachword in self.big_dictionary_list:
			if len(eachword)-1 > words_max_len:
				words_max_len=len(eachword)-1

		#Miramos cada una de las longitudes y las palabras que coinciden con esta.
		for act_words_len in range(words_max_len):
			act_list[:]=[]
			for word in self.big_dictionary:
				if(len(word)-1==act_words_len):
					act_list.append(self.big_dictionary.index(word))
			self.sep_words_dict.append(act_list)


	'''
	
