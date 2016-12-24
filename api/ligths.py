#!/usr/bin/python
#-*- coding:Utf-8 -*-
import sys#,getopt
#import re
from phue import Bridge
import json
import ast

b = Bridge(sys.argv[2])
lang=sys.argv[1]
TOSAY=""

lbl={
		'fr':{
			'on':'allumé',
			'off':'éteinte',
			'lamp':'lumière',
			'unknow':'inconnue',
			'error':'erreur',
			'command':'commande',
		},
		'en':{
			'on':'on',
			'off':'off',
			'lamp':'lamp',
			'unknow':'unknow',
			'error':'error',
			'command':'command',
		}
	}

def toggle_light(light=1):
	global TOSAY
	try:
		if (b.get_light(light,'on')):
			b.set_light(light,'on',False)
		else:
			b.set_light(light,'on',True)
		status(light)
	except: 
		TOSAY= lbl[lang]['lamp']+" "+lbl[lang]['unknow']
		return TOSAY
		
def status(light=1):
	global TOSAY
	try:
		status = b.get_light(light,'on')
		if (status):
			statusS=lbl[lang]['on']
		else:
			statusS=lbl[lang]['off']
				
		TOSAY = lbl[lang]['lamp']+' '+light+' '+statusS
		
	except:
		TOSAY = lbl[lang]['lamp']+' '+lbl[lang]['unknow']	
	return TOSAY
			
def brightness(light, arg):
	bri = arg[0]
	bri = int(bri)/100*254
	b.set_light(light,'bri',bri)
	
def router(arg):
	return {
		'toggle': toggle_light,
		'status': status,
		'brightness':brightness
	}

def main():
	global TOSAY
	routes = router(sys.argv)
	try:
		#Recherche dans le dico si le mot n'a pas ete mal traduit par le stt
		sys.argv[3]=ast.literal_eval(sys.argv[3])
		sys.argv[5] =sys.argv[3].get(sys.argv[5], sys.argv[5])
		light=str(sys.argv[5]).capitalize()
		if len(sys.argv) > 6:
			routes[sys.argv[4]](light,sys.argv[6:])
		else:
			routes[sys.argv[4]](light)
	except  Exception as e:
		print str(e)
		TOSAY = lbl[lang]['command']+" "+lbl[lang]['unknow']
		
	print TOSAY

if __name__ == "__main__":
	main()
	