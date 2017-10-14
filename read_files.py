'''
Esta clase genera todas las lecturas de los ficheros y genera las estructuras que necesitaremos para hacer el backtracking.
'''
class StructureCreator:
	def __init__(self,file_crossword):
		#REVISADA

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
		#IMPORTANTE:Llamar antes a la funcion que genere las orientaciones(wordOrientation) y a la funcion que detecta los diferentes tamaños de las palabras (lookWidths)
		#Estructura que usa (1)->self.orient_words_list=['1H','1V',...] 
		#Output(1)->genera una estructura self.occupied_positions=[[0,3,0,4,0,5],[...]]] self.occupied_positions[0] contiene todas las posiciones de la palabra 1
		#Output(2)->genera una estructura de self.cross=[[palabra_1,palabra_2,pos_x,pos_y],[palabra_1,palabra_2,pos_x,pos_y],...] self.cross[0] contiene [palabra_1,palabra_2,pos_x,pos_y]

		occupied_for_word=[]
		#Para cada palabra generamos las casillas que ocupa para poder encontrar a posteriori los diferentes cruces entre las palabras
		for num_word,orientation in enumerate(self.orient_words_list):
			occupied_for_word[:]=[]
			associated_squares=self.longitudes[num_word]
			initial_pos=self.pos_init_words[self.orient_words_values[num_word]]

			#Segundo caracter contiene la orientacion ej. (1H) si es horizontal incrementamos los contadores en el eje de las Y.
			if orientation[1]=='H':
				for offset in range(associated_squares):
					occupied_for_word.extend([initialpos[0],initial_pos[1]+offset])

			#Sino incrementamos el contador en el eje de las X.
			else:
				for offset in range(associated_squares):
					occupied_for_word.extend([initialpos[0]+offset,initial_pos[1]])
			
			#Anadimos las posiciones que ocupa cada palabra a la lista que contiene todas las ocupaciones
			self.occupied_positions.append([occupied_for_word])

	
		skip=0
		#Las posiciones de la matriz representan una palabra
		each_cross=[]
		for indice_1,diff_pos_word in enumerate(self.occupied_positions):
			each_cross[:]=[]
			skip+=1
			if index==len(occupied_positions)-1:
				break
			for word in self.occupied_positions[skip:]:
				st1=set(tuple(diff_pos_word))
				st2=set(tuple(word))
				cruce=st1.intersection(st2)
				if len(cruce) > 0:
					palabra_1=self.orient_words_list[indice_1]
					palabra_2=self.orient_words_list[self.occupied_positions.index(word)]
					each_cross.extend(palabra_1,palabra_2,cruce[0],cruce[1])
			#Anadimos en el caso de que se crucen en alguna posicion si la posicion 
				self.cross.append(each_cross)


	def generate_index_cross(self):
		#REVISADA
		#Genera los indices de cruce para simplificar el calculo posterior del backtracking
		#Formato de each_cross [palabra_1,palabra_2,pos_x,pos_y]
		#Output: [[palabra_1,palabra_2,index_pal_1,index_pal_2],[palabra_1,palabra_3,indice_pal_1,indice_pal_2]]
		auxiliar=[]
		for each_cross in self.cross:
			#Auxiliar es la estructura final de los cruces
			auxiliar[:]=[]
			auxiliar.extend((each_cross[0],each_cross[1]))#Ponemos las palabras igual

			#Recuperamos la posicion que ocupan respecto a los vectores y extraemos la posiciones ocupadas por esa palabra
			indice_lista_ocupadas_1=self.orient_words_list.index(each_cross[0])
			indice_lista_ocupadas_2=self.orient_words_list.index(each_cross[1])
			pos_ocupadas_1=self.occupied_positions[indice_lista_ocupadas_1]
			pos_ocupadas_2=self.occupied_positions[indice_lista_ocupadas_2]

			#Por ultimo alargamos la longitud de la lista auxiliar con las indices de las posiciones que ocupan 
			auxiliar.extend((posiciones_ocupadas_1.index([each_cross[3],each_cross[4]])),posiciones_ocupadas_2.index([each_cross[3],each_cross[4]]))#Buscamos a que indice de la palabra corresponde
			
			#Anadimos la estructura intermedia a la final
			self.index_cross.append(auxiliar)



	def initialPosWords(self):
		#REVISADA
		# Miramos la cuadricula y buscamos numeros mayores que 0.
		#Output:self.pos_init_words[]
		for num_row,row in enumerate(self.squares):
			for num_col,element in enumerate(row):
				if(element > '0') and (element !='#'):
					self.pos_init_words.append([int(num_row),int(num_col)])

		self.domain_pointers=[0]*len(self.pos_init_words)



	def wordOrientation(self):
		#REVISADA
		#En teoria estan por orden asi que no es necesario usar metodos como el insert ya que se revisan las cordenadas por orden.
		#Output: self.orients_words_list es una lista que contiene una lista para cada uno de las aplabras indicando la orientacion en forma de una lista de chars H, V
		
		for position in self.pos_init_words:

			#Tratamiento primera fila
			if position[0] == 0:
				#Ultima pos primera fila
				if position[1] == len(self.squares[0]) - 1:
					self.orient_words_list.append(str(index)+'V')

				#Dos corchetes o primera casilla genera 2 orientaciones si en la casilla [1][0] no hay una almohadilla
				elif self.squares[0][position[1]-1] == '#' or (position[0] == 0 and self.squares[1][0] != '#'):
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
		#REVISADA
		#Comprobamos las longitudes de las palabras horizontales
		#Output:lista de longitudes self.longitudes[3,4,5,...] que corresponden 1 a 1 con las posiciones de self.orient_word_list=[1H,1V,...] 
	
		len_max=0
		height=len(self.squares)
		width=len(self.squares[0])

		#Para cada palabra que tenemos
		for index,palabra in enumerate(self.orient_words_list):
			coord=self.pos_init_words[index].copy()
			counter=0

			#Orientacion horizontal
			if palabra[1] == 'H':
				len_max=width-coord[1]

				#Mientras no encontremos un corchete y la medida sea valida contamos lo que ocupa la palabra
				while (self.squares[coord[0]][coord[1]]!='#' and counter < len_max):
					coord[1]+=1
					counter+=1
				self.longitudes.append(counter)

			#Orientacion vertical
			else:
				len_max=height-coord[0]

				#Mientras no encontremos un corchete y la medida sea valida contamos lo que ocupa la palabra
				while (self.squares[coord[0]][coord[1]] !=' #' and counter < len_max):
					coord[0]+=1
					counter+=1
				self.longitudes.append(counter)
			if counter > self.maxima_longitud:
					maxima_longitud=counter


	def generatePairs(self):
		#
		#Genera relaciones de palabras que comparten la misma longitud[[],[],[3,4]] donde la pos indica la longitud 
		##Ouput:
		for longitud in range(self.maxima_longitud+1):
			self.palabras_juntas.append([self.orient_words_list[i] for i, x in enumerate(self.longitudes) if x == longitud])
		for indice_palabras,palabras in enumerate(palabras_juntas):
			if len(palabras) > 0:
				for indice_pointer,x in self.orient_words_list:
					if x in palabras:
						self.domain_pointers.insert(indice_pointer,indice_palabras)



	def __str__(self):
		#REVISADA
		#Funcion que sirve para comprobar el correcto funcionamiento del sistema generador de estructuras.
		#Output: Muestra por pantalla todas las estructuras importantes genradas
		print "Casillas: " + self.squares
		print "Palabras separadas (indices): " + self.sep_words_dict
		print "Posiciones ocupadas por las palabras: " + self.occupied_positions
		print "Posiciones iniciales ocupadas: " + self.pos_init_words
		print "Longitudes de las palabras: " + self.longitudes
		print "Orientacion de las palabras: " + self.orient_words_list
		print "Palabras: " + self.orient_words_values
		print "Cruces: "  + self.cross
		print "Indices de cruces: " + self.index_cross
		print "Palabra de maxima longitud: " + self.maxima_longitud
		print "Lista de palabras que comparten longitudes: " + self.palabras_juntas

























