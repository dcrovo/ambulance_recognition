#!/bin/bash
raspi-gpio set 26 op #Configura el GPIO 26 como salida
file_path="/home/camera/ambulance_recognition/app/ctl/amb_flag"

while true
do	
	flag=$(cat ${file_path})
	if [ $flag -eq 1 ];
	then
		raspi-gpio set 26 dh 	#Pone el GPIO 26 en alto
	else  
		raspi-gpio set 26 dl  	#Pone el GPIO 26 en bajo 
	fi
done

