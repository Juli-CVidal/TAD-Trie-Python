import myLinkedList as mll

class Trie:
	root = None

class TrieNode:
	parent = None #almacena al padre
	children = None #almacena una linkedlist, sus nodos son trienodes
	key = None #almacena un caracter
	isEndOfWord = False #indica si es el último caracter de una palabra ingresada


"""Insert"""
def insert(Trie, element):
	if (Trie.root == None):
		Trie.root = TrieNode()
	else:
		if (search(Trie, element) == True): #palabra ya ingresada
			return None

	return insertWord(Trie.root, element, 0)

def insertWord(currentNode, wordToInsert, index):
	if (currentNode.children == None):
		currentNode.children = mll.linkedList()

	childListNode = getListNode(currentNode.children, wordToInsert[index])
	if (childListNode != None):
		if (index != len(wordToInsert) - 1):
			return insertWord(childListNode, wordToInsert, index + 1)
		else:
			childListNode.isEndOfWord = True
		
	newTrieNode = TrieNode()
	newTrieNode.key = wordToInsert[index]
	newTrieNode.parent = currentNode
	mll.add(currentNode.children, newTrieNode)
	if (index != len(wordToInsert) - 1):
		return insertWord(currentNode.children.head.value, wordToInsert, index + 1)
	else:
		newTrieNode.isEndOfWord = True


"""Search"""
def search(Trie, element):
	currentNode = Trie.root.children.head
	result = getLastNode(currentNode, element, 0)
	if (result == None):
		return False

	return result.isEndOfWord


"""Delete"""
def delete(Trie, element):
	if (Trie.root == None or Trie.root.children == None):
		return False
	return deleteWord(Trie, Trie.root, element, 0)

def deleteWord(Trie, currentNode, wordToDelete, index):
	currentNode = getLastNode(Trie.root.children.head, wordToDelete, 0)
	if (currentNode == None):
		return False

	if (currentNode.children != None):
		currentNode.isEndOfWord = False
		return True

	mll.delete(currentNode.parent.children, currentNode)
	currentNode = currentNode.parent
	while (not currentNode.isEndOfWord and currentNode.parent != None):
		currentList = currentNode.parent.children
		mll.delete(currentList, currentNode)
		if (mll.length(currentList) == 1):
			return True
		currentNode = currentNode.parent
	return True



"""Obtener palabras que comiencen con un prefijo"""
def getWordsWithPrefix(Trie, prefix, size):
	prefixSize = len(prefix)
	wordList = mll.linkedList()
	currentNode = getLastNode(Trie.root.children.head, prefix, 0)
	if (currentNode == None):
		return None
		
	getSuffixes(currentNode, wordList, "", size - prefixSize, 0)
	if (mll.length(wordList) == 0):
		return wordList
	
	suffixNode = wordList.head
	while (suffixNode != None):
		suffixNode.value = prefix + suffixNode.value
		suffixNode = suffixNode.nextNode
	
	return wordList

	
def getSuffixes(currentNode, wordList, wordFinded, length, index):
	childListNode = currentNode.children.head
	while (childListNode != None):
		wordFinded += childListNode.value.key
			
		if (len(wordFinded) ==  length and childListNode.value.isEndOfWord):
			#print(f"{wordFinded=}, {index=}")
			mll.insert(wordList, wordFinded, index)
			wordFinded = ""
			index += 1
	
		if (childListNode.value.children != None):
			getSuffixes(childListNode.value, wordList, wordFinded, length, index)
	
		wordFinded = wordFinded[1:]
		childListNode = childListNode.nextNode


"""Comparar dos árboles"""
def compareTries(Trie1, Trie2):
	wordsInTrie1 = mll.linkedList()
	getAllWords(Trie1.root, wordsInTrie1, "")
	wordsInTrie2 = mll.linkedList()
	getAllWords(Trie2.root, wordsInTrie2, "")
	
	if (mll.length(wordsInTrie1) != mll.length(wordsInTrie2)):
		return False

	currTrie1 = wordsInTrie1.head
	currTrie2 = wordsInTrie2.head
	while (currTrie1 != None):
		if (currTrie1.value != currTrie2.value):
			return False
		currTrie1 = currTrie1.nextNode
		currTrie2 = currTrie2.nextNode

	return True


"""Verificar si contiene una cadena invertida"""
def checkIfInverted(Trie):
	wordsInTrie = mll.linkedList()
	getAllWords(Trie.root, wordsInTrie, "")

	currentNode = wordsInTrie.head

	while (currentNode != None):
		nextNode = currentNode.nextNode
		while (nextNode != None):
			if (currentNode.value == nextNode.value[::-1]):
				return True
			nextNode = nextNode.nextNode
		currentNode = currentNode.nextNode
	return False


"""Autocompletar"""
def autoComplete(Trie, prefix):
	currentNode = getLastNode(Trie.root.children.head, prefix, 0)
	if (currentNode == None):
		return "ninguna"
	nextChars = ""
	while (mll.length(currentNode.children) == 1):
		if (currentNode.isEndOfWord):
			return nextChars
		nextChars += currentNode.children.head.value.key
		currentNode = currentNode.children.head.value
	return "ninguna"
	
"""PrintTrie"""
def printTrie(currentNode, space):
	if (currentNode.isEndOfWord):
		print(f"{space} <{currentNode.key}>")
	else:
		print(f"{space} {currentNode.key}")

	space += " "
	if (currentNode.children != None):
		childList = currentNode.children
		childListNode = childList.head
		size = mll.length(childList)
		for index in range(size):

			printTrie(childListNode.value, space)
			childListNode = childListNode.nextNode
			

"""Funciones Auxiliares"""
def getLastNode(currentNode, wordToSearch, index):
	if (currentNode == None):
		return None

	if (currentNode.value.key == wordToSearch[index]):
		if (index == len(wordToSearch) - 1):
			return currentNode.value
		if (currentNode.value.children != None):
			return getLastNode(currentNode.value.children.head, wordToSearch, index + 1)
			
	return getLastNode(currentNode.nextNode, wordToSearch, index)
	

def getListNode(LL, key):
	currentNode = LL.head
	while (currentNode != None):
		if (currentNode.value.key == key):
			return currentNode.value
		currentNode = currentNode.nextNode
		
	return None


def getAllWords( currentNode, wordList, wordFinded):
	childListNode = currentNode.children.head
	hasPrefix = False
	while (childListNode != None):
		if (hasPrefix and currentNode.key != None):
			wordFinded = ""
			searchCurrent = currentNode
			while (searchCurrent.key != None):
				wordFinded += searchCurrent.key
				searchCurrent = searchCurrent.parent
			wordFinded = wordFinded[::-1] 
			#el while superior recorre hacia el inicio de la palabra, por eso debo invertirla
		wordFinded += childListNode.value.key
			
		if (childListNode.value.isEndOfWord):
			mll.add(wordList, wordFinded)

		if (childListNode.value.children != None):
			getAllWords(childListNode.value, wordList, wordFinded)

		childListNode = childListNode.nextNode
		wordFinded = wordFinded[1:] 
		#elimino el primer caracter debido a que es el de otro hijo de la root
		hasPrefix = True