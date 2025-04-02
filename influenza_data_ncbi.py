


###############################################################################
##FLUJO DE TRABAJO PARA MANEJAR DATOS DE INFLUENZA DESCARGADOS DE NCBI VIRUS##
##############################################################################



##### PASO 1: COMPILANDO LOS DATOS
#Compilar la metadata de BLAST-NCBI en python, saldra una metadata modificada y una lista de codigos
#input: sequences_ncbi.csv
#output: metadata1.csv y codigos.txt

#Importando las librerias
import pandas as pd

#Pasos iniciales, input sequences_ncbi.csv
data = pd.read_csv("sequences_ncbi.csv")
#data.columns #Para verificar los nombres de las columnas
#data_ha = data[data["HA_Segment_Id"].notna()] #Los None se representan como NaN
data2 = data[["Accession","Collection_Date","Country"]]


#Trabajando con el dataframe
data2 = data2.rename(columns={'Accession': 'strain', 'Collection_Date': 'date', "Country": "country"})
data2['year'] = data2['date'].apply(lambda x: x.split('-')[0])
data2["dataset"] = "GenBank"
data2.to_csv("metadata1.csv", sep=",", index=False)

#Creando la lista de codigos
codigos = data2[["strain"]]
codigos.to_csv("codigos.txt", sep=",", index=False, header=False)
quit()


.........................................................................................

###PASO2:
#Extraer los codigos que tienen metadata y remover duplicados
seqtk subseq sequences_ncbi.fasta codigos.txt > filtrado.fasta
seqkit rmdup filtrado.fasta > secuencias_ncbi.fasta
rm filtrado.fasta codigos.txt

#Correr nextclade para NA, cambiar la base de datos
nextclade run --input-dataset /home/veronica/Programas/database_nextclade/H1N1_NA_MW626056 --output-csv nextclade.csv secuencias_ncbi.fasta




------------...........................................-----------------------------------

###PASO 3:Concatenar los datos de metadata1.csv y nextclade.csv
#Calculando el clado en nextclade para los segementos NA y HA
#input: metadata1.csv, nextclade.csv
#output: metadata_ncbi.csv

import pandas as pd
data1 = pd.read_csv("metadata1.csv")
data1
data2 = pd.read_csv("nextclade.csv",sep=";")
data2
data3 = data2[["seqName","clade"]]
data3 = data3.rename(columns={"seqName":"strain"})

#Concatenar data1 y data3
merge_df = pd.merge(data1,data3,on="strain")
merge_df
merge_df.to_csv("metadata_ncbi.csv", sep=",", index=False)
quit()



----------------------------------------------------------------------------------------

###PASO4: Eliminando archivos
rm metadata1.csv nextclade.csv sequences_ncbi.csv sequences_ncbi.fasta


---------------------------------------------------------------------------------------

#Los archivos finales son metadata_ncbi.csv y secuencias_ncbi.fasta
