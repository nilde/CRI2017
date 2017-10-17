import numpy as np
import timeit

class Backtracking:
	def __init__(self,R,file_dict,orient_word_list,longitudes):
		#Constructor de la clase Backtracking inicializa las estructuras auxiliares necesarias

		
		self.dictionary=open(file_dict, 'r')
		self.R=R
		self.D=[]
		self.lva={}
		self.lvna=orient_word_list
		#Hay que generar
		self.words_list=[]
		self.variable_aux_domains=[]
		self.num_words=len(orient_word_list)
		self.longitudes=longitudes
		self.orient_word_list=orient_word_list
		self.big_dictionary_list=[]
		self.generateCorrectDict()
		self.dictionary.close()
		self.all_crosses={}
		self.generateDomains()
		self.generate_cruces_dict()


	def generateCorrectDict(self):
		#Genera el diccionario de las palabras eliminando los caracteres inecesarios(en MAC nose si en otra plataforma dara error)
		for word in self.dictionary:
			self.big_dictionary_list.append(word.translate(None, '\n\r'))

	def generateDomains(self):
		# REVISADA / FUNCIONA
		#Genera los indices de las palabras del diccionario para cada una de las palabras
		for i in range(len(self.longitudes)):
			self.D.append([-1])
		for index,each_word in enumerate(self.big_dictionary_list):
			for indice,longitud in enumerate(self.longitudes):
				if longitud == len(each_word):
					self.D[indice].append(index)
		for index,i in enumerate(self.D):
			self.D[index]=i[1:]
		aux_clave={}
		#conversion a diccionario
		for indice,domain in enumerate(self.D):
			aux_clave[self.orient_word_list[indice]]=domain
		self.D=dict(aux_clave)

	def generate_cruces_dict(self):
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
		# REVISADA / FUNCIONA (version del backtracking implementada con los dominios ya separados previamente)
		# En este punto no puede haber palabras de longitud diferente a la adecuada
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
		# Mira si la longitud de la lista de soluciones es correcta( T / F)
		if len(solution)!=self.num_words:
			return False
		return True

	def domain(self,var,D):
		#BACKTRACKING Y BACKTRACKING CON FC
		return D[var]
    	
	def updateDomains(self,asignableValue,DA):
		#Si queda algun dominio sin alguna variable no hay solucion
		ya_insertado=0
		lista_auxiliar=[]
		copia_lista=[]
		for key in DA:
			copia_lista=[]
			if asignableValue in DA[key]:
				if ya_insertado==0:
					ya_insertado=1
					lista_auxiliar.append(asignableValue)
				lista_auxiliar.append(key)
				DA[key] = [x for x in DA[key] if x != asignableValue]
				if not DA[key]:
					return False
		self.variable_aux_domains.append(lista_auxiliar)
		return True

	def __str__(self):
		#Muestra los resultados obtenidos por el backtracking y el backtracking con forward checking

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

		lva=dict(self.lva)
		lvna=self.lvna[:]
		start_time = timeit.default_timer()
		solution_backtracking_SD=self.resolveBacktrackingSD(lva,lvna,self.R,self.D)
		elapsed = timeit.default_timer() - start_time
		
		if solution_backtracking_SD is not None:
			print 'Solucion backtracking con los dominios separados: ' + '\n'
			print solution_backtracking_SD
		else:
			print 'No existe solucion para este crucigrama \n'
		print 'Tiempo transcurrido ' + str(elapsed)
   	

   		lva=dict(self.lva)
		lvna=self.lvna[:]
		DA=dict(self.D)
		start_time = timeit.default_timer()
		solution_backtracking_w_forward=self.resolveBacktrackingFC(lva,lvna,self.R,DA)
		elapsed = timeit.default_timer() - start_time

		if solution_backtracking_w_forward is not None:
			print 'Solucion backtracking con forward checking: ' + '\n'
			print solution_backtracking_w_forward
		else:
			print 'No existe solucion para este crucigrama \n'
		print 'Tiempo transcurrido ' + str(elapsed)
		
		lva=dict(self.lva)
		lvna=self.lvna[:]
		DA=dict(self.D)
		self.variable_aux_domains[:]=[]
		lvna_sorted=self.sortbydomain()
		print lvna_sorted
		start_time = timeit.default_timer()
		solution_backtracking_w_forward_mvc=self.resolveBacktrackingFC(lva,lvna_sorted,self.R,DA)
		elapsed = timeit.default_timer() - start_time

		if solution_backtracking_w_forward_mvc is not None:
			print 'Solucion backtracking con forward checking y mvc: ' + '\n'
			print solution_backtracking_w_forward_mvc
		else:
			print 'No existe solucion para este crucigrama \n'
		print 'Tiempo transcurrido ' + str(elapsed)
		
		return ''


	def rescueDomains(self,DA,l_to_act):
		#Recupera los valores de los dominios de la iteracion previa ( FC )
		for diff_domain in l_to_act[1:]:
			DA[diff_domain].append(l_to_act[0])

	def satisfiesConstraintsTD(self,word,var,lva):
		#Funcion intermedia para comprovar la longitud de las palabras del dominio (Backtracking normal), llama a satisfiesConstraints de mas arriba
		if len(word)!=self.longitudes[self.orient_word_list.index(var)]:
			return False
		else:
			return self.satisfiesConstraints(word,var,lva)

	def list_except1(self,lvna,var):
		#Elimina un valor de una lista se usa para el mvc (eliminar un valor en concreto)
		return [x for x in lvna if x != var]

	def sortbydomain(self):
		#Funcion que selecciona la variable con el dominio mas pequeno de las que aun no se han asignado
		return [x[0] for x in sorted(self.D.items(), key = lambda item : len(item[1]))]



	#DIFERENTES BACKTRACKINGS
	

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

	def resolveBacktrackingSD(self, lva, lvna,R,D):
		#Funcion que va a resolver el backtracking con los dominios separados

		# Si ya hemos asignado todas las variables retornamos
		if not lvna:
			return lva
		#Seleccionamos la primera variable no asignada
		var = lvna[0]
		## Miramos todos los diferentes valores que puede tomar el dominio
		for asignableValue in self.domain(var,D):
			if self.satisfiesConstraints(self.big_dictionary_list[asignableValue],var,lva):
				lva[var]=self.big_dictionary_list[asignableValue]
				res = self.resolveBacktrackingSD(lva,lvna[1:],R,D)
				if self.isCompleteSolution(res):
					return res
		return ''

	def resolveBacktrackingFC(self, lva, lvna, R, DA):
		#Resuelve el algoritmo de backtracking con forward checking
		# Si ya hemos asignado todas las variables retornamos
		if not lvna:
			return lva
		# Cogemos la primera variable no asignada
		var = lvna[0]
		# Miramos todos los diferentes valores que puede tomar el dominio
		for asignableValue in self.domain(var,DA):
			if self.satisfiesConstraints(self.big_dictionary_list[asignableValue],var,lva): #satisface constantes
				if self.updateDomains(asignableValue,DA): #actualizamos dominios
					lva[var]=self.big_dictionary_list[asignableValue]
					res = self.resolveBacktrackingFC(lva,lvna[1:],R,DA)
					#Condicion evaluada para saber si hemos acabado el backtracking
					if self.isCompleteSolution(res):
						return res
					self.rescueDomains(DA,self.variable_aux_domains[-1])
					
		return ''


	
