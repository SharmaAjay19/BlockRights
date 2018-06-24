from gensim import corpora, models, similarities
import nltk
import string
from nltk.corpus import stopwords
from collections import defaultdict
from gensim.test.utils import datapath
stoplist = set(stopwords.words('english'))

def prepareDictionary(alldocuments):
	texts = [[word for word in nltk.word_tokenize(document.lower()) if (word not in stoplist) and (word not in string.punctuation)] for document in alldocuments]
	frequency = defaultdict(int)
	for text in texts:
		for token in text:
			frequency[token] += 1
	texts = [[token for token in text if frequency[token] > 0] for text in texts]
	dictionary = corpora.Dictionary(texts)
	#dictionary.save('Dictionary.dict')
	return dictionary

def getMostSimilarWork(model, index, dictionary, testDoc):
	sims = index[model[dictionary.doc2bow(nltk.word_tokenize(testDoc))]]
	mos = sorted(list(enumerate(sims)), key=lambda x: x[1], reverse=True)
	print(mos)
	mos = mos[0]
	if mos[1]==0:
		return (-1, 0)
	else:
		return mos

def processCorpus(alldocuments, testdocument):
	dictionary = prepareDictionary(alldocuments+[testdocument])
	corpus = [dictionary.doc2bow(nltk.word_tokenize(document.lower())) for document in alldocuments]
	corpora.MmCorpus.serialize('Corpus.mm', corpus)
	model = models.ldamodel.LdaModel(corpus)
	#model = models.LsiModel(corpus, id2word=dictionary)
	index = similarities.docsim.MatrixSimilarity(model[corpus])
	return (model, index, dictionary)

def getPlagiarism(alldocuments, testDocument):
	model, index, dictionary = processCorpus(alldocuments, testDocument)
	sim = getMostSimilarWork(model, index, dictionary, testDocument.lower())
	if (sim[1]>0.9):
		return sim[0]
	else:
		return -1

'''alldocs = [
"A suspension bridge is a type of bridge in which the deck (the load-bearing portion) is hung below suspension cables on vertical suspenders. The first modern examples of this type of bridge were built in the early 1800s.[3][4] Simple suspension bridges, which lack vertical suspenders, have a long history in many mountainous parts of the world. This type of bridge has cables suspended between towers, plus vertical suspender cables that carry the weight of the deck below, upon which traffic crosses. This arrangement allows the deck to be level or to arc upward for additional clearance. Like other suspension bridge types, this type often is constructed without falsework. The suspension cables must be anchored at each end of the bridge, since any load applied to the bridge is transformed into a tension in these main cables. The main cables continue beyond the pillars to deck-level supports, and further continue to connections with anchors in the ground. The roadway is supported by vertical suspender cables or rods, called hangers. In some circumstances, the towers may sit on a bluff or canyon edge where the road may proceed directly to the main span, otherwise the bridge will usually have two smaller spans, running between either pair of pillars and the highway, which may be supported by suspender cables or may use a truss bridge to make this connection. In the latter case there will be very little arc in the outboard main cables.",
"A simple suspension bridge (also rope bridge, swing bridge (in New Zealand), suspended bridge, hanging bridge and catenary bridge) is a primitive type of bridge that is supported entirely from anchors at either end and has no towers or piers. However, it may have saddles. In such bridges, the deck of the bridge follows the downward and upward arc of the load-bearing cables, with additional light ropes at a higher level used to form a handrail. Alternatively, stout handrail cables supported on short piers at each end may be the primary load-bearing element, with the deck suspended below. Suspended well from two high locations over a river or canyon, simple suspension bridges follow a shallow downward catenary arc and are not suited for modern roads and railroads. Owing to practical limitation in the grade (i.e. the deck being an arc, not flat) and the response to dynamic loads of the bridge deck, this type is quite restricted in its load-carrying capacity relative to its span. This type of bridge is considered the most efficient and sustainable design in developing countries, however, especially for river crossings that lie in non-floodplain topography such as gorges.",
"Wire rope is several strands of metal wire twisted into a helix forming a composite "rope", in a pattern known as "laid rope". Larger diameter wire rope consists of multiple strands of such laid rope in a pattern known as "cable laid". In stricter senses the term "wire rope" refers to diameter larger than 3/8 inch (9.52 mm), with smaller gauges designated cable or cords.[1] Initially wrought iron wires were used, but today steel is the main material used for wire ropes. Historically, wire rope evolved from wrought iron chains, which had a record of mechanical failure. While flaws in chain links or solid steel bars can lead to catastrophic failure, flaws in the wires making up a steel cable are less critical as the other wires easily take up the load. While friction between the individual wires and strands causes wear over the life of the rope, it also helps to compensate for minor failures in the short run. Wire ropes were developed starting with mining hoist applications in the 1830s. Wire ropes are used dynamically for lifting and hoisting in cranes and elevators, and for transmission of mechanical power. Wire rope is also used to transmit force in mechanisms, such as a Bowden cable or the control surfaces of an airplane connected to levers and pedals in the cockpit. Only aircraft cables have WSC (wire strand core). Also, aircraft cables are available in smaller diameters than wire rope. For example, aircraft cables are available in 3/64 in. diameter while most wire ropes begin at a 1/4 in. diameter.[2] Static wire ropes are used to support structures such as suspension bridges or as guy wires to support towers. An aerial tramway relies on wire rope to support and move cargo overhead.",
"A bridge is a structure built to span physical obstacles without closing the way underneath such as a body of water, valley, or road, for the purpose of providing passage over the obstacle. There are many different designs that each serve a particular purpose and apply to different situations. Designs of bridges vary depending on the function of the bridge, the nature of the terrain where the bridge is constructed and anchored, the material used to make it, and the funds available to build it."
]
getPlagiarism(alldocs, "A bridge is a very big structure that is mostly built to span physical obstacles without shutting the way below it such as vallye, a body of water, or road, for the purpose of providing a way over the obstacle.")'''