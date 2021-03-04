import pandas as pd

file=pd.read_excel(r'H:\Accounting Dept Shared Files\CPC\Month End Close\Participations\FY21\PART_BALS_02.xls')
#print(file.head())

cri_app=file["GL MATRIX CODE"].str.contains("APP")
file1=file[~cri_app]
cri_ina=file1["GL MATRIX CODE"].str.contains("INACTV")
file2=file1[~cri_ina]
#print(file2)
cri_inv=(file2["INVESTOR NUMBER"]==301) | (file2["INVESTOR NUMBER"]==302) | (file2["INVESTOR NUMBER"]==303) | (file2["INVESTOR NUMBER"]==307)
file3=file2[~cri_inv]

#file3.to_csv("file3.csv")

cri_loan= (file3["GL MATRIX CODE"].str.contains("CL_")) & (file3["INVESTOR NUMBER"]!=309) & (file3["INVESTOR NUMBER"]<900)
file4=file3[~cri_loan]
#file4.to_csv('file4.csv')

cri_upb_0=file4["CURRENT UPB"]==0
cri_upb_others=file4["CURRENT UPB"] !=0

file_without_upb=file4[cri_upb_0]
#file_without_upb.to_csv("file_without_upb.csv")
#print(file_without_upb["CURRENT UPB"])

file_with_upb=file4[cri_upb_others]


cri_loan_type=file_without_upb["GL MATRIX CODE"].str.contains("PL_")
file_without_upb_1=file_without_upb[~cri_loan_type]
#file_without_upb_1.to_csv("1.csv")

file_without_upb_1["ORIGINAL LOAN DATE"]=file_without_upb_1["ORIGINAL LOAN DATE"].astype("str")
file_without_upb_1["year"]=file_without_upb_1["ORIGINAL LOAN DATE"].str.slice(start=-4)
#print(file_without_upb_1)

cri_year=file_without_upb_1.year.astype(int)>2016
file_without_upb_2=file_without_upb_1[cri_year]
#print(file_without_upb_2)

cri_ownership=file_without_upb_2["PARTICIPATION % OWNE"]!=0
file_without_upb_3=file_without_upb_2[cri_ownership]
file_without_upb_3.to_csv("withoutupb_02.csv")
#print(file_without_upb_3)


dl_extract=pd.read_excel(r"H:\Accounting Dept Shared Files\CPC\Month End Close\Loan Reconciliation\FY 2021\08 Feb 2021\Strategy Data Extract 02-2021.xlsx")
dl_extract_loan=dl_extract["CPC#"]
participation_without_upb=file_without_upb_3.merge(dl_extract_loan, left_on='LOAN NUMBER',right_on='CPC#',how="inner")
participation_without_upb.to_csv("participation without upb_02.csv")

cri_inv=file_with_upb["INVESTOR NUMBER"] !=751
file_with_upb_new=file_with_upb[cri_inv]
file_with_upb_new.to_csv("file_with_upb_final_02.csv")

