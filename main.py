import backtracking
import read_files
import numpy
def main():
	#Generacion de estructuras auxiliares
	reader=read_files.StructureCreator("crossword_CB.txt")
	reader.initialPosWords()
	reader.wordOrientation()
	reader.lookWidths()
	reader.OcuppiedPositionsGenerator()
	reader.generate_index_cross()
	reader.generatePairs()
	print reader
	#self,R,lvna,file_dict,longitudes
	solver=backtracking.Backtracking(reader.index_cross,reader.orient_words_list,"diccionari_CB.txt",reader.longitudes,reader.domain_pointers,reader.palabras_juntas)#Revisar intensamente esto
	#print solver

if __name__ == "__main__":
    main()
