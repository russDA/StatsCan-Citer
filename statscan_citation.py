#An application to auto-generate Statistic's Canada Citations

#Russell Abraira

from bs4 import BeautifulSoup
import requests
import tkinter as tk
import pyperclip
from datetime import date
import klembord as klb

def main():
    """
    
    Application to take in user URL of a Stats Can dataset, and generate the citation necessary for it
    
    """
    
    #Housekeeping variables and the like
    #
    klb.init()
    citation_mla = 'MLA'
    citation_apa = 'APA'
    citation_chicago = 'Chicago'
    citation_ieee = 'IEEE'
    citation_statscan = 'StatsCan'
    
    ready = 'Waiting on Button...'
    
    #Obtain the current date
    #
    the_day = str(date.today().day)
    the_month = str(date.today().month)
    the_year = str(date.today().year)
    
    #Function to convert month to full str, using dictionary
    #
    def make_month_string(mm):
        month_int_long = ['01','02','03','04','05','06','07','08','09']
        month_int = ['1','2','3','4','5','6','7','8','9','10','11','12']
        month_str = ['January','February','March','April','May','June','July','August','September','October','November','December']
        
        #Handle all cases, convert to format we want
        #
        mlong_to_mshort = dict(zip(month_int_long, month_int[:9]))
        mint_to_mstr_tens = dict(zip(month_int[9:], month_str[9:]))
        mint_to_mstr_ones = dict(zip(month_int[:9], month_str[:9]))
        
        #Conert user input to single digits, if need be (Jan-Sep)
        #
        for l, s in mlong_to_mshort.items():
            mm = mm.replace(l, s)
        
        #Must cycle through october-Dec first, because python will convert, for example, 10(october) to January0 instead. It reads the 1 -> Jan 'too quickly'
        #
        for i, s in mint_to_mstr_tens.items():
            mm = mm.replace(i, s)
        for i, s, in mint_to_mstr_ones.items():
            mm = mm.replace(i,s)
        
        #Return the value after it has been spit out as a str
        #
        return mm
    
    the_month_str = make_month_string(the_month)
    
    
    #Functions to get the necessary info from the URL, which the user will pass
    
    
    #Function to obtain the catalogue no
    #
    def get_cat(site_url):
        
        the_site = requests.get(site_url)
        soup = BeautifulSoup(the_site.text, features='lxml')
        catalogue_no = soup.find('p', {'class':'margin-top-large font-small'}).text
        
        catalogue_no = str.split(catalogue_no, 'no. ')[1]
        
        return catalogue_no
    
    #Function to get the site title
    #
    def get_title(site_url):
        
        the_site = requests.get(site_url)
        soup = BeautifulSoup(the_site.text, features='lxml')
        title = soup.find('h2', {'id':'table-title'}).text
        
        return title
        
    #Function to get the site publication date. This is the last time this table was updated. will be a list:
        #[0] = day, [1] = month, [2] = year, [3] = month_string
    def pub_date(site_url):
        
        the_site = requests.get(site_url)
        soup = BeautifulSoup(the_site.text, features='lxml')
        
        pub_date = soup.find('time',  {'property': 'dateModified'}).text
        
        pub_date = str.split(pub_date, '-')
        pub_day = str.strip(pub_date[2])
        pub_month = pub_date[1]
        pub_year = pub_date[0]
        
        pub_month_str = make_month_string(pub_month)
        
        return [pub_day, pub_month, pub_year, pub_month_str]
    
    
    """
    
    Setting up the tkinter (Application)
    
    """
    
    #Setup and welcome message
    #
    root = tk.Tk()
    root.title('StatsCan Citer')
    root.geometry('1040x380')
    welcome_msg = tk.Label(root, text='Welcome! I\'m an application which will generate citations for Statistic\'s Canada Data Tables!\n' + 
                            '\n\nFind the page where the main header is \'Data Tables, 20XX Census\', with the data below.', font=20)
    welcome_msg.grid(row = 1, column = 1)
    
    status_label = tk.Label(root, text='Status:')
    status_label.grid(row = 6, column = 3)
    ready_label = tk.Label(root, text=f'*{ready}*', font=20)
    ready_label.grid(row = 7, column = 3)
    
    #Explanatory instructions on how to use the app
    #
    #Will NOT handle users not honoring the format
    #
    date_warning = tk.Label(root, text='If you wish to specify the access date (i.e. not take current date) you must follow the DD-MM-YYYY format, else I will misbehave.')
    date_warning.grid(row = 2, column = 1)
    
    enter_here = tk.Label(root, text="Click the button *AFTER* you've pasted the URL into the box below(Press Ctrl + v in the box). Date & Title are optional.\n")
    enter_here.grid(row = 3, column = 1)
    
    #Creation of URL, Date, and Title Entry forms, as well as their corresponding labels
    #
    url_label = tk.Label(root, text = 'Enter URL below:')
    url_label.grid(row = 4, column = 1)
    url_entry = tk.Entry()
    url_entry.grid( row = 5, column = 1)
    
    date_label = tk.Label(root, text = 'Date(DD-MM-YYYY):')
    date_label.grid(row = 6, column =1)
    date_entry = tk.Entry()
    date_entry.grid(row = 7, column = 1)
    
    title_label = tk.Label(root, text = 'Title(Optional):')
    title_label.grid(row = 8, column =1)
    title_entry = tk.Entry()
    title_entry.grid(row = 9, column = 1)
    
    #A final warning to user to enter a URL, or else it will give bunk info
    last_warning = tk.Label(root, text='*WARNING* Important that the URL is properly pasted, or else I will give you placeholder citations, and/or possibly misbehave')
    last_warning.grid(row=10, column = 1)
    
    #Defining button functionality for each citation style
    #
    def copy_mla(): 
        
        ready_label.configure(text='MLA ready')
        #Getting and checking for user values
        #
        user_url = url_entry.get()
        user_title = title_entry.get()
        user_date = date_entry.get()
        user_day = ''
        user_month = ''
        user_year = ''
        user_month_str = ''
        
        user_catalogue = get_cat(user_url)
        
        if user_title == '':
            user_title = get_title(user_url)
            
        #Here I am first checking if the user input nothing, if so, going to take today's values as access date
        #
        if user_date == '':
            user_day = the_day
            user_month = the_month
            user_year = the_year
            user_month_str = the_month_str
        
        #IF they did input something, I will split that up into necessary info
        #
        else:
            date_vals = str.split(user_date, '-')
            user_day = date_vals[0]
            user_month = date_vals[1]
            user_year = date_vals[2]
            user_month_str = make_month_string(user_month)
            
        citation_mla = klb.set_with_rich_text('', f'Canada, Statistics Canada. <i>{user_title} Census of Population, catalogue no. {user_catalogue}</i>, www.statscan.gc.ca. Accessed {user_day} {user_month_str} {user_year}. Dataset.')
        
        pyperclip.copy(citation_mla)
        
        
    def copy_apa():
        
        ready_label.configure(text='APA ready')
        #Getting and checking for user values
        #
        user_url = url_entry.get()
        user_title = title_entry.get()
        user_date = date_entry.get()
        user_day = ''
        user_month = ''
        user_year = ''
        user_month_str = ''
        
        #[0] = day, [1] = month, [2] = year, [3] = month_string
        user_pub = pub_date(user_url)
        user_pub_year = user_pub[2]
        
        user_catalogue = get_cat(user_url)
        
        if user_title == '':
            user_title = get_title(user_url)
            
        #Here I am first checking if the user input nothing, if so, going to take today's values as access date
        #
        if user_date == '':
            user_day = the_day
            user_month = the_month
            user_year = the_year
            user_month_str = the_month_str
        
        #IF they did input something, I will split that up into necessary info
        #
        else:
            date_vals = str.split(user_date, '-')
            user_day = date_vals[0]
            user_month = date_vals[1]
            user_year = date_vals[2]
            user_month_str = make_month_string(user_month)
            
    
        citation_apa = klb.set_with_rich_text('', f'Canada, Statistics Canada. ({user_pub_year}). <i>{user_title}</i>. (Catalogue no. {user_catalogue}). Retrieved from www.statscan.gc.ca [Dataset]')
        
        pyperclip.copy(citation_apa)
        
    def copy_chicago():
        
        ready_label.configure(text='Chicago ready')
        #Getting and checking for user values
        #
        user_url = url_entry.get()
        user_title = title_entry.get()
        user_date = date_entry.get()
        user_day = ''
        user_month = ''
        user_year = ''
        user_month_str = ''
        
        #[0] = day, [1] = month, [2] = year, [3] = month_string
        user_pub = pub_date(user_url)
        user_pub_month_str = user_pub[3]
        user_pub_day = user_pub[0]
        user_pub_year = user_pub[2]
        
        user_catalogue = get_cat(user_url)
        
        if user_title == '':
            user_title = get_title(user_url)
            
        #Here I am first checking if the user input nothing, if so, going to take today's values as access date
        #
        if user_date == '':
            user_day = the_day
            user_month = the_month
            user_year = the_year
            user_month_str = the_month_str
        
        #IF they did input something, I will split that up into necessary info
        #
        else:
            date_vals = str.split(user_date, '-')
            user_day = date_vals[0]
            user_month = date_vals[1]
            user_year = date_vals[2]
            user_month_str = make_month_string(user_month)
        
        citation_chicago = klb.set_with_rich_text('', f'Canada, Statistics Canada. \"{user_title} Census of Population, catalogue no. {user_catalogue}\". Last Modified {user_pub_month_str} {user_pub_day}, {user_pub_year}. www.statscan.gc.ca.')
        
        pyperclip.copy(citation_chicago)
        
    def copy_ieee():
        
        ready_label.configure(text='IEEE ready')
        #Getting and checking for user values
        #
        user_url = url_entry.get()
        user_title = title_entry.get()
        user_date = date_entry.get()
        user_day = ''
        user_month = ''
        user_year = ''
        user_month_str = ''
        
        #[0] = day, [1] = month, [2] = year, [3] = month_string
        user_pub = pub_date(user_url)
        user_pub_month_str = user_pub[3]
        user_pub_day = user_pub[0]
        user_pub_year = user_pub[2]
        
        user_catalogue = get_cat(user_url)
        
        if user_title == '':
            user_title = get_title(user_url)
            
        #Here I am first checking if the user input nothing, if so, going to take today's values as access date
        #
        if user_date == '':
            user_day = the_day
            user_month = the_month
            user_year = the_year
            user_month_str = the_month_str
        
        #IF they did input something, I will split that up into necessary info
        #
        else:
            date_vals = str.split(user_date, '-')
            user_day = date_vals[0]
            user_month = date_vals[1]
            user_year = date_vals[2]
            user_month_str = make_month_string(user_month)
        
        citation_ieee = klb.set_with_rich_text('', f'Canada, Statistics Canada. \"{user_title}, catalogue no. {user_catalogue}\" in <i>Statistics Canada, Census of Population</i>, {user_pub_month_str} {user_pub_day}, {user_pub_year}. [Online]. Available: www.statscan.gc.ca, Accessed on: {user_month_str} {user_day}, {user_year}.')
        
        pyperclip.copy(citation_ieee)
        
    def copy_statscan():
        
        ready_label.configure(text='StatsCan ready')
        user_url = url_entry.get()
        user_catalogue = get_cat(user_url)
        
        citation_statscan = f'Source: Statistics Canada, 2016 Census of Population, Statistics Canada Catalogue no. {user_catalogue}'
        
        pyperclip.copy(citation_statscan)
    
    #Creating each button, individually, with indicator above
    #
    select_label = tk.Label(root, text='Click on the button to copy \n that citation into your clipboard:')
    select_label.grid(row = 4, column = 2)
    mla_button = tk.Button(root, text='Copy MLA Citation', command=copy_mla)
    mla_button.grid(row = 5, column = 2)
    mla_button = tk.Button(root, text='Copy APA Citation', command=copy_apa)
    mla_button.grid(row = 6, column = 2)
    mla_button = tk.Button(root, text='Copy Chicago Citation', command=copy_chicago)
    mla_button.grid(row = 7, column = 2)
    mla_button = tk.Button(root, text='Copy IEEE Citation', command=copy_ieee)
    mla_button.grid(row = 8, column = 2)
    mla_button = tk.Button(root, text='Copy StatsCan Citation', command=copy_statscan)
    mla_button.grid(row = 9, column = 2)
    
    
    #Notes and help and the like
    #
    expand_label = tk.Label(root, text='EXPAND WINDOW FOR TIPS ->')
    expand_label.grid(row = 2, column = 3)
    tips_label = tk.Label(root, text="TIPS:\nOnce all your citations are in your document, use the following tricks to indent all sources: \n"+
                               "Microsoft Word: With all sources highlighted, press: Ctrl + T \n"+
                               "Google Docs: With all sources highlighted, click on: Format > Align & Indent > Indentation Options > Special Indent > Hanging > Apply")
    tips_label.grid(row = 1, column = 4)
    
    disclaimer_label = tk.Label(root, text='\nDISCLAIMER: I don\'t guarantee the\nvalidity of any citation.\nI\'m just a robot. Caveat emptor.')
    disclaimer_label.grid(row = 10, column = 2)
    
    #credit, please
    #
    credit_label=tk.Label(root, text='\n\n\n         Code and App. by\n         Russell Abraira')
    credit_label.grid(row=10, column = 3)
    
    
    root.mainloop()

if __name__ == '__main__':
    main()


























    
