import pandas as pd

Total_MSR_file=pd.read_excel(r'H:\Accounting Dept Shared Files\CPC\Month End Close\Loan Reconciliation\FY 2021\07 Jan 2021\Strategy Data Extract Jan 21-for total portofolio-do not delete.xlsx')
#print(Total_MSR_file.head())
total_MSR=Total_MSR_file.sort_values("COMPANY CODE")
#print(total_MSR.tail())
#print(total_MSR.shape[0])
total_MSR_file=total_MSR.iloc[:total_MSR.shape[0]]
total_MSR_file.dropna(how='all',inplace=True)
#print(total_MSR.tail())
#print(total_MSR_file)


criteria_5=total_MSR_file["COMPANY CODE"]!=5
total_MSR_without_5=total_MSR_file[criteria_5]
#print(total_MSR_without_5.shape)

criteria_900=(total_MSR_without_5["INV CODE"] <900) & (total_MSR_without_5["INV CODE"] !=684) & (total_MSR_without_5["INV CODE"] !=685) & (total_MSR_without_5["INV CODE"] !=690) & (total_MSR_without_5["INV CODE"] !=694 & (total_MSR_without_5["INV CODE"] !=751))
total_MSR_data=total_MSR_without_5[criteria_900]
#total_MSR_data.to_csv("a.csv")

Total_portofolio_pricing=pd.read_excel(r'H:\Accounting Dept Shared Files\CPC\Month End Close\Mortgage Servicing Rights\FY 2021\01 July 2020\MSR Total Portofolio 2020 Preswick pricing-do not delete.xlsx')
#print(Total_portofolio_pricing)

new_pricing=Total_portofolio_pricing[["LOAN #","Factor","Pricing_ref"]]
pricing_by_loan=new_pricing[:2202]
pricing_by_investor=new_pricing[2337:new_pricing.shape[0]]
#print(pricing_by_investor)
#print(pricing_by_investor)
#print(pricing_by_loan)
#new_pricing.to_csv('e.csv')
#print(new_pricing)
                                     
#print(new_pricing)

merged_file=total_MSR_data.merge(pricing_by_loan,how='left',left_on='ref',right_on='Pricing_ref').drop(["LOAN #","Pricing_ref"],axis=1)
merged_file['pricing_by_inv']=merged_file['INV CODE'].map(pricing_by_investor.set_index('LOAN #')['Factor'].to_dict())
#print(merged_file)
#merged_file.to_csv('b.csv')
#print(merged_file)
#print(merged_file.Factor.isnull().sum())

#merged_file_final=merged_file.merge(pricing_by_investor,how='left',left_on='INV CODE',right_on='LOAN #').drop(["LOAN #","Pricing_ref"],axis=1).drop_duplicates()
#merged_file_final.to_csv('k.csv')


#print(merged_file_final)

merged_file.rename(columns={'Factor': 'pricing_by_loan'},inplace=True)
#merged_file.to_csv('C.csv')

merged_file['pricing']=merged_file['pricing_by_loan'].fillna(merged_file['pricing_by_inv'])
merged_file['valuation']= merged_file['pricing'] * merged_file["INVESTOR'S SHARE OF CURRENT BALANCE"]
merged_file.to_csv('Total Portfolio_Jan 21.csv')
                                                                
                                                                     
