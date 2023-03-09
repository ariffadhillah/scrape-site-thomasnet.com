import requests
from bs4 import BeautifulSoup
import pandas as pd
# https://www.thomasnet.com/nsearch.html?act=M&cov=NA&heading=26096008&navsec=modify&what=digital
# url = 'https://www.thomasnet.com/nsearch.html?cov=NA&what=digital&heading=26096008'
base_url = 'https://www.thomasnet.com/'
itemlinkdataSupplier = []

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
    'cookie':'PHPSESSID=bt3j5ihfdtu8b96o2b56vc58f5; tnet_sid=fe9c5993-10d3-4ef4-b51b-43a4ca757913; _ga=GA1.2.875644548.1678179744; _gid=GA1.2.616245202.1678179744; _gcl_au=1.1.1887114947.1678179745; _fbp=fb.1.1678179746477.2092807830; __adroll_fpc=c656b51d401c13824e03676a966a5c8f-1678179747654; hubspotutk=655ed3494757d8383a456b37cc5aa858; QuantumMetricUserID=78fa5bcf32202bb249d709719d4d2faf; privacy_disclosure=true; tinid=229579193; refresh_token_cookie=v1.MYiQb6KN6UDZGNq5WmDWwX2lZIvJVHnnJk4jYhSI6WsVHFAgP6JSZfc8aDeg3TPcwBGyynHIays68KSEFf4REgw; UUID=229579193; ln_or=eyIxMjEwODkiOiJkIn0=; QuantumMetricSessionID=551e442b50a1332a6ab4b27a8a777184; _usrvst=7; _tnetses=64087fa0c59cf-20; tnetMode=suppliers; compcov=NA; slsb=; tnetsearch=; __hstc=193920946.655ed3494757d8383a456b37cc5aa858.1678179756850.1678256398951.1678278582544.13; __hssrc=1; UUS=6408864bdddfe; us=6408864bdddfe; TINHEADING=40451205; ctsrc=direct; sitetab=supp; sitemode=supp; LS=/nsearch.html?cov=NA&what=digital&heading=66360207; comphd=66360207; utag_main=v_id:0186bb4ea84e0032058b6381439405081001a0790086e$_sn:8$_ss:0$_st:1678284933603$dc_visit:8$ses_id:1678256391909;exp-session$_pn:170;exp-session$dc_event:1296;exp-session$dc_region:ap-east-1;exp-session; _gat_tealium_0=1; amp_4b1323=AqQmNtFqFip3mlj_VT0RmX.MjI5NTc5MTkz..1gqvu0mk2.1gr0ngkpf.0.ae.ae; amp_4b1323_thomasnet.com=AqQmNtFqFip3mlj_VT0RmX.MjI5NTc5MTkz..1gqvu0mpm.1gr0ngkps.1q1.1qs.3kt; _uetsid=c770ac50bcc611ed864705673e739b77; _uetvid=c7713990bcc611ed83d42d526fc0209c; __ar_v4=IL2VZMDA4VFJNJQGZKZOG5:20230306:7|KJ5TD77QTZBR7EEU7K2NHB:20230306:316|TMTAKRB6LBBSVK3AQQGICC:20230306:324|22GNI4SB75HHRGB3B3KOOG:20230306:324; __hssc=193920946.16.1678278582544'
}

# res = requests.get(url, headers=headers).text
for page in range(1,100):
    r = requests.get(f'')
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

df.to_csv('.csv', index=False)