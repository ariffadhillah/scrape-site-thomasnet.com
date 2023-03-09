import requests
from bs4 import BeautifulSoup
import pandas as pd
# https://www.thomasnet.com/nsearch.html?act=M&cov=NA&heading=26096008&navsec=modify&what=digital
# url = 'https://www.thomasnet.com/nsearch.html?cov=NA&what=digital&heading=26096008'
base_url = 'https://www.thomasnet.com/'
itemlinkdataSupplier = []

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
    'cookie':'tnet_sid=fe9c5993-10d3-4ef4-b51b-43a4ca757913; _ga=GA1.2.875644548.1678179744; _gid=GA1.2.616245202.1678179744; _gcl_au=1.1.1887114947.1678179745; _fbp=fb.1.1678179746477.2092807830; hubspotutk=655ed3494757d8383a456b37cc5aa858; QuantumMetricUserID=78fa5bcf32202bb249d709719d4d2faf; privacy_disclosure=true; tinid=229579193; refresh_token_cookie=v1.MYiQb6KN6UDZGNq5WmDWwX2lZIvJVHnnJk4jYhSI6WsVHFAgP6JSZfc8aDeg3TPcwBGyynHIays68KSEFf4REgw; UUID=229579193; _usrvst=9; _tnetses=6409733d43056-45; tnetMode=suppliers; tnetsearch=; __hstc=193920946.655ed3494757d8383a456b37cc5aa858.1678179756850.1678304085036.1678340934625.15; __hssrc=1; QuantumMetricSessionID=fab8aec6d207df39d1fef6b0f292d976; compcov=NA; slsb=; sitetab=supp; sitemode=supp; comphd=25441601; UUS=640974e5e6121; us=640974e5e6121; TINHEADING=25441601; ctsrc=direct; LS=/nsearch.html?cov=NA&heading=25441601&what=electronic&pg=113; utag_main=v_id:0186bb4ea84e0032058b6381439405081001a0790086e$_sn:10$_ss:0$_st:1678343217830$dc_visit:10$ses_id:1678340924580;exp-session$_pn:11;exp-session$dc_event:66;exp-session$dc_region:ap-east-1;exp-session; _gat_tealium_0=1; _uetsid=c770ac50bcc611ed864705673e739b77; _uetvid=c7713990bcc611ed83d42d526fc0209c; amp_4b1323=AqQmNtFqFip3mlj_VT0RmX.MjI5NTc5MTkz..1gr2ek9po.1gr2f3b4m.0.h7.h7; amp_4b1323_thomasnet.com=AqQmNtFqFip3mlj_VT0RmX.MjI5NTc5MTkz..1gr2empqn.1gr2f3b55.366.376.6dc; __hssc=193920946.9.1678340934625; ad_click=UR'
}

# res = requests.get(url, headers=headers).text
for page in range(1,150):
    r = requests.get(f'https://www.thomasnet.com/nsearch.html?cov=NA&heading=25441601&what=electronic&pg={page}')
    # r = requests.get(f'https://www.thomasnet.com/nsearch.html?cov=NA&what=digital&heading=3180106')
    soup = BeautifulSoup(r.content, 'lxml')
    dataSupplier = soup.find_all('h2', class_='profile-card__title')
    
    for item in dataSupplier:
        for link in item.find_all('a', href=True):
            itemlinkdataSupplier.append(base_url + link['href'])

companylist = []

for link in itemlinkdataSupplier:
    r = requests.get(link, headers=headers)

    soup = BeautifulSoup(r.content, 'lxml')
    
    h1 = soup.find("h1", {"class": "copro-supplier-name"})
    
    try:
        div_to_remove = h1.find("div", {"id": "copro-supplier-main-badges-container"})
        div_to_remove.decompose()
        company_name = h1.get_text(strip=True)

    except:
        div_to_remove =''   
        company_name =''

    
    # element_company_name = soup.find('h1', {'class': 'copro-supplier-main-badges-container'})
    # try:
    #     company_name = element_company_name.find('a').text.strip()
    # except:
    #     company_name =''
    # phone_number = soup.find('p', class_='phoneline').text.strip().replace('ico-phone', '').replace('ico-website', '').replace('Visit Website', '').replace('•', '').replace(' Call Supplier', '').replace('Request Information', '').replace('ico-contact', '')

    number = soup.find('p', class_='phoneline')
    try: 
        phone_number = number.find('span', class_='').text.strip()
    except:
        phone_number = ''
        
    # print(phone_number)
    try:
        website = soup.find('a', class_='visit-website-link')['href']
    except:
        website = ''
    try:
        location = soup.find('span', class_='copro-address-line').text.strip()
    except:
        location = ''
    try:
        company_type = soup.find('span', class_='copro-company-type').text.strip()
    except:
        company_type = ''

    textcompanyDescriptionbyThomasnet = soup.find('div', {'id': 'copro_about'})
    try:
        companyDescriptionbyThomasnet = textcompanyDescriptionbyThomasnet.find('p').text.strip()
    except:
        companyDescriptionbyThomasnet = ''
    try:
        companyDescriptionbythecompany = textcompanyDescriptionbyThomasnet.find_all('p')[1].text.strip()
    except:
        companyDescriptionbythecompany = ''

    try:
        linkedinURL = soup.find('a', {'data-conversion_action': 'Linkedin'})['href'].replace('https://', '')

    except:
        linkedinURL = ''
        
    textdisckription = soup.find('div', {'class': 'bdcol2 match-height'})

    try:
        element_annualSales = textdisckription.find_all('div', {'class': 'bizdetail'})[3]
        annualSales = element_annualSales.find('li').text.strip()
    except:
        element_annualSales = ''
        annualSales =''

    try:
        element_No_of_Employees = textdisckription.find_all('div', {'class': 'bizdetail'})[4]
        No_of_Employees = element_No_of_Employees.find('li').text.strip() + " " + " Employees"
    except:
        element_No_of_Employees = ''
        No_of_Employees =''
    
    try:
        services = soup.find('div', {'id': 'copro_prodserv_cats'})
        hidden_h3_element = services.find('h3')
        # remove elemen span
        hidden_h3_element.decompose()
    except:
        services = ''
    try:
        manufacturingservices = services.find('div', {'class': 'prodserv_group'}).text.strip()
    except:
        manufacturingservices = 'No MANUFACTURING SERVICES'
    try: 
        allproductservices = services.find_all('div', {'class': 'prodserv_group'})[1].text.strip()
    except:
        allproductservices ='No ALL PRODUCTS / SERVICES'


    data  = {
        'Company name': company_name,
        'Phone number': phone_number,
        'website (Homepage)': website,
        'Location': location,
        'Company type': company_type,
        'Company Description by Thomasnet': companyDescriptionbyThomasnet,
        'Company Description by the company': companyDescriptionbythecompany,
        'Linkedin URL': linkedinURL,
        'Annual Sales:': annualSales,
        'No of Employees:': No_of_Employees,
        'MANUFACTURING SERVICES': manufacturingservices,
        'ALL PRODUCTS / SERVICES': allproductservices
    }
    companylist.append(data)
    print('Saving:', data['Company name'])


df = pd.DataFrame(companylist, columns=['Company name', 'Phone number', 'website (Homepage)','Location', 'Company type', 'Company Description by Thomasnet','Company Description by the company', 'Linkedin URL','Annual Sales:', 'No of Employees:' , 'MANUFACTURING SERVICES', 'ALL PRODUCTS / SERVICES' ])

df.to_csv('Electronic Equipment & Devices.csv', index=False)
# belum slesqi