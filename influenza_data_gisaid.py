
##########################################################################
##FLUJO DE TRABAJO PARA MANEJAR DATOS DE INFLUENZA DESCARGADOS DE GISAID##
##########################################################################



#!/bin/bash
#1. Compilar la metadata de GISAID en python, saldra una metadata modificada y una lista de codigos
python3 influenza_data.py .

#2. Extraer los codigos que tienen metadata y remover duplicados
seqtk subseq gisaid_epiflu_sequence.fasta codigos.txt > filtrado.fasta
seqkit rmdup filtrado.fasta > secuencias_gisaid.fasta
rm filtrado.fasta codigos.txt

#3. Correr nextclade para NA, cambiar la base de datos
nextclade run --input-dataset /home/veronica/Programas/database_nextclade/H1N1_NA_MW626056 --output-csv nextclade.csv secuencias_gisaid.fasta

#4. Concatenar los datos de metadata.csv y nextclade.csv (solo para NA)

#5. Remover archivos
rm gisaid_epiflu_isolates.csv gisaid_epiflu_sequence.fasta nextclade.csv metadata.csv

#6. Los archivos finales son: metadata_gisaid.csv y secuencias_gisaid.fasta


----------------------------------------------------------------------------------------------------------

#PASO 1: Compilar la metadata de GISAID en python, saldra una metadata modificada y una lista de codigos
#input: gisaid_epiflu_isolates.csv
#output: metadata.csv y codigos.txt
	

########################################
####### FLUJO DE TRABAJO PARA HA #######
########################################


#Importando las librerias
import pandas as pd

#Pasos iniciales
data = pd.read_csv("gisaid_epiflu_isolates.csv")
#data.columns #Para verificar los nombres de las columnas
data_ha = data[data["HA_Segment_Id"].notna()] #Los None se representan como NaN
data2 = data_ha[["Isolate_Id","Location","Collection_Date"]]

#Trabajando con el dataframe
data2['country'] = data2['Location'].apply(lambda x: x.split(' / ')[1] if len(x.split(' / ')) > 1 else None)
data2.drop("Location", axis=1, inplace=True)
data2 = data2.rename(columns={'Isolate_Id': 'strain', 'Collection_Date': 'date'})
data2['year'] = data2['date'].apply(lambda x: x.split('-')[0])
data2["dataset"] = "GISAID"
data2.to_csv("metadata.csv", sep=",", index=False)

#Creando la lista de codigos
codigos = data2[["strain"]]
codigos.to_csv("codigos.txt", sep=",", index=False, header=False)
quit()




########################################
####### FLUJO DE TRABAJO PARA NA #######
########################################


#Importando las librerias
import pandas as pd

#Pasos iniciales
data = pd.read_csv("gisaid_epiflu_isolates.csv")
#data.columns #Para verificar los nombres de las columnas
data_ha = data[data["NA_Segment_Id"].notna()] #Los None se representan como NaN
data2 = data_ha[["Isolate_Id","Location","Collection_Date"]]

#Trabajando con el dataframe
data2['country'] = data2['Location'].apply(lambda x: x.split(' / ')[1] if len(x.split(' / ')) > 1 else None)
data2.drop("Location", axis=1, inplace=True)
data2 = data2.rename(columns={'Isolate_Id': 'strain', 'Collection_Date': 'date'})
data2['year'] = data2['date'].apply(lambda x: x.split('-')[0])
data2["dataset"] = "GISAID"
data2.to_csv("metadata.csv", sep=",", index=False)

#Creando la lista de codigos
codigos = data2[["strain"]]
codigos.to_csv("codigos.txt", sep=",", index=False, header=False)
quit()


------------------------------------------------
#PASO 4:Concatenar los datos de metadata.csv y nextclade.csv
#Calculando el clado en nextclade para los segementos NA y HA
#input: metadata.csv, nextclade.csv
#output: metadata_gisaid.csv

import pandas as pd
data1 = pd.read_csv("metadata.csv")
data1
data2 = pd.read_csv("nextclade.csv",sep=";")
data2
data3 = data2[["seqName","clade"]]
data3 = data3.rename(columns={"seqName":"strain"})

#Concatenar data1 y data3
merge_df = pd.merge(data1,data3,on="strain")
merge_df
merge_df.to_csv("metadata_gisaid.csv", sep=",", index=False)
quit()



-----------------------------------------------
#Datos que se modifican en el archivo original
'''
Isolate_Id >> strain
Location >> country
Collection_Date >> date
Clade >> clade
year (hay que colocarle el año)
dataset (hay que asignarle el nombre "GISAID")
'''
