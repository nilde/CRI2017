import numpy as np
import timeit
import random as rd

class Backtracking:
	def __init__(self,R,file_dict,orient_word_list,longitudes,n):
		#Constructor de la clase Backtracking inicializa las estructuras auxiliares necesarias

		self.n=n
		self.dictionary=open(file_dict, 'r')
		self.R=R
		self.D=[]
		self.lva={}
		self.lvna=orient_word_list
		#Hay que generar
		self.words_list=[]
		self.variable_aux_domains={}
		self.num_words=len(orient_word_list)
		self.longitudes=longitudes
		self.orient_word_list=orient_word_list
		self.big_dictionary_list=[]
		self.generateCorrectDict()
		self.dictionary.close()
		self.all_crosses={}
		self.generateDomains()
		self.generateCrucesDict()


	def generateCorrectDict(self):
		#Genera el diccionario de las palabras eliminando los caracteres inecesarios(en MAC nose si en otra plataforma dara error)
		for word in self.dictionary:
			self.big_dictionary_list.append(word.translate(None, '\n\r'))
		self.big_dictionary_list=self.big_dictionary_list[0:self.n+1]


	def generateDomains(self):
		#Genera los indices de las palabras del diccionario para cada palabra, es decir, se le asocia un dominio
		for i in range(len(self.longitudes)):
			self.D.append([-1])
		for index,each_word in enumerate(self.big_dictionary_list):
			for indice,longitud in enumerate(self.longitudes):
				if longitud == len(each_word):
					self.D[indice].append(index)
		for index,i in enumerate(self.D):
			self.D[index]=i[1:][:]
		aux_clave={}
		#conversion a diccionario
		for indice,domain in enumerate(self.D):
			aux_clave[self.orient_word_list[indice]]=domain[:]
		self.D=dict(aux_clave)

	def generateCrucesDict(self):
		#Genera las posiciones de cruce entre todas las palabras con la estrcutura adecuada [['1H','1V',0,2]...]
		for i in self.D.keys():
			self.all_crosses[i]=[]
		for word in self.orient_word_list:
			aux=[]
			for indice,each_cross in enumerate(self.R):
				if word in each_cross:
					aux.append(each_cross)
				self.all_crosses[word]=aux[:]

	def satisfiesConstraints(self,asignacion,palabra,lva):
		# En este punto no puede hay palabras de longitud inadecuada, retorna verdadero o falso indicando si se cumplen las restricciones
		all_crosses_word=self.all_crosses[palabra]
		for cross in all_crosses_word:
			if cross[0]==palabra:
				palabra_p=cross[2]
				palabra_a_comparar=cross[1]
				palabra_a_comparar_p=cross[3]
			else:
				palabra_p=cross[3]
				palabra_a_comparar=cross[0]
				palabra_a_comparar_p=cross[2]
			if palabra_a_comparar in lva.keys():
				if lva[palabra_a_comparar][palabra_a_comparar_p] != asignacion[palabra_p]:
					return False
		return True

	def isCompleteSolution(self,solution):
		# Mira si tenemos una solucion
		if len(solution)!=self.num_words:
			return False
		return True

	def domain(self,var,D):
		#Retorna el dominio asignado a una determinada variable
		return D[var]

    	
	def updateDomains(self,asignableValue,DA):
		#Si queda algun dominio sin alguna variable no hay solucion
		for key in DA:
			copia_lista=[]
			if asignableValue in DA[key]:
				if not asignableValue in self.variable_aux_domains:
					self.variable_aux_domains[asignableValue]=[]
				self.variable_aux_domains[asignableValue].append(key)
				if len(DA[key])==1:
					self.variable_aux_domains.popitem()
					return False
				else:
					DA[key] = [x for x in DA[key] if x != asignableValue]
		return True

	def __str__(self):
		#Muestra los resultados obtenidos por los diferentes backtrackings

		R=self.R[:]
		lva=dict(self.lva)
		lvna=self.lvna[:]
		start_time = timeit.default_timer()
		solution_backtracking_TD=self.resolveBacktrackingTD(lva,lvna,self.R,self.D)
		elapsed = timeit.default_timer() - start_time
		
		if solution_backtracking_TD is not None:
			print 'Solucion backtracking con los dominios juntos (peor caso): ' + '\n'
			print solution_backtracking_TD
		else:
			print 'No existe solucion para este crucigrama \n'
		print 'Tiempo transcurrido ' + str(elapsed)



		lva={}
		n_lvna=self.lvna[:]
		DA=dict(self.D)
		start_time = timeit.default_timer()
		solution_backtracking_w_forward=self.resolveBacktrackingFC(lva,n_lvna,self.R,DA)
		elapsed = timeit.default_timer() - start_time

		if solution_backtracking_w_forward is not None:
			print 'Solucion backtracking con forward checking: ' + '\n'
			print solution_backtracking_w_forward
		else:
			print 'No existe solucion para este crucigrama \n'
		print 'Tiempo transcurrido ' + str(elapsed)

		
		
		'''
		lva={}
		n_lvna=self.lvna[:]
		self.variable_aux_domains={}
		start_time = timeit.default_timer()
		solution_backtracking_w_forward_mrv=self.resolveBacktrackingFC_MRV(lva,n_lvna,self.R,dict(self.D))
		elapsed = timeit.default_timer() - start_time
		if solution_backtracking_w_forward_mvc is not None:
			print 'Solucion backtracking con forward checking y mvc: ' + '\n'
			print solution_backtracking_w_forward_mrv
		else:
			print 'No existe solucion para este crucigrama \n'
		print 'Tiempo transcurrido ' + str(elapsed)
		
		'''
		return ''



	def rescueDomains(self,DA,asignableValue):
		#Recupera los valores de los dominios de la iteracion previa ( FC )
		rescue=self.variable_aux_domains.keys()[0]
		for i in self.variable_aux_domains[rescue]:
			DA[i].append(asignableValue)
		del self.variable_aux_domains[rescue]


	def satisfiesConstraintsTD(self,word,var,lva):
		#Funcion intermedia para comprovar la longitud de las palabras del dominio (Backtracking normal), llama a satisfiesConstraints de mas arriba
		if len(word)!=self.longitudes[self.orient_word_list.index(var)]:
			return False
		else:
			return self.satisfiesConstraints(word,var,lva)

	def list_except1(self,lvna,var):
		#Elimina un valor de una lista se usa para el mvc (eliminar un valor en concreto)
		return [x for x in lvna if x != var]

	def sortbydomain(self,DA,lvna):
		#Funcion que selecciona la variable con el dominio mas pequeno de las que aun no se han asignado
		order=[x[0] for x in sorted(DA.items(), key = lambda item : len(item[1]))]
		return [i for i in order if i in lvna] [0]


	def rescueDomains_mvc(self,DA,asignableValue):
		#Recupera los valores de los dominios de la iteracion previa ( FC )
		if self.variable_aux_domains.keys():
			rescue=max(self.variable_aux_domains.keys())
			for i in self.variable_aux_domains[rescue]:
				DA[i].append(asignableValue)
			del self.variable_aux_domains[rescue]




##################################################
##### RESOLUTION OF DIFF BACKTRACKING CONFIGS ####
##################################################



	def resolveBacktrackingTD(self, lva, lvna,R,D):
		#Funcion que va a resolver el backtracking con los dominios juntos
		# Si ya hemos asignado todas las variables retornamos
		if not lvna:
			return lva
		# Cogemos la primera variable no asignada
		var = lvna[0]
		# Miramos todos los diferentes valores que puede tomar el dominio
		for word in self.big_dictionary_list:
			if self.satisfiesConstraintsTD(word,var,lva):
				lva[var]=word
				res = self.resolveBacktrackingTD(lva,lvna[1:],R,D)
				if self.isCompleteSolution(res):
					return res
		return ''
	'''
	def resolveBacktrackingSD(self, lva, lvna,R,D):
		#Funcion que va a resolver el backtracking con los dominios separados
		# Si ya hemos asignado todas las variables retornamos
		if not lvna:
			return lva
		var = lvna[0]
		## Miramos todos los diferentes valores que puede tomar el dominio
		for asignableValue in self.domain(var,D):
			if self.satisfiesConstraints(self.big_dictionary_list[asignableValue],var,lva):
				lva[var]=self.big_dictionary_list[asignableValue]
				res = self.resolveBacktrackingSD(lva,lvna[1:],R,D)
				if self.isCompleteSolution(res):
					return res
		return ''
		'''

	def resolveBacktrackingFC(self, lva, lvna, R, DA):
		#Resuelve el algoritmo de backtracking con forward checking
		if not lvna:
			return lva
		var = lvna[0]
		# Miramos todos los diferentes valores que puede tomar el dominio
		for asignableValue in self.domain(var,DA):
			if self.satisfiesConstraints(self.big_dictionary_list[asignableValue],var,lva):
				if self.updateDomains(asignableValue,DA):
					lva[var]=self.big_dictionary_list[asignableValue]
					res = self.resolveBacktrackingFC(lva,lvna[1:],R,DA)		
					if self.isCompleteSolution(res):
						return res
					self.rescueDomains(DA,asignableValue)			
		return ''

	def resolveBacktrackingFC_MRV(self, lva, lvna, R, DA):
		#Resuelve el algoritmo de backtracking con forward checking
		# Si ya hemos asignado todas las variables retornamos
		if not lvna:
			return lva
		# Cogemos la primera variable no asignada
		var = self.sortbydomain(DA,lvna)
		# Miramos todos los diferentes valores que puede tomar el dominio
		for asignableValue in self.domain(var,DA):
			if self.satisfiesConstraints(self.big_dictionary_list[asignableValue],var,lva): #satisface constantes
				if self.updateDomains(asignableValue,DA): #actualizamos dominios
					lva[var]=self.big_dictionary_list[asignableValue]
					n_lvna=self.list_except1(lvna,var)
					res = self.resolveBacktrackingFC_MRV(lva,n_lvna,R,DA)
					#Condicion evaluada para saber si hemos acabado el backtracking
					if self.isCompleteSolution(res):
						return res
					self.rescueDomains_mvc(DA,asignableValue)
					
		return ''

	
