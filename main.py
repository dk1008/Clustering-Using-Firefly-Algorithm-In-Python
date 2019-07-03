				#################################################################################
				# 										#
				#		Clustering Using Firefly Algorithm In Python			#
				#										#
				#################################################################################




#*********************************************************************************************************************************************
# LB -> Lower Bound 	UB -> Upper Bound
LB = []	# It Take Lower Bound As Input
UB = []	# It take Upper Bound As Input

def Data_boundation(DD, Ndata , sheet):
	for i in range(DD):
		for j in range(NData):
			if(j == 0):
				LB.append(sheet.cell_value(j, i))
				UB.append(sheet.cell_value(j, i))
			else:
				if(LB[i]>sheet.cell_value(j, i)):
					LB[i] = sheet.cell_value(j,i)
				if(UB[i]<sheet.cell_value(j, i)):
					UB[i] = sheet.cell_value(j,i)
#--------------------------------------------------------------------------------------------------------------------------------------------





#START****************************************************************************************************************************************

MD = None	#MD -> Max Distance Of Centroid DataSets 

# This Will Generate A Distance Which Will Be longest Distance Between any Points in centroid Data set
def Max_distance(DD):
	MD = 0
	for i in range(DD):
		MD += math.pow((UB[i]-LB[i]),2)
	return(math.sqrt(MD))
#END-----------------------------------------------------------------------------------------------------------------------------------------





#START***************************************************************************************************************************************

#Distance Between Centroid And A Data Set Point
def Distance_Evaluation(CP , DP):	#CP -> Centroid Data Set	#DP -> Data Point DataSet
	sum = 0
	for i in range(DD):
		sum += math.pow((CP[i]-DP[i]),2)
	return (math.sqrt(abs(sum))) 	#return square of distance between two firefly..

#END-----------------------------------------------------------------------------------------------------------------------------------------





#START****************************************************************************************************************************************

DPP = []	#DPP -> Input Data

#Generating Data Set
#DPP Contain "NData" Unit Of Data Set Value
#Each Data Set Has "DD" Unit Dimension
def Data_Point_Position(Location, wb, sheet, NData , DD):
	for i in range (NData):
		DPP.append([])
		for j in range (DD):
			DPP[i].append([])
			DPP[i][j] = sheet.cell_value(i, j) #initializing the Input Data
#END-----------------------------------------------------------------------------------------------------------------------------------------





#START***************************************************************************************************************************************

LOC = []	#LOC -> List Of Centroid

#generating Fireflies
#LOC List Contain "NF" Unit of Firefly
#Each Firefly has "NC" Unit of Centroid
#Each Centroid has "DD" Unit of Dimension
def Number_Of_Firefly(NF , NC , DD):
	for i in range(NF):
		LOC.append([])
		for j in range(NC):
			LOC[i].append([])
			for k in range(DD):
				LOC[i][j].append([])
				LOC[i][j][k] = random.uniform(LB[k] , UB[k])
#END-----------------------------------------------------------------------------------------------------------------------------------------





#START***************************************************************************************************************************************

CRD = []	#CDL -> Centroid With Respective DataSet
def respective_Centroid_List(NC):
	CRD [:]=[]
	for i in range(NC):
		CRD.append([])
#END-----------------------------------------------------------------------------------------------------------------------------------------





#START***************************************************************************************************************************************

DBCD = []	#DBCD -> Distance Between Centroid And Data Points
def Respective_Centroid_Distance(NF ):
	DBCD[:]=[]
	for i in range(NF):
		DBCD.append([])
		DBCD[i] = 0
#END-----------------------------------------------------------------------------------------------------------------------------------------





#START***************************************************************************************************************************************

#Seprating Dataset According to Their Respective Centroid
#MD -> Max Distance Of Centroid Data Sets
#NData -> Number Of DataSet
#NC -> Each Firefly Has Number of centroid 
def DataSet_Centroid_Connection(MD , NData , NC ):
	for i in range(NData):
		CT_Index = 0	#Allocate A DataSet To A Respective Centroid
		dis = MD
		for j in range(NC):
			distance = Distance_Evaluation(DPP[i] , Centroid[j])
			if(distance < dis):
				dis = distance
				CT_Index = j
		CRD[CT_Index].append(DPP[i])
	 
#END-----------------------------------------------------------------------------------------------------------------------------------------





#START***************************************************************************************************************************************

#Calculating and Allocating Dataset-Centroid Distance According to Their Respective Centroid
#MD -> Max Distance Of Centroid Data Sets
#NF -> Number Of Firefly
#NData -> Number Of DataSet
#NC -> Each Firefly Has Number of centroid 
def DataSet_Centroid_Distance_Connection(MD , NF , NData , NC ):
	for i in range(NF):
		for j in range(NData):
			dis = MD
			for k in range(NC):
				distance = Distance_Evaluation(DPP[j] , LOC[i][k])
				if(distance <= dis):
					dis = distance
			DBCD[i] += dis 

#END-----------------------------------------------------------------------------------------------------------------------------------------





#START***************************************************************************************************************************************
def Firefly_Evaluation(Location , wb , sheet, NData, DD, NF, NC, MD):
	Data_Point_Position(Location, wb, sheet, NData , DD)
	Number_Of_Firefly(NF , NC , DD )
	Respective_Centroid_Distance(NF )
	DataSet_Centroid_Distance_Connection(MD , NF , NData , NC )

	#Firefly Algorithm.....
	for i in range(MaxGeneration):
		for j in range(NF):
			for k in range(NF):
				if(DBCD[j] > DBCD[k]):
					r_square = DBCD[j]-DBCD[k]
					for l in range(NC):
						for m in range(DD):
							r_square = (Distance_Evaluation(LOC[j][l] , LOC[k][l]))**2
							LOC[j][l][m] += BETA*math.exp(-GAMMA*r_square)*(LOC[k][l][m]-LOC[j][l][m]) + BETA*math.exp(-GAMMA*r_square)*(LOC[k][l][m]-LOC[j][l][m]) + ALPHA*(random.uniform(0,1) - .5)
							if(LOC[j][l][m] < LB[m]):
								LOC[j][l][m] = random.uniform(LB[m],UB[m])
							if(LOC[j][l][m] > UB[m]):
								LOC[j][l][m] = random.uniform(LB[m],UB[m])
		Respective_Centroid_Distance(NF )
		DataSet_Centroid_Distance_Connection(MD , NF , NData , NC )
#END-----------------------------------------------------------------------------------------------------------------------------------------





#START***************************************************************************************************************************************

def Centroid_Average(NC , DD):
	for i in range(NC):
		for j in range(DD):
			total = 0
			avg = 0
			for k in range(len(CRD[i])):
				total += CRD[i][k][j]
			if(total != 0):
				avg = total/len(CRD[i])
			Centroid[i][j] = avg 
#END-----------------------------------------------------------------------------------------------------------------------------------------





#START***************************************************************************************************************************************
#K-Mean Algorithm.....
Centroid = None

def K_Means_Evaluation(NC, MD, NData, DD):
	for i in range(10):
		respective_Centroid_List(NC)
		DataSet_Centroid_Connection(MD , NData , NC )
		Centroid_Average(NC , DD)
		print(Centroid)
#END-----------------------------------------------------------------------------------------------------------------------------------------





#START***************************************************************************************************************************************
if __name__ =="__main__":
	import xlrd
	import random
	import math

	Location = raw_input("Enter Location Of Input Data File ")
	#Location = ("/home/lenovo/Documents/new clustering/glass_Data_set.xlsx")
	wb = xlrd.open_workbook(Location) 
	sheet = wb.sheet_by_index(0)

	## It Contains Data Set Values
	NData = sheet.nrows
	
	## It Take Dimension Of Data Set As Input
	DD = sheet.ncols
	
	## It Take Number Of Firefly as Input 
	MaxGeneration = int(input("Enter MaxGeneration Value "))
	
	## It Take Number Of Firefly as Input 
	NF = int(input("Enter Number Of Firefly "))
	
	## It Take Number Of Centroid As Input
	NC = int(input("Every Firefly Has Number Of Centriod: "))
	
	ALPHA = .7
	BETA = 1
	GAMMA = 1
	
	Data_boundation(DD, NData , sheet)
	MD = Max_distance(DD)
	Firefly_Evaluation(Location , wb , sheet, NData, DD, NF, NC, MD)
	Centroid = LOC[DBCD.index(min(DBCD))]
	K_Means_Evaluation(NC, MD, NData, DD)
#END-----------------------------------------------------------------------------------------------------------------------------------------

