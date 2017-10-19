import backtracking
import read_files
def main():
	#Generacion de estructuras auxiliares
	reader=read_files.StructureCreator("crossword_A.txt")
	reader.initialPosWords()
	reader.wordOrientation()
	reader.lookWidths()
	reader.OcuppiedPositionsGenerator()
	reader.generateIndexCross()
	reader.generatePairs()
	
	#Descomentar para ver las estrcuturas que se generan
	#print reader
	solver=backtracking.Backtracking(reader.index_cross,"diccionari_A.txt",reader.orient_words_list,reader.longitudes,3000)
	print solver

if __name__ == "__main__":
    main()
