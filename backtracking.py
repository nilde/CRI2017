
#objetos a guardar
'''
self.dictionary=[]
self.D=[ [ [ pal1,pal2,pal3] , [ipal11,ipal12,...] ],[...],... ]
self.restdict=[[4,[poscom1]]
self.lva=[]
self.lvna=list(range(11, 17))
words_list=[[pos1,pos2,...,pos,],[...]]

'''
class Backtracking:
	def __init__(self,R,words_list,lvna,file_dict,longitudes,words_list):
		
		self.dictionary=open(file_dict, 'r')
		self.R=R
		self.D={}
		self.lva=[]
		self.lvna=lvna
		self.words_list=words_list
		self.longitudes=longitudes

		self.big_dictionary_list=[]
		for word in self.dictionary:
			self.big_dictionary_list.append(word)
		self.dictionary.close()
		self.equivalents={}
		generateEquivalents()
		generateDomains()


	def generateDomains(self):
		for key, value in self.equivalents.iteritems():
			self.D[tuple(value)]=[]
		for word in self.big_dictionary_list:
			for key, value in self.equivalents.iteritems():
				if len(word) in key:
					self.D[key].append(word)
					break



	def domain(self,var):
		#REESCRIBIR
		#Buscar las palabras correspondientes a los indices en el diccionario
		for unique_domain in self.D: #Elemento con [[indices],[dominio]]
			if var in unique_domain[0]:#si esta en unique_domain[0]=indices
				return unique_domain[1]#retorna el dominio asociado

	def satisfiesConstraints(self,asignableValue,index):
		#REEScribir
		# En teoria en este punto no puede haber palabras de longitud diferente a la adecuada
		for word in self.avl:
			if word[1]==asignableValue:
				return False
		for indice,crosses in enumerate(self.R[index-1][index:]):
			if crosses: #se cruza con alguna otra palabra
				if self.lva[index-1] and self.lva[indice-1]:
					letter1=asignableValue[self.words_list[index-1].index(crosses)]
					letter2=self.lva[indice-1][1][self.words_list[indice-1].index(crosses)]	
					if letter1 != letter2:
						return False

		return True



	def isCompleteSolution(self,solution):
		#REESCRIBIR, SE PUEDE USAR UN CONTADOR DE DIMENSIONES TOTALES
		
		if len(solution)==self.num_words:
			return True
		return False

	def resolve_backtracking(self, lva, lvna):
		# We cant assign more values
		if not self.lvna:
			return self.lva
		# Get variable to assign and its D
		var = [self.lvna[0],""]
		# Loop over the possibilities of the domain(that function returns a list)
		for asignableValue in self.domain(var):
			if self.satisfiesConstraints(asignableValue,var[0]):
				res = self.backtracking(lva.append([var,asignableValue]),lvna[1:],self.R,self.D)
				if self._isCompleteSolution(res):
					return res
		return None

	def updateDomains(self):

		if llista_buida:
			return false


	def __str__(self):
		print "Solucionando el backtracking: "
		solution_backtracking=self.resolve_backtracking(self.lva,self.lvna,self.R,self.D)
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

		for index,word in zip(self.lvna,self.lva):
   			if index != auxiliar:
   				print index + " : " + auxiliar + "\n"
   			else:
   				print "(Vertical)" + index + " : " + auxiliar + "\n"

   			auxiliar = index


	
	def resolve_backtracking_w_forward(self, lva, lvna, R, D):
		# We cant assign more values
		if not self.lvna:
			return self.lva
		# Get variable to assign and its D
		var = [self.lvna[0],""]
		# Loop over the possibilities of the domain(that function returns a list)
		for asignableValue in self.domain(var):
			if self.satisfiesConstraints(asignableValue,var[0]):
				if DA
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
	
