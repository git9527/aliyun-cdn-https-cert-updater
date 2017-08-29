#!/usr/bin/python
#coding:utf-8 

import sys,os,inspect,subprocess,urlparse,time
import requests
import argparse

def get_script_dir(follow_symlinks=True):
	if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
		path = os.path.abspath(sys.executable)
	else:
		path = inspect.getabsfile(get_script_dir)
	if follow_symlinks:
		path = os.path.realpath(path)
	return os.path.dirname(path)

def get_file_content_in_line(fileContainer):
	result = fileContainer.readlines()
	return ''.join(result)
	
def fire_update_request(args):
	certName = args.certName
	if not certName:
		domain = urlparse.urlparse("http://" + args.domainName)
		subdomain = ".".join(domain.hostname.split('.')[:-2])
		timestamp = time.strftime("%Y%m%d", time.gmtime())
		certName = subdomain + "_" + timestamp
	scriptPath = os.path.join(get_script_dir(), "cdn-api", "cdn.py")

	if not args.privateKeyFile:
		url = subprocess.check_output(['python', scriptPath, "Action=SetDomainServerCertificate", "ServerCertificateStatus=on", "DomainName=" + args.domainName, "CertName=" + certName, "-i" + args.accessKeyId, "-s" + args.accessKeySecret]).rstrip()
	else:
		privateKey = get_file_content_in_line(args.privateKeyFile)
		certificate = get_file_content_in_line(args.certificateFile)
		url = subprocess.check_output(['python', scriptPath, "Action=SetDomainServerCertificate", "ServerCertificateStatus=on", "DomainName=" + args.domainName, "CertName=" + certName, "PrivateKey=" + privateKey, "ServerCertificate=" + certificate, "-i" + args.accessKeyId, "-s" + args.accessKeySecret]).rstrip()

	resp = requests.get(url)
	print resp.text

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Short sample app')
	parser.add_argument("-i", dest="accessKeyId", help="Specify access key id")
	parser.add_argument("-s", dest="accessKeySecret", help="Specify access key secret")
	parser.add_argument("-d", dest="domainName", help="Specify CDN domain name")
	parser.add_argument("-n", dest="certName", help="Specify certificate name")
	parser.add_argument("-p", dest="privateKeyFile", help="Specify certificate private key file location", type=argparse.FileType('r'))
	parser.add_argument("-c", dest="certificateFile", help="Specify certificate content file location", type=argparse.FileType('r'))

	args = parser.parse_args()
	
	if not args.accessKeyId:
		parser.error("Access key id required")
	if not args.accessKeySecret:
		parser.error("Access key secret required")
	if not args.domainName:
		parser.error("CDN domain name required")

	
	fire_update_request(args)
				
	



	