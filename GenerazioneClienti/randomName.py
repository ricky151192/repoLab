import random
import string 
import re
import csv
import datetime

def stampaCSV(table_input, headers):
		length = len(headers)
		with open(final_file+'.csv', 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=headers)
			writer.writeheader()
			for i in xrange(len(table_input)):
				for j in xrange(length):
					if j == 0:
						obj = {str(headers[j]) : str(table_input[i][j])}
						#print(obj)
					else:
						obj.update({str(headers[j]) : str(table_input[i][j])})
						#print(obj)
						#print('error else')
				writer.writerow(obj)


def generazioneNumLet(type_input, type_letter):
	if type_input == 'let':
		if type_letter == 0:
			var = str(random.choice(string.ascii_letters)).upper()
			regex = re.search('[A-E]', var, flags = 0)
			while(not(regex)):
				var = str(random.choice(string.ascii_letters)).upper()
				regex = re.search('[A-E]', var, flags = 0)
		else:
			var = str(random.choice(string.ascii_letters)).upper()

	else:
		var = str(random.randrange(0,9)).upper()

	return var

def generazioneTarga():
	letter1 = generazioneNumLet('let',0)
	letter2 = generazioneNumLet('let',1)
	letter_part_1 = letter1+letter2


	letter1 = generazioneNumLet('let',1)
	letter2 = generazioneNumLet('let',1)
	letter_part_2 = letter1+letter2
	

	num1 = generazioneNumLet('num',0)
	num2 = generazioneNumLet('num',0)
	num3 = generazioneNumLet('num',0)
	numbers = num1+num2+num3
	
	targa = letter_part_1+numbers+letter_part_2
	print(targa)
	return targa

def generazioneData():
	num1 = generazioneNumLet('num',0)
	num2 = generazioneNumLet('num',0)
	return data


def rimuoviApici(string_input):
			tmp = ''
			for i in xrange(len(string_input)):
				if i > 0 and i < len(string_input)-1:
					tmp = tmp+string_input[i]
			return tmp

def capitalLetter(string_input):
	tmp = ''
	for i in xrange(len(string_input)):
		if i == 0:
			tmp = string_input[0].upper()
		else:
			tmp = tmp + string_input[i]
	return tmp

def getDates():

	num_data_immatricolazione = random.randrange(1000,10000)
	data_immatricolazione = date_list[num_data_immatricolazione].strftime("%Y/%m/%d")
	num_data_acquisto = random.randrange(10,num_data_immatricolazione+1)
	data_acquisto = date_list[num_data_acquisto].strftime("%Y/%m/%d")
	num_data_assicurazione = random.randrange(10, num_data_acquisto+1)
	data_assicurazione = date_list[num_data_assicurazione].strftime("%Y/%m/%d")

	print(data_immatricolazione)
	print(data_acquisto)
	print(data_assicurazione)

	return data_immatricolazione, data_acquisto, data_assicurazione

def generazioneCodiceRischio():
	codice_rischio = random.randrange(1,4)
	return codice_rischio




random.seed(42) # un numero a caso, serve per fissare la generazione



nomi = map(lambda x: x.strip(), list(open("nomi_italiani.txt","r")))
cognomi = map(lambda x: x.strip(), list(open("cognomi.txt","r")))
car = map(lambda x: x.strip(), list(open("auto_def.txt","r")))
numdays = 20000
base = datetime.datetime.today()
date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]
# print(date_list)

tabella_clienti = list([])
dictionary_targa = dict([])
id_cliente = 1
for i in xrange(800): ##Numero clienti con un veicoli
	immatricolazione, acquisto, assicurazione = getDates()
	num_nome = random.randrange(1,8913)
	num_cognome = random.randrange(1,150)
	num_car = random.randrange(1,205)
	age = random.randrange(18,90)
	targa = generazioneTarga()
	rischio = generazioneCodiceRischio()
	while (dictionary_targa.get(targa) != None):
		targa = generazioneTarga()
	car_list = car[num_car].split(",", 50)
	new_line = [id_cliente, targa, capitalLetter(nomi[num_nome]), cognomi[num_cognome], age, capitalLetter(rimuoviApici(car_list[2])), rimuoviApici(car_list[15]), car_list[21], car_list[25], immatricolazione, acquisto, assicurazione, rischio]
	tabella_clienti.append(new_line)
	id_cliente +=1

for i in xrange(150): ##Numero clienti con due veicoli
	num_nome = random.randrange(1,8913)
	num_cognome = random.randrange(1,150)
	age = random.randrange(18,80)
	rischio = generazioneCodiceRischio()
	for j in xrange(2): ## Numero auto del cliente
		immatricolazione, acquisto, assicurazione = getDates()
		num_car = random.randrange(1,205)
		targa = generazioneTarga()
		while (dictionary_targa.get(targa) != None):
			targa = generazioneTarga()
		car_list = car[num_car].split(",", 50)
		new_line = [id_cliente, targa, capitalLetter(nomi[num_nome]), cognomi[num_cognome],age, capitalLetter(rimuoviApici(car_list[2])), rimuoviApici(car_list[15]), car_list[21], car_list[25], immatricolazione, acquisto, assicurazione, rischio]
		tabella_clienti.append(new_line)
	id_cliente +=1

for i in xrange(50): ##Numero clienti con tre veicoli
	num_nome = random.randrange(1,8913)
	num_cognome = random.randrange(1,150)
	age = random.randrange(18,85)
	rischio = generazioneCodiceRischio()
	for j in xrange(3): ## Numero auto del cliente
		immatricolazione, acquisto, assicurazione = getDates()
		num_car = random.randrange(1,205)
		targa = generazioneTarga()
		while (dictionary_targa.get(targa) != None):
			targa = generazioneTarga()
		car_list = car[num_car].split(",", 50)

		new_line = [id_cliente, targa, capitalLetter(nomi[num_nome]), cognomi[num_cognome], age, capitalLetter(rimuoviApici(car_list[2])), rimuoviApici(car_list[15]), car_list[21], car_list[25], immatricolazione, acquisto, assicurazione, rischio]
		tabella_clienti.append(new_line)
		print(new_line)
	id_cliente +=1

headers = ['Id_Cliente', 'Targa', 'Nome', 'Cognome', 'Age', 'Marca', 'NumCilindri', 'Cv','Prezzo','Data_Immatricolazione', 'Data_Acquisto', 'Data_Assicurazione','Codice_Rischio']
final_file = 'tabella_clienti'
stampaCSV(tabella_clienti, headers)



