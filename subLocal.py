#!/usr/bin/env python
# -*-coding:Utf-8- -*

#Very simple multi-processing wordlist based sub domain brute force using socket python library, can also be done using dnslib
#Main usage : Lan Network / CTF / HackTheBox
#Requirements : validators (pip3 install validators)
#Multi-processing using concurrent.futures and ProcessPoolExecutor to avoid GIL restrictions

#Credits : Lutzenfried


import sys
import argparse
import validators
import socket
import concurrent.futures

#Default subdomain list
subdomainList = ["www","mail","dev","sub","backup","development","mob","mobile","legacy","leg","email","ftp","sftp","test","labo","lab","info","site","premium","one","identity","manager","lead","manage","rest","api","req","content","client","clients","back","imap","m","smtp","pop","blog","webmail","courriel","wiki","support","service","help","kb","go","mysql","admin","administrator","feeds","static","sites","group","groups","store","vpn","myvpn","mysite","orga","organization","organisation","files","file","resource","resources","ressource","ressources","secure","secures","transfert","media","medias","mysql","mssql","beta","photo","photos","ssl","tls","live","search","pic","status","list","lists","ns1","ns2","ww1","portal","portail","bbs","mail2","ww42","mail1","cloud","owa","gw","mx","forum","cdn","exchange","gov","gouv","vps","ns","live","app","apps","videos","news","mx0","mx1","mailserver","video","localhost","autoconfig","config","configuration","autodiscover","web","disk","webdisk","remote","server","system","network"]

exitFlag = 0

#ANSI color for Linux
Green = '\033[92m'  # green
Yellow = '\033[93m'  # yellow
Bblue = '\033[94m'  # blue
Red = '\033[91m'  # red
White = '\033[0m'   # white

#Picasso style function
def asciiNoob():
    print("""
           _     _                 _ 
 ___ _   _| |__ | | ___   ___ __ _| |
/ __| | | | '_ \| |/ _ \ / __/ _` | |
\__ \ |_| | |_) | | (_) | (_| (_| | |
|___/\__,_|_.__/|_|\___/ \___\__,_|_|\n""")
    print ("Multi-processing subdomain brute force enumeration tool\n")
   
#User arguments function
def get_Args():
	asciiNoob()
	parser = argparse.ArgumentParser(description='Multi-process Sudomain enumeration tool based on wordlist : subLocal.py -d domain.local -w wordlist.txt -t -o results_sub_bruteforce.txt')
	parser.add_argument('-d','--domain', help='Domain to bruteforce', required=True)
	parser.add_argument('-w','--wordlist', help='Subdomain wordlist', type=argparse.FileType('r', encoding='UTF-8'), default=subdomainList, required=False)
	parser.add_argument('-t','--thread',metavar='Number of threads to use for subLocal bruteforce', help='Concurrent thread', type=int, default=15, choices=range(0,200), required=False)
	parser.add_argument('-o','--outfile', type=argparse.FileType('w'), required=True)
	args = parser.parse_args()
	return args
	
#Domain validation function      
def domain_Validity(domain):
	if validators.domain(args.domain) == True:
		try:
			validators.ip_address.ipv4(socket.gethostbyname(args.domain))
			print (" ==> The following domain name %s resolving to %s will be Brute Force +++\n" % (args.domain,socket.gethostbyname(args.domain)))
			return True
		except socket.error:
			print ("Please verify your connexion / DNS resolution / Access to the provided domain ==> ", args.domain)
			False
		return True
	else:
		print (Red+" --- Bad domain name : Please verify your domain name\n")
        	
#Writting results function
def writeToFile(subrequest):
	fh = open(args.outfile.name, "a")
	fh.write(subrequest + "\n")
	fh.close()

#Main brute force function	
def bruteForce(sub):
	subrequest = (sub.rstrip('\r\n') + "." + args.domain)
	try:
		socket.gethostbyname(subrequest)
		print(Green+" ++++++ Successfully discover subdomain : " + subrequest + White)
		writeToFile(subrequest)
	except socket.error:
		print(Red + " --- Cannot  resolve : " +  sub +"."+ args.domain + White)
	
if __name__ == "__main__":
	args = get_Args()

	try:
		if domain_Validity(args.domain) == True:
			print(" ==> Launching Brute Force request using following arguments :\n")
			print("     - Domain : %s" % args.domain)
			if args.wordlist == 1:
				print("     - Wordlist : %s" % args.wordlist.name)
			print("     - Thread : %s" % args.thread)
			print("     - OutFile : %s\n" % args.outfile.name)
			with concurrent.futures.ProcessPoolExecutor(args.thread) as executor:
				executor.map(bruteForce, args.wordlist)
		else:
			pass
	except:
		pass

