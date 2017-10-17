import numpy as np
import timeit

class Backtracking:
	def __init__(self,R,file_dict,orient_word_list,longitudes):
		#REVISADA / FUNCIONA 
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
		# REVISADA / FUNCIONA
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
		for indice,domain in enumerate(self.D):
			aux_clave[self.orient_word_list[indice]]=domain
		self.D=dict(aux_clave)

	def generate_cruces_dict(self):
		#Genera las posiciones de cruce entre todas las palabras
		
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
		# En teoria en este punto no puede haber palabras de longitud diferente a la adecuada
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
		# Mira si la longitud de la lista de soluciones es correcta(T / F)
		if len(solution)!=self.num_words:
			return False
		return True

	def domain(self,var,D):
		#BACKTRACKING Y BACKTRACKING CON FC
		return D[var]
	
	def chooseNewVar(self,D,lvna):
		#ESTO SIRVE PARA EL MVC
		i_min_length = 0 
		i_min_distance = 999999
		for indice,domain in enumerate(D):
			if ((len(D[domain]) != 0) and (len(D[domain]) < i_min_distance) and (domain in lvna)):
				i_min_length=domain
				i_min_distance=len(D[domain])
		return i_min_length
	

	

	def updateDomains(self,asignableValue,DA):
		# REVISADA / FUNCIONA
		#Si queda algun dominio sin alguna variable no puede estar bien
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
		#REVISADA / FUNCIONA 
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
		start_time = timeit.default_timer()
		solution_backtracking_w_forward_mvc=self.resolveBacktrackingFC_MVC(lva,lvna,self.R,DA)
		elapsed = timeit.default_timer() - start_time
		if solution_backtracking_w_forward_mvc is not None:
			print 'Solucion backtracking con forward checking y mvc: ' + '\n'
			print solution_backtracking_w_forward_mvc
		else:
			print 'No existe solucion para este crucigrama \n'
		print 'Tiempo transcurrido ' + str(elapsed)
		
		return ''


	def rescueDomains(self,DA,l_to_act):
		#REVISADA / FUNCIONA
		#recupera los valores de los dominios 
		for diff_domain in l_to_act[1:]:
			DA[diff_domain].append(l_to_act[0])

	def satisfiesConstraintsTD(self,word,var,lva):
		if len(word)!=self.longitudes[self.orient_word_list.index(var)]:
			return False
		else:
			return self.satisfiesConstraints(word,var,lva)

	def list_except1(self,lvna,var):
		print '----------------'
		print var
		print lvna
		print [x for x in lvna if x != var]
		print '----------------'
		return [x for x in lvna if x != var]


	#DIFERENTES BACKTRACKINGS
	

	def resolveBacktrackingTD(self, lva, lvna,R,D):
		#Funcion que va a resolver el backtracking con los dominios juntos
		#
		#Output:

		# We cant assign more values
		if not lvna:
			return lva
		# Get variable to assign and its D
		var = lvna[0]
		# Loop over the possibilities of the domain(that function returns a list)
		for word in self.big_dictionary_list:
			if self.satisfiesConstraintsTD(word,var,lva):
				lva[var]=word
				res = self.resolveBacktrackingTD(lva,lvna[1:],R,D)
				if self.isCompleteSolution(res):
					return res
		return ''

	def resolveBacktrackingSD(self, lva, lvna,R,D):
		#Funcion que va a resolver el backtracking con los dominios separados
		#Output:

		# We cant assign more values
		if not lvna:
			return lva
		# Get variable to assign and its D
		var = lvna[0]
		# Loop over the possibilities of the domain(that function returns a list)
		for asignableValue in self.domain(var,D):
			if self.satisfiesConstraints(self.big_dictionary_list[asignableValue],var,lva):
				lva[var]=self.big_dictionary_list[asignableValue]
				res = self.resolveBacktrackingSD(lva,lvna[1:],R,D)
				if self.isCompleteSolution(res):
					return res
		return ''

	def resolveBacktrackingFC(self, lva, lvna, R, DA):
		#print lvna
		# REVISADA / FUNCIONA
		#Resuelve el algoritmo de backtracking
		# We cant assign more values
		if not lvna:
			return lva
		# Get variable to assign and its D
		var = lvna[0]
		# Miramos todos los diferentes valores que puede tomar el dominio
		for asignableValue in self.domain(var,DA):
			if self.satisfiesConstraints(self.big_dictionary_list[asignableValue],var,lva): #satisface constantes
				if self.updateDomains(asignableValue,DA): #actualizamos dominios
					lva[var]=self.big_dictionary_list[asignableValue]
					res = self.resolveBacktrackingFC(lva,lvna[1:],R,DA)
					#Condicion evaluada para acabar el backtracking
					if self.isCompleteSolution(res):
						return res
					self.rescueDomains(DA,self.variable_aux_domains[-1])
					
		return ''

	def resolveBacktrackingFC_MVC(self, lva, lvna, R, DA):
		#print lvna
		# REVISADA / FUNCIONA
		#Resuelve el algoritmo de backtracking
		# We cant assign more values
		if not lvna:
			return lva
		# Get variable to assign and its D
		var = self.chooseNewVar(DA,lvna)
		# Miramos todos los diferentes valores que puede tomar el dominio
		for asignableValue in self.domain(var,DA):
			if self.satisfiesConstraints(self.big_dictionary_list[asignableValue],var,lva): #satisface constantes
				if self.updateDomains(asignableValue,DA): #actualizamos dominios
					lva[var]=self.big_dictionary_list[asignableValue]
					new_lvna=self.list_except1(lvna,var)
					res = self.resolveBacktrackingFC_MVC(lva,new_lvna,R,DA)
					#Condicion evaluada para acabar el backtracking
					if self.isCompleteSolution(res):
						return res
					self.rescueDomains(DA,self.variable_aux_domains[-1])
					
		return ''

	
