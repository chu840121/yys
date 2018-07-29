from sklearn.feature_extraction.text import CountVectorizer  
import numpy as np
import matplotlib.pyplot as plt
import os, sys
import os.path
from sklearn.feature_extraction.text import TfidfTransformer 
import re
from simhash import Simhash
from PIL import Image
from time import time
bening_code_okay_to = ("C:\\Users\\islab718A\\Desktop\\malware\\hhj")
store_benefit_jpg = ("C:\\Users\\islab718A\\Desktop\\malware\\test_image")
corpus = []
############################################################################## get r, g, b, x, y
def hash_djb2_generate_r_g_b(string):                                                                                                                                
    hash = 5381
    for x in string:
        hash = (( hash << 5) + hash) + ord(x)
    return (hash & 0xFF0000)>>16, (hash & 0x00FF00)>>8, hash & 0x0000FF

def simhash(s): ############################################################## get x, y
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]

def after_SimHash(n):
	a = [int(digit) for digit in bin(n)[2:]]
	k = []
	while len(a)<=69:
		a.insert(0, 0)
	for i in range(0, len(a), 7):
		k.append(a[i]^a[i+1]^a[i+2]^a[i+3]^a[i+4]^a[i+5]^a[i+6])
	out1 = 0
	out2 = 0
	o = 0
	k1 = []
	k2 = []
	for bit in k:
		if o <= 4:
			k1.append(bit)
		else:
			k2.append(bit)
		o = o + 1
	for bitt in k1: 
		out1 = (out1 << 1) | bitt
	for bittt in k2: 
		out2 = (out2 << 1) | bittt
	return out1, out2
	
def get_x_y(string):
	return after_SimHash(Simhash(simhash(string)).value)

############################################################################## tf-idf part(get sequence of word)
for foldername in os.listdir(bening_code_okay_to): 
	with open(bening_code_okay_to+"\\"+foldername, 'r') as myfile:
			data=myfile.read().replace('\n', '')
	corpus.append(data)#if have to 
print "preparing.."
vectorizer = CountVectorizer()  
X = vectorizer.fit_transform(corpus)  
word = vectorizer.get_feature_names()  ## unicode list 
print "total word is : "+str(len(word))
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(X)  

a = []
to_sim_list = []
for k in range(len(corpus)): #tfidf.toarray()[0]tfidf.toarray()[k]len(corpus)
	print "now handling : "+str(k)
	if os.path.exists(store_benefit_jpg+"\\"+str(k+250)+".jpg"):
		continue
	else:
		aa = time()
		for t in range(0, 9600, 120):
			if t < 120:
				a = np.array(word)[tfidf.toarray()[k].argsort()[-(t+120):][::-1]].tolist()
				to_sim_list.append(' '.join(a))
				del a[:]
			else:
				#a.append(word[tfidf.toarray()[0].argsort()[-(t+20):-t][::-1][i]])
				a = np.array(word)[tfidf.toarray()[k].argsort()[-(t+120):-t][::-1]].tolist()
				to_sim_list.append(' '.join(a))
				del a[:]
	##############################################################################generate jpg
		img = Image.new( 'RGB', (32,32), "black")
		pixels = img.load()
		for i in range(len(to_sim_list)):
			to_sim_list[i]
			r, g, b = hash_djb2_generate_r_g_b(to_sim_list[i])
			x, y = get_x_y(to_sim_list[i])
			for j in range(-2, 3):
				for yt in range(-2, 3):
					rq = x+yt
					h = y+j
					if rq < 0 or h < 0 or rq > 31 or h > 31:
						continue
					else:
						if pixels[rq ,h][0] == 0 and pixels[rq ,h][1] == 0 and pixels[rq ,h][2] == 0:
							pixels[rq ,h] = (r, g, b)
						else:
							continue
		img.save(store_benefit_jpg+"\\"+str(k+250)+".jpg")
	##############################################################################
		del to_sim_list[:]
		bb = time()
		print "handle time : "+str(bb - aa)