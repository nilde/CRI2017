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
	reader.generateSeparatedList()
	print reader
	solver=backtracking.Backtracking(reader.cross,reader.sep_words_dict,reader.big_dictionary_list,reader.orientword,"diccionari_CB.txt")#Revisar intensamente esto
	print solver

if __name__ == "__main__":
    main()
