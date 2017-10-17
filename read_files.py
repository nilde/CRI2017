'''
Esta clase genera todas las lecturas de los ficheros y genera las estructuras que necesitaremos para hacer el backtracking.
'''
class StructureCreator:
	def __init__(self,file_crossword):
		#REVISADA / FUNCIONA

		#Leemos el crucigrama de fichero
		self.crossword=open(file_crossword, 'r')
		

		#Variables que usaremos
		self.squares=[]
		self.sep_words_dict=[]
		self.occupied_positions=[]
		self.pos_init_words=[]
		self.orient_words_list=[]
		self.longitudes=[]
		self.cross=[]
		self.index_cross=[]
		self.maxima_longitud=0
		self.palabras_juntas=[]
		self.domain_pointers=[]

		#Lee el fichero y guarda cada uno de los valores en una variable squares(casillas) que equivale al tablero
		for row in self.crossword:
			self.squares.append(row.split())
		
		#Cerramos ficheros
		self.crossword.close()
		

	def OcuppiedPositionsGenerator(self):
		#IMPORTANTE:Llamar antes a la funcion que genere las orientaciones(wordOrientation) y a la funcion que detecta los diferentes tamanos de las palabras (lookWidths)
		#Estructura que usa (1)->self.orient_words_list=['1H','1V',...] 
		#Output(1)->genera una estructura self.occupied_positions=[[0,3,0,4,0,5],[...]]] self.occupied_positions[0] contiene todas las posiciones de la palabra 1
		#Output(2)->genera una estructura de self.cross=[[palabra_1,palabra_2,pos_x,pos_y],[palabra_1,palabra_2,pos_x,pos_y],...] self.cross[0] contiene [palabra_1,palabra_2,pos_x,pos_y]

		occupied_for_word=[]
		#Para cada palabra generamos las casillas que ocupa para poder encontrar a posteriori los diferentes cruces entre las palabras
		for indice,palabra in enumerate(self.orient_words_list):
			if len(palabra) == 2:
				letra = palabra[1]
				numero= int(palabra[0])
			else:
				letra=palabra[2]
				numero=int(palabra[0])*10+int(palabra[1])

			occupied_for_word[:]=[]
			associated_squares=self.longitudes[indice]
			initial_pos = list(self.pos_init_words[numero-1])

			#Segundo caracter contiene la orientacion ej. (1H) si es horizontal incrementamos los contadores en el eje de las Y.
			if letra =='H':
				for offset in range(associated_squares):
					occupied_for_word.append([initial_pos[0],initial_pos[1]+offset])
			#Sino incrementamos el contador en el eje de las X.
			else:
				for offset in range(associated_squares):
					occupied_for_word.append([initial_pos[0]+offset,initial_pos[1]])
			#Anadimos las posiciones que ocupa cada palabra a la lista que contiene todas las ocupaciones
			self.occupied_positions.append(occupied_for_word[:])
			
		
		each_cross=[]
		#Las posiciones de la matriz representan una palabra
		for indice_1,diff_pos_word in enumerate(self.occupied_positions):
			for indice_2,word in enumerate(self.occupied_positions):
				each_cross[:]=[]
				for i in diff_pos_word:
					if i in word and indice_1 != indice_2:
						each_cross.extend(([self.orient_words_list[indice_1],self.orient_words_list[indice_2],i[0],i[1]]))
						self.cross.append(each_cross[:])
						each_cross[:]=[]

				
		#eliminar las permutaciones
		for comb_1 in self.cross:
			p1=comb_1[0]
			p2=comb_1[1]
			for indice_2,comb_2 in enumerate(self.cross):
				if comb_2[0] == p2 and comb_2[1] == p1:
					self.cross.pop(self.cross.index(comb_2))

	def generate_index_cross(self):
		#Genera los indices de cruce para simplificar el calculo posterior del backtracking
		#Formato de each_cross [palabra_1,palabra_2,pos_x,pos_y]
		#Output: [[palabra_1,palabra_2,index_pal_1,index_pal_2],[palabra_1,palabra_3,indice_pal_1,indice_pal_2]]
		auxiliar=[]
		for each_cross in self.cross:
			#Auxiliar es la estructura final de los cruces
			auxiliar[:]=[]
			auxiliar.extend((each_cross[0],each_cross[1]))#Ponemos las palabras igual
			if len(each_cross[0]) == 2:
				letra_1 = each_cross[0][1]
				numero_1 = int(each_cross[0][0])
			else:
				letra_1 =each_cross[2]
				numero_1 =int(each_cross[0][0])*10+int(each_cross[0][1])

			if len(each_cross[1]) == 2:
				letra_2 = each_cross[1][1]
				numero_2= int(each_cross[1][0])
			else:
				letra_2=each_cross[1][2]
				numero_2=int(each_cross[1][0])*10+int(each_cross[1][1])

			#Recuperamos la posicion que ocupan respecto a los vectores y extraemos la posiciones ocupadas por esa palabra
			indice_lista_ocupadas_1=self.orient_words_list.index(each_cross[0])
			indice_lista_ocupadas_2=self.orient_words_list.index(each_cross[1])

			pos_ocupadas_1=self.occupied_positions[indice_lista_ocupadas_1]
			pos_ocupadas_2=self.occupied_positions[indice_lista_ocupadas_2]

			#Por ultimo alargamos la longitud de la lista auxiliar con las indices de las posiciones que ocupan 
			auxiliar.extend((pos_ocupadas_1.index(each_cross[2:]),pos_ocupadas_2.index(each_cross[2:])))#Buscamos a que indice de la palabra corresponde
			
			#Anadimos la estructura intermedia a la final
			self.index_cross.append(auxiliar[:])



	def initialPosWords(self):
		# Miramos la cuadricula y buscamos numeros mayores que 0.
		#Output:self.pos_init_words[]
		for num_row,row in enumerate(self.squares):
			for num_col,element in enumerate(row):
				if(element > '0') and (element !='#'):
					self.pos_init_words.append([int(num_row),int(num_col)])

		



	def wordOrientation(self):
		#En teoria estan por orden asi que no es necesario usar metodos como el insert ya que se revisan las cordenadas por orden.
		#Output: self.orients_words_list es una lista que contiene una lista para cada uno de las aplabras indicando la orientacion en forma de una lista de chars H, V
		
		for index,position in enumerate(self.pos_init_words):
			index+=1
			#Tratamiento primera fila
			if position[0] == 0:
				#Ultima pos primera fila
				if position[1] == len(self.squares[0]) - 1:
					self.orient_words_list.append(str(index)+'V')


				#Dos corchetes o primera casilla genera 2 orientaciones si en la casilla [1][0] no hay una almohadilla
				elif self.squares[0][position[1]-1] == '#' or (position[1] == 0 and self.squares[1][0] != '#'):
					self.orient_words_list.append(str(index)+'H')
					self.orient_words_list.append(str(index)+'V')

				#Caso generico para la primera fila
				else:
					self.orient_words_list.append(str(index)+'V')


			#Tratamiento ultima fila
			elif position[0] == len(self.squares) - 1:
					self.orient_words_list.append(str(index)+'H')


			#Tratamiento primera columna
			elif position[1]==0:
				#Si arriba tiene una almohadilla genera 2 orientaciones
				if self.squares[position[0]-1][0]=='#':
					self.orient_words_list.append(str(index)+'H')
					self.orient_words_list.append(str(index)+'V')

				#Caso generico genera una palabra horizontal
				else:
					self.orient_words_list.append(str(index)+'H')
			

			#Tratamiento ultima columna
			elif position[1]==len(self.squares[0]):
				self.orient_words_list.append(str(index)+'V')



			#Tratamiento resto de la malla
			else:
				#Dos corchetes generan dos orientaciones diferentes
				if self.squares[position[0]][position[1]-1]=='#' and self.squares[position[0]-1][position[1]]=='#':
					self.orient_words_list.append(str(index)+'H')
					self.orient_words_list.append(str(index)+'V')
				
				#Si tenemos un corchete arriba genera una vertical
				elif self.squares[position[0]-1][position[1]]=='#':
					self.orient_words_list.append(str(index)+'V')

				#Si tenemos un corchete a la izquierda genera una horizontal
				elif self.squares[position[0]][position[1]-1]=='#':
					self.orient_words_list.append(str(index)+'H')

				#Si tenemos un valor a la izquierda igual o superior a la izquierda genera una palabra horizontal
				elif self.squares[position[0]][position[1]-1] >= 0:
					self.orient_words_list.append(str(index)+'V')

				#Caso generico es horizontal
				else:
					self.orient_words_list.append(str(index)+'H')

	def lookWidths(self):
		#Comprobamos las longitudes de las palabras horizontales
		#Output:lista de longitudes self.longitudes[3,4,5,...] que corresponden 1 a 1 con las posiciones de self.orient_word_list=[1H,1V,...] 
	
		len_max=0
		height=len(self.squares)
		width=len(self.squares[0])
		#Para cada palabra que tenemos
		aux=self.pos_init_words[:]
		for palabra in self.orient_words_list:
			if len(palabra) == 2:
				letra = palabra[1]
				numero= int(palabra[0])
			else:
				letra=palabra[2]
				numero=int(palabra[0])*10+int(palabra[1])
			
			coord=aux[numero-1][:]
			counter=0
			#Orientacion horizontal
			if letra == 'H':
				len_max=width-coord[1]
				
				#Mientras no encontremos un corchete y la medida sea valida contamos lo que ocupa la palabra
				while (counter < len_max and self.squares[coord[0]][coord[1]]!='#'):
					coord[1]+=1
					counter+=1
				self.longitudes.append(counter)

			#Orientacion vertical
			else:
				len_max=height-coord[0]
				#Mientras no encontremos un corchete y la medida sea valida contamos lo que ocupa la palabra
				while (counter < len_max and self.squares[coord[0]][coord[1]]!= '#'):
					coord[0]+=1
					counter+=1
				self.longitudes.append(counter)
			if counter > self.maxima_longitud:
					self.maxima_longitud=counter


	def generatePairs(self):
		#Genera relaciones de palabras que comparten la misma longitud[[],[],[3,4]] donde la pos indica la longitud 
		##Ouput:
		print self.longitudes
		self.domain_pointers=self.longitudes[:]
		for longitud in range(self.maxima_longitud+1):
			self.palabras_juntas.append([self.orient_words_list[i] for i, x in enumerate(self.longitudes) if x == longitud])

		#Hasta aqui va perf
		#repasar los pointers
		for indice_palabras,palabras in enumerate(self.palabras_juntas):
			for each in palabras:
				self.domain_pointers[self.orient_words_list.index(each)]=indice_palabras



	def __str__(self):
		#Funcion que sirve para comprobar el correcto funcionamiento del sistema generador de estructuras.
		#Output: Muestra por pantalla todas las estructuras importantes genradas
		print "---------ESTRUCTURAS GENERADAS PARA RESOLVER EL BACKTRACKING----------"
		print "======================================================================"
		print "Casillas: " + str(self.squares)
		print "======================================================================"
		print "Posiciones ocupadas por las palabras: " + str(self.occupied_positions)
		print "======================================================================"
		print "Posiciones iniciales ocupadas: " + str(self.pos_init_words)
		print "======================================================================"
		print "Longitudes de las palabras: " + str(self.longitudes)
		print "======================================================================"
		print "Orientacion de las palabras: " + str(self.orient_words_list)
		print "======================================================================"
		print "Cruces: "  + str(self.cross)
		print "======================================================================"
		print "Indices de cruces: " + str(self.index_cross)
		print "======================================================================"
		print "Palabra de maxima longitud: " + str(self.maxima_longitud)
		print "======================================================================"
		print "Lista de palabras que comparten longitudes: " + str(self.palabras_juntas)
		print "======================================================================"
		print "Lista de punteros a la estructura de las palabras compartidas: " + str(self.domain_pointers)
		print "======================================================================"
		print "======================================================================"
		return ''


























