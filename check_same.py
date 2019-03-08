import pandas
colnames = ['0', '1', 'carplate']
data = pandas.read_csv('F.csv', names=colnames)
carplates = set(data.carplate)
#print(carplates)

colnames2 = ['02', '12', 'carplate2']
data2 = pandas.read_csv('U.csv', names=colnames2)
carplates2 = set(data2.carplate2)
#print(carplates2)

colnames3 = ['03', '13', 'carplate3']
data3 = pandas.read_csv('S.csv', names=colnames3)
carplates3 = set(data3.carplate3)

with open('test.csv','r') as in_file, open('test-result.csv','w') as out_file:
	out_file.write(next(in_file))
	for line in in_file:
		plate=line.split(",")[34]
		plate_slipt=line.strip() 
		#print((plate))
		if plate in carplates:
			out_file.write(plate_slipt+','+'F'+'\n')
		elif plate in carplates2:
			#print('U')
			out_file.write(plate_slipt+','+'U'+'\n')
		elif plate in carplates3:
			out_file.write(plate_slipt+','+'S'+'\n')
		else:
			out_file.write(line)
