#have CC keyword or not(only keep data within 0-90 days):  
with open('../TBN_CUST_BEHAVIOR.csv','r') as in_file, open('KEY_OR_NO.csv','w') as out_file:
    seen = set() 
    (next(in_file))
    out_file.write('CUST_NO,KEY_OR_NO'+'\n')
    for line in in_file:
        address=line.split(",")[2]
        visit_date=line.split(",")[1]   
        idnum=line.split(",")[0] 
        if idnum in seen: 
            continue # skip duplicate

        if 'cugfkt'  in address and int(visit_date)< 9538:
            seen.add(idnum)
            out_file.write(idnum+','+'1'+'\n')
#############################################################################################
#count keyword number
from collections import Counter
import csv
with open('../TBN_CUST_BEHAVIOR.csv','r') as in_file, open('KEY_TIMES.csv','w') as out_file:
    seen=[]
    next(in_file)
    #out_file.write('CUST_NO,VISIT_TIMES')
    for line in in_file:
        address=line.split(",")[2]
        idnum=line.split(",")[0]
        visit_date=line.split(",")[1]        
        if 'cugfkt'  in address and int(visit_date)< 9538:
            seen.append(idnum)
    out_file.write('CUST_NO,VISIT_TIMES\n')  
    for tag, count in Counter(seen).items():  
        out_file.write('{},{}\n'.format(tag, count))  
############################################################################################

#have or not recent date
with open('../TBN_RECENT_DT.csv','r') as in_file, open('RECENT_DATE_1.csv','w') as out_file:
    out_file.write('CUST_NO,BOUGHT_OR_NOT'+'\n')
    seen = set() # set for fast O(1) amortized lookup
    next(in_file)
    for line in in_file:
        idnum=line.split(",")[0]
        CC_RECENT=line.split(",")[1]
        
        if idnum in seen: 
            continue # skip duplicate

        seen.add(idnum)
        out_file.write(idnum+','+'1'+'\n')
#############################################################################################
#recent date in three years
with open('../TBN_RECENT_DT.csv','r') as in_file, open('THREE_YEARS.csv','w') as out_file:
    seen = set() 
    out_file.write('CUST_NO,THREE_YEARS'+'\n')
    (next(in_file))
    for line in in_file:
        idnum=line.split(",")[0]
        CC_RECENT=line.split(",")[1]
        
        if idnum in seen: 
            continue # skip duplicate
        if CC_RECENT!='""' and (float(CC_RECENT))> 8368:
            seen.add(idnum)
            out_file.write(idnum+','+'1'+'\n') 

#############################################################################################
#applied in 90-120
with open('../TBN_CC_APPLY.csv','r') as in_file, open('APPLIED.csv','w') as out_file:
    seen = set() 
    next(in_file)
    out_file.write('CUST_NO,DEAL_OR_NO_DEAL'+'\n')
    for line in in_file:
        idnum=line.split(",")[0]
        CC_RECENT=line.split(",")[1]
        
        if idnum in seen: 
            continue # skip duplicate


        if int(CC_RECENT)> 9538:
            seen.add(idnum)
            out_file.write(idnum+','+'1'+'\n')
######################################################################################
#merge all data
import pandas as pd 
dir="./"

df1 = pd.read_csv(dir+"KEY_OR_NO.csv",index_col=[0], parse_dates=[0])
df2 = pd.read_csv(dir+"KEY_TIMES.csv",index_col=[0], parse_dates=[0])
merged1 = df1.merge(df2, on='CUST_NO', how='outer')
df3 = pd.read_csv(dir+"RECENT_DATE_1.csv",index_col=[0], parse_dates=[0])
merged2 = merged1.merge(df3, on='CUST_NO', how='outer')
df4 = pd.read_csv(dir+"THREE_YEARS.csv",index_col=[0], parse_dates=[0])
merged3 = merged2.merge(df4, on='CUST_NO', how='outer')
df5 = pd.read_csv(dir+"../TBN_CIF.csv",index_col=[0], parse_dates=[0])
merged4 = merged3.merge(df5, on='CUST_NO', how='outer')
df6 = pd.read_csv(dir+"APPLIED.csv",index_col=[0], parse_dates=[0])
merged = merged4.merge(df6, on='CUST_NO', how='outer')

merged.to_csv("output_cc_mergeall.csv")
#########################################################################################
#fill in blank data
with open('output_cc_mergeall.csv','r') as in_file, open('filledin.csv','w') as out_file:
    out_file.write(next(in_file))
    for line in in_file:
        KEY_OR_NO=line.split(",")[1]
        VISIT_TIMES=line.split(",")[2]
        BOUGHT_OR_NOT=line.split(",")[3]
        THREE_YEARS=line.split(",")[4]
        DEAL_OR_NO_DEAL=line.split(",")[12]
        
        CUST_NO=line.split(",")[0]
        AGE=line.split(",")[5]
        CHILDREN_CNT=line.split(",")[6]
        CUST_START_DT=line.split(",")[7]
        EDU_CODE=line.split(",")[8]
        GENDER_CODE=line.split(",")[9]
        INCOME_RANGE_CODE=line.split(",")[10]
        WORK_MTHS=line.split(",")[11]
        if KEY_OR_NO =='': 
            KEY_OR_NO='0'
            #print(KEY_OR_NO)
        if VISIT_TIMES =='': 
            VISIT_TIMES='0'
        if BOUGHT_OR_NOT =='': 
            BOUGHT_OR_NOT='0'
        if THREE_YEARS == '':
            THREE_YEARS='0'
        if DEAL_OR_NO_DEAL.isspace(): 
            DEAL_OR_NO_DEAL='0'
        else:
            DEAL_OR_NO_DEAL='1'

        out_file.write(CUST_NO+','+KEY_OR_NO+','+VISIT_TIMES+','+BOUGHT_OR_NOT+','+THREE_YEARS+','+\
            AGE+','+CHILDREN_CNT+','+CUST_START_DT+','+EDU_CODE+','+GENDER_CODE+','+\
            INCOME_RANGE_CODE+','+WORK_MTHS+','+DEAL_OR_NO_DEAL+'\n')

        


