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

def on(light=1):
	return toggle_light(light, True)

def off(light=1):
	return toggle_light(light, False)

def toggle_light(light=1,state=None):
	global TOSAY
	try:
		if state is None:
			state = not b.get_light(light,'on')

		b.set_light(light,'on',state)
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
		
	except  Exception as e:
		TOSAY = lbl[lang]['lamp']+' '+lbl[lang]['unknow']	
	return TOSAY
			
def brightness(light, arg):
	bri = arg[0]
	bri = int(float(bri)/100*254)
	b.set_light(light,'bri',bri)

def hue(light, arg):
	colors=ast.literal_eval(arg[0])
	color=arg[1]
	command =  {'on' : True, 'hue':colors[color]['hue'],'sat':colors[color]['sat']}
	b.set_light(light, command)
	
def router(arg):
	return {
		'on': on,
		'off': off,
		'toggle': toggle_light,
		'status': status,
		'brightness':brightness,
		'hue':hue
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
	
