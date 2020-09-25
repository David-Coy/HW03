# withing iPython do the following as an examples in the workingdirectory
# import NIST_Data
# NIST_Data.NIST_Props.interp_props('Helium',70.0001,1.5,'Density','C', 'MPa', 'kg/m3')
import sys
from bs4 import BeautifulSoup
import requests #https://www.dataquest.io/blog/web-scraping-tutorial-python/
import pandas as pd
import pdb
from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg") #For whatever reason, this needs to be imported after matplotlib but before pyplot
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import csv
import time
import matplotlib.animation as animation
from importlib import reload
import tkinter, re, pyfiglet, os
from selenium import webdriver
import argparse
from IPython import display
import plotly.graph_objects as go
from mpl_toolkits.mplot3d import Axes3D 

pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_columns',9,'max_rows',2000,'display.max_colwidth',400)

#parser = argparse.ArgumentParser(description=str(print(pyfiglet.figlet_format("NIST Data! ", font='standard'))), epilog='IDKLOL',usage='Accepts a range of Magnification values to ouput a Pandas DataFrame of usefully formated data for comparison with using different camera systems')    
#args = parser.parse_args()
ascii_error_banner = pyfiglet.figlet_format("RANGE ERROR ", font='standard')

unit_dict_url={'K':'K', 'C':'C', 'F':'F', 'R':'R',
'MPa':'MPa', 'bar':'bar', 'atm':'atm', 'torr':'torr', 'psia':'psia',
'mol/l':'mol%2Fl', 'mol/m3':'mol%2Fm3' ,'g/ml':'g%2Fml', 'kg/m3':'kg%2Fm3', 'lb-mole/ft3':'lb-mole%2Fft3', 'lbm/ft3':'lbm%2Fft3' ,
'kJ/mol':'kJ%2Fmol', 'kJ/kg':'kJ%2Fkg', 'kcal/mol':'kcal%2Fmol', 'Btu/lb-mole':'Btu%2Flb-mole', 'kcal/g':'kcal%2Fg', 'Btu/lbm':'Btu%2Flbm',
'm/s':'m%2Fs', 'ft/s':'ft%2Fs', 'mph':'mph',
'µPa*s':'uPa*s', 'Pa*s':'Pa*s', 'cP':'cP', 'lbm/ft*s':'lbm%2Fft*s',
'N/m':'N%2Fm', 'dyn/cm':'dyn%2Fcm', 'lb/ft':'lb%2Fft', 'lb/in':'lb%2Fin',
}

ID_dic={
        'Water':'C7732185',                                    'H20':'C7732185',
        'Nitrogen':'C7727379',                                 'N':'C7727379',
        'Hydrogen':'C1333740',                                 'H':'C1333740',
        'Parahydrogen':'B5000001',                             'H2':'B5000001',
        'Deuterium':'C7782390',                                'D':'C7782390', '2H':'C7782390','Hydrogen-2':'C7782390',
        'Oxygen':'C7782447',                                   'O':'C7782447',
        'Flourine':'C7782414',                                 'F':'C7782414',
        'Carbon monoxide':'C630080',                           'CO':'C630080',
        'Carbon dioxide':'C124389',                            'CO2':'C124389',
        'Dinitrogen monoxide':'C10024972',                     'N2O':'C10024972',
        'Deuterium oxide':'C7789200',                          'D2O':'C7789200',
        'Methanol':'C67561',                                   'CH3OH':'C67561', 'CH4O':'C67561',
        'Methane':'C74828',                                    'CH4':'C74828',
        'Ethane':'C74840',                                     'C2H6':'C74840',
        'Ethene':'C74851',                                     'Ethylene':'C74851', 'C2H4':'C74851',
        'Propane':'C74986',                                    'C3H8':'C74986',
        'Propene':'C115071',                                   'C3H6':'C115071',
        'Propyne':'C74997',                                    'C3H4':'C74997',
        'Cyclopropane':'C75194',                               'C3H6':'C75194',
        'Isobutane':'C75285',                                  'C4H10':'C75285',
        'Pentane':'C109660',                                   'C5H10':'C109660',
        '2-Methylbutane':'C78784',                        
        '2,2-Dimethylpropane':'C463821',
        'Hexane':'C110543',
        '2-Methylpentane':'C107835',
        'Cyclohexane':'C110827',
        'Heptane':'C142825',
        'Octane':'C111659',
        'Nonane':'C111842',
        'Decane':'C124185',
        'Dodecane':'C112403',
        'Helium':'C7440597',
        'Neon':'C7440019',
        'Argon':'C7440371',
        'Krypton':'C7439909',
        'Xenon':'C7440633',
        'Ammonia':'C7664417',
        'Nitrogen trifluoride':'C7783542',
        'Trichlorofluoromethane (R11)':'C75694',
        'Dichlorodifluoromethane (R12)':'C75718',
        'Chlorotrifluoromethane (R13)':'C75729',
        'Tetrafluoromethane (R14)':'C75730',
        'Dichlorofluoromethane (R21)':'C75434',
        'Methane, chlorodifluoro- (R22)':'C75456',
        'Trifluoromethane (R23)':'C75467',
        'Methane, difluoro- (R32)':'C75105',
        'Fluoromethane (R41)':'C593533',
        '1,1,2-Trichloro-1,2,2-trifluoroethane (R113)':'C76131',
        '1,2-Dichloro-1,1,2,2-tetrafluoroethane (R114)':'C76142',
        'Chloropentafluoroethane (R115)':'C76153',
        'Hexafluoroethane (R116)':'C76164',
        'Ethane, 2,2-dichloro-1,1,1-trifluoro- (R123)':'C306832',
        'Ethane, 1-chloro-1,2,2,2-tetrafluoro- (R124)':'C2837890',
        'Ethane, pentafluoro- (R125)':'C354336',
        'Ethane, 1,1,1,2-tetrafluoro- (R134a)':'C811972',
        '1,1-Dichloro-1-fluoroethane (R141b)':'C1717006',
        '1-Chloro-1,1-difluoroethane (R142b)':'C75683',
        'Ethane, 1,1,1-trifluoro- (R143a)':'C420462',
        'Ethane, 1,1-difluoro- (R152a)':'C75376',
        'Octafluoropropane (R218)':'C76197',
        '1,1,1,2,3,3,3-Heptafluoropropane (R227ea)':'C431890',
        '1,1,1,2,3,3-Hexafluoropropane (R236ea)':'C431630',
        '1,1,1,3,3,3-Hexafluoropropane (R236fa)':'C690391',
        '1,1,2,2,3-Pentafluoropropane (R245ca)':'C679867',
        '1,1,1,3,3-Pentafluoropropane (R245fa)':'C460731',
        'Octafluorocyclobutane (RC318)':'C115253',
        'Benzene':'C71432',
        'Toluene':'C108883',
        'Decafluorobutane':'C355259',                                                        
        'Dodecafluoropentane':'C678262',
        'Sulfur dioxide':'C7446095',  
        'Hydrogen sulfide':'C7783064',
        'Sulfur hexafluoride':'C2551624',   
        'Carbonyl sulfide':'C463581',                                
        }    
class NIST_Props():
    #The below text is an example of what could be pasted into iPython3
    def scrape_IsoTherm(chrome=False, ID=['Water',
    'Nitrogen',
    'Hydrogen',
    'Parahydrogen',
    'Deuterium',
    'Oxygen',
    'Flourine',
    'Carbon monoxide',
    'Carbon dioxide',      
    'Dinitrogen monoxide', 
    'Deuterium oxide', 
    'Methanol',
    'Methane',
    'Ethane',     
    'Ethene',
    'Propane',                       
    'Propene',                 
    'Propyne',          
    'Cyclopropane',                             
    'Isobutane',                          
    'Pentane',                            
    '2-Methylbutane',                        
    '2,2-Dimethylpropane',
    'Hexane',
    '2-Methylpentane',
    'Cyclohexane',
    'Heptane',
    'Octane',
    'Nonane',
    'Decane',
    'Dodecane',
    'Helium',
    'Neon',
    'Argon',
    'Krypton',
    'Xenon',
    'Ammonia',
    'Nitrogen trifluoride',
    'Trichlorofluoromethane (R11)',
    'Dichlorodifluoromethane (R12)',
    'Chlorotrifluoromethane (R13)',
    'Tetrafluoromethane (R14)',
    'Dichlorofluoromethane (R21)',
    'Methane, chlorodifluoro- (R22)',
    'Trifluoromethane (R23)',
    'Methane, difluoro- (R32)',
    'Fluoromethane (R41)',
    '1,1,2-Trichloro-1,2,2-trifluoroethane (R113)',
    '1,2-Dichloro-1,1,2,2-tetrafluoroethane (R114)',
    'Chloropentafluoroethane (R115)',
    'Hexafluoroethane (R116)',
    'Ethane, 2,2-dichloro-1,1,1-trifluoro- (R123)',
    'Ethane, 1-chloro-1,2,2,2-tetrafluoro- (R124)',
    'Ethane, pentafluoro- (R125)',
    'Ethane, 1,1,1,2-tetrafluoro- (R134a)',
    '1,1-Dichloro-1-fluoroethane (R141b)',
    '1-Chloro-1,1-difluoroethane (R142b)',
    'Ethane, 1,1,1-trifluoro- (R143a)',
    'Ethane, 1,1-difluoro- (R152a)',
    'Octafluoropropane (R218)',
    '1,1,1,2,3,3,3-Heptafluoropropane (R227ea)',
    '1,1,1,2,3,3-Hexafluoropropane (R236ea)',
    '1,1,1,3,3,3-Hexafluoropropane (R236fa)',
    '1,1,2,2,3-Pentafluoropropane (R245ca)',
    '1,1,1,3,3-Pentafluoropropane (R245fa)',
    'Octafluorocyclobutane (RC318)',
    'Benzene',
    'Toluene',
    'Decafluorobutane',                                                        
    'Dodecafluoropentane',
    'Sulfur dioxide',  
    'Hydrogen sulfide',
    'Sulfur hexafluoride',   
    'Carbonyl sulfide'],
    Type='IsoTherm', #Type = IsoTherm (do not bother changing)
    Digits=6, #Digits = Number of digits to be displayed in tables (does not effect accuracy of computations)
    PLow=0.0001, #PLow = Pressure Low range
    PHigh=3000, #PHigh = Pressure High range
    PInc=5, #PInc =  Pressure Increments between PHigh and Plow
    T=list(range(0,2000,5)), #T= Temperature scope : [100,200,500,1000] or use list(range(start,stop, Increment))
    RefState='DEF&TUnit', #RefState=DEF&TUnit
    TUnit='F', #TUnit = Temperatures Units: K,C,F,R
    PUnit='MPa', #PUnit = Pressure Units: MPa  bar  atm.  torr  psia
    DUnit='kg/m3', #DUnit = Density Units: mol/l  mol/m3  g/ml  kg/m3  lb-mole/ft3  lbm/ft3
    HUnit='kJ/kg', #HUnit = Energy Units: kJ/mol  kJ/kg  kcal/mol  Btu/lb-mole  kcal/g  Btu/lbm
    WUnit='m/s', #WUnit = Velocity Units: m/s  ft/s  mph
    VisUnit='µPa*s', #VisUnit =Viscosity Units: µPa*s  Pa*s  cP  lbm/ft*s
    STUnit='N/m'): #STUnit = Surface Tension Units: N/m  dyn/cm  lb/ft  lb/in)
        '''
        IDKLOL##########
        #######################################
        '''
        if chrome:
            driver = webdriver.Chrome(executable_path='./chromedriver')
            options = webdriver.ChromeOptions()
            options.add_argument("headless")
        
        data_path = "./data_"+Type
        access_rights = 0o755
        try:
            os.mkdir(data_path, access_rights)
        except OSError:
            print ("Creation of the directory %s failed" % data_path)
        else:
            print ("Successfully created the directory %s" % data_path)

        for gas in ID:
            writer=pd.ExcelWriter('./data/NIST_Fluid_Prop_'+gas+'.xlsx')
            for temp in T:
                    #pdb.set_trace()
                    time.sleep(float(np.random.rand(1)*2))
                    url = "https://webbook.nist.gov/cgi/fluid.cgi?Action=Data&Wide=on&ID="+ID_dic[gas]+"&Type="+Type+"&Digits="+str(Digits)+"&PLow="+str(PLow)+"&PHigh="+str(PHigh)+"&PInc="+str(PInc)+"&T="+str(temp)+"&RefState=DEF&TUnit=C&PUnit="+PUnit+"&DUnit=kg%2Fm3&HUnit=kJ%2Fmol&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm"
                    #pdb.set_trace()
                    page = requests.get(url)
                    if chrome:
                        driver.get(url)
                    
                    if re.findall('Error',page.text, re.I):
                        print('\n'+('#'*80))
                        print(ascii_error_banner)
                        print(('#'*80)+'\n') 
                    else:
                        reader_list = csv.DictReader(page.text)
                        soup = BeautifulSoup(page.content, 'html.parser')
                        print(soup.prettify())
                        soup_str=soup.prettify()
                        soup_str=soup_str.split('\n')
                        headers=np.asarray(soup_str[0].split('\t'))
                        Matrix=headers
                        for i in range(1,len(soup_str)-1):
                            N=np.array(soup_str[i].split('\t'))
                            Matrix=np.vstack((Matrix,N))
                        df=pd.DataFrame(Matrix,index=Matrix[:,0])
                        df=df.reset_index(drop=True)
                        new_header=df.iloc[0] # Grab the first row of the header
                        df=df[1:] # Take the data less than the header row
                        df.columns=new_header
                        print('#'*80)
                        print(url)
                        print(' ')
                        print(gas)
                        print('#'*80)
                        print(df)
                        df.to_excel(writer,'Props_'+str(temp)+TUnit)
            writer.save()
################################################################################
    def scrape_IsoBar(chrome=False, ID=['Water'],
    Type='IsoBar', #Type = IsoTherm (do not bother changing)
    Digits=6, #Digits = Number of digits to be displayed in tables (does not effect accuracy of computations)
    P=list(range(0,2100,100)), #PLow = Pressure Low range
    TLow=10, #T= Temperature scope : [100,200,500,1000] or use list(range(start,stop, Increment))
    THigh=3010, #T= Temperature scope : [100,200,500,1000] or use list(range(start,stop, Increment))
    TInc=50, #T= Temperature scope : [100,200,500,1000] or use list(range(start,stop, Increment))    
    RefState='DEF&TUnit', #RefState=DEF&TUnit
    TUnit='F', #TUnit = Temperatures Units: K,C,F,R
    PUnit='psia', #PUnit = Pressure Units: MPa  bar  atm  torr  psia
    DUnit='kg/m3', #DUnit = Density Units: mol/l  mol/m3  g/ml  kg/m3  lb-mole/ft3  lbm/ft3
    HUnit='kJ/kg', #HUnit = Energy Units: kJ/mol  kJ/kg  kcal/mol  Btu/lb-mole  kcal/g  Btu/lbm
    WUnit='m/s', #WUnit = Velocity Units: m/s  ft/s  mph
    VisUnit='µPa*s', #VisUnit =Viscosity Units: µPa*s  Pa*s  cP  lbm/ft*s
    STUnit='N/m'): #STUnit = Surface Tension Units: N/m  dyn/cm  lb/ft  lb/in)
    #https://webbook.nist.gov/cgi/fluid.cgi?Action=Data&Wide=on&ID=C7732185&Type=IsoBar&Digits=6&P=100&THigh=1000&TLow=100&TInc=100&RefState=DEF&TUnit=F&PUnit=psia&DUnit=kg%2Fm3&HUnit=kJ%2Fkg&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm
        if chrome:
            driver = webdriver.Chrome(executable_path='./chromedriver')
            options = webdriver.ChromeOptions()
            options.add_argument("headless")
        
        data_path = "./data/"+Type
        access_rights = 0o755
        try:
            os.makedirs(data_path, access_rights)
        except OSError:
            print ("Creation of the directory %s failed" % data_path)
        else:
            print ("Successfully created the directory %s" % data_path)
        
        for gas in ID:
            writer=pd.ExcelWriter(data_path+'/NIST_Fluid_Prop_'+gas+'.xlsx')
            df_csv=pd.DataFrame()
            for press in P:
                    time.sleep(np.random.rand(1)*2)                    
                    url =  "https://webbook.nist.gov/cgi/fluid.cgi?Action=Data&Wide=on&ID="+ID_dic[gas] \
                            +"&Type="+Type \
                            +"&Digits="+str(Digits) \
                            +"&P="+str(press) \
                            +"&THigh="+str(THigh) \
                            +"&TLow="+str(TLow) \
                            +"&TInc="+str(TInc) \
                            +"&RefState=DEF&TUnit="+unit_dict_url[TUnit] \
                            +"&PUnit="+unit_dict_url[PUnit] \
                            +"&DUnit="+unit_dict_url[DUnit] \
                            +"&HUnit="+unit_dict_url[HUnit] \
                            +"&WUnit="+unit_dict_url[WUnit] \
                            +"&VisUnit="+unit_dict_url[VisUnit] \
                            +"&STUnit="+unit_dict_url[STUnit]
                    #unit_dict_url
                    page = requests.get(url)
                    if chrome:
                        driver.get(url)
                    
                    if re.findall('Error',page.text, re.I):
                        print('\n'+('#'*80))
                        print(ascii_error_banner)
                        print(('#'*80)+'\n') 
                    else:
                        reader_list = csv.DictReader(page.text)
                        soup = BeautifulSoup(page.content, 'html.parser')
                        print(soup.prettify())
                        soup_str=soup.prettify()
                        soup_str=soup_str.split('\n')
                        headers=np.asarray(soup_str[0].split('\t'))
                        Matrix=headers
                        for i in range(1,len(soup_str)-1):
                            N=np.array(soup_str[i].split('\t'))
                            Matrix=np.vstack((Matrix,N))
                        df=pd.DataFrame(Matrix,index=Matrix[:,0])
                        df=df.reset_index(drop=True)
                        new_header=df.iloc[0] # Grab the first row of the header
                        df=df[1:] # Take the data less than the header row
                        df.columns=new_header
                        print('#'*80)
                        print(url)
                        print(' ')
                        print(gas)
                        print('#'*80)
                        print(df)
                        df.to_excel(writer,'Props_'+str(press)+PUnit, index=False)
                        df_csv=df_csv.append(df)
                         
            writer.save()
            df_csv.to_csv(data_path+'/NIST_Fluid_Prop_'+gas+'.csv', index = False)
        #pdb.set_trace()
        print('Done Scraping! '*10)
################################################################################
    def read_props(type='IsoBar',fluid='Water', file_type='csv'):
        if file_type == 'csv':
            df = pd.read_csv('./data/'+type+'/NIST_Fluid_Prop_'+fluid+'.'+file_type)    
        
        elif file_type == 'xlsx':
            OrderedDict=pd.read_excel('./data/'+type+'/NIST_Fluid_Prop_'+fluid+'.xlsx', sheet_name=None)
            sorted_sheet_list = sorted(list(OrderedDict))
            df=pd.DataFrame()
            for i in sorted_sheet_list:
                df = df.append(OrderedDict[i])
        #pdb.set_trace()
        return df
################################################################################
    def plots(df,press=list(range(10,200,100))):
        from mpl_toolkits.mplot3d import Axes3D 
        from matplotlib import cm
        def f(X, Y):
            return np.sin(np.sqrt(X ** 2 + Y ** 2))
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        fig.show()
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        for p in press:
            df_p=df.loc[df['Pressure (psia)'] == p]
            x=df_p['Entropy (J/g*K)'].values  
            y=df_p['Temperature (F)'].values
            #X=np.array(list(zip(X,Y)))
            #Y=np.array(list(zip(X,Y)))
            X,Y = np.meshgrid(x,y)
            #Z=df_p['Density (kg/m3)'].values
            Z=f(X,Y)
            #fig.add_trace(go.Scatter(X, Y,mode='lines',name='lines'))
            #plt.plot(X,Y,Z)
            #plt.scatter(X,Y)
            cset = ax.contour(X, Y, Z, 50,cmap=cm.coolwarm)
            ax.clabel(cset, fontsize=9, inline=1)
            plt.draw()
            plt.pause(0.001)
            #plt.clf()
            #fig.canvas.draw()
        #fig.canvas.flush_events()
        #pdb.set_trace()
################################################################################
    def interp_props(ID,T,P,Prop,TUnit, PUnit, YUnit):
        #help(NIST_Data.NIST_Props.interp_props
        '''
        Double interpolates off of excel files
        
        Parameters
        ----------
        ID : string
             NIST fluid name:
                 'Water',
                 'Nitrogen',
                 'Hydrogen',
                 'Parahydrogen',
                 'Deuterium',
                 'Oxygen',
                 'Flourine',
                 'Carbon monoxide',
                 'Carbon dioxide',      
                 'Dinitrogen monoxide', 
                 'Deuterium oxide', 
             
        T  : float
            Temperature of interest `T` (K,C,F,R)
        P  : float
            Pressure of interest
        Prop : string
            Property to be calculated 
            density
        TUnit : string
            Temperature units `TUnit` (K,C,F,R)
        PUnit : string
            Pressure units `PUnit` (MPa,bar,atm.,torr,psia)
        YUnit : string
            Units of dependent variable to be calculated ('kg/m3')
        
        '''
        # import NIST_Data
        # NIST_Data.NIST_Props.interp_props('Helium',70.0001,1.5,'Density','C', 'MPa', 'kg/m3')
        def make_patch_spines_invisible(ax):
            ax.set_frame_on(True)
            ax.patch.set_visible(False)
            for sp in ax.spines.values():
                sp.set_visible(False)

        
        workbook_name='./data/NIST_Fluid_Prop_'+ID+'.xlsx'
        df1=pd.read_excel(workbook_name, sheet_name=0)
        xl = pd.ExcelFile(workbook_name)
        temps=[]
        for i in xl.sheet_names:
            temps.append(pd.read_excel(workbook_name, sheet_name=i)['Temperature (C)'].values[0])
        temps=sorted(temps)
        #if T in temps: #Check to too see if the desired temp is exactly the same as one listed in the DataFrame
        if T in temps:
            name=ID+'_Properties_'+str(T)+TUnit
            df=pd.read_excel(workbook_name, sheet_name=name)
            
            if P>0:
                y_1=df[df['Pressure (' + PUnit + ')'].gt(P)].head(1)[Prop +' (' + YUnit + ')'].values[0]# Upper Y Value
                y_0=df[df['Pressure (' + PUnit + ')'].lt(P)].tail(1)[Prop +' (' + YUnit + ')'].values[0]# Lower Y Values
                x=P # Current exact pressure
                x_1=df[df['Pressure (' + PUnit + ')'].gt(P)].head(1)['Pressure (' + PUnit + ')'].values[0]# Upper Pressure
                x_0=df[df['Pressure (' + PUnit + ')'].lt(P)].tail(1)['Pressure (' + PUnit + ')'].values[0]# Lower Pressure
                y=y_0+(x-x_0)*((y_1-y_0)/(x_1-x_0))# Linearly interpolated Density
        
        if T not in temps:
            #https://www.youtube.com/watch?v=fP_h-iQckqo
            T_l=list(filter(lambda h: h < T, temps))[-1]
            name_l=ID+'_Properties_'+str(int(T_l))+TUnit
            T_h=list(filter(lambda h: h > T, temps))[0]
            name_h=ID+'_Properties_'+str(int(T_h))+TUnit
            
            
            df_l=pd.read_excel(workbook_name, sheet_name=name_l)
            df_h=pd.read_excel(workbook_name, sheet_name=name_h)

            Y_l_at_T_l=df_l[df_l['Pressure (' + PUnit + ')'].gt(P)].head(1)[Prop +' (' + YUnit + ')'].values[0]# Lower Y Value at T_l
            Y_h_at_T_l=df_l[df_l['Pressure (' + PUnit + ')'].lt(P)].tail(1)[Prop +' (' + YUnit + ')'].values[0]# Upper Y Value at T_l
            P_l_at_T_l=df_l[df_l['Pressure (' + PUnit + ')'].lt(P)].tail(1)['Pressure (' + PUnit + ')'].values[0]# Lower Pressure at T_l
            P_h_at_T_l=df_l[df_l['Pressure (' + PUnit + ')'].gt(P)].head(1)['Pressure (' + PUnit + ')'].values[0]# Upper Pressure at T_l

            Y_l_at_T_h=df_h[df_h['Pressure (' + PUnit + ')'].gt(P)].head(1)[Prop +' (' + YUnit + ')'].values[0]# Lower Y Value at T_h
            Y_h_at_T_h=df_h[df_h['Pressure (' + PUnit + ')'].lt(P)].tail(1)[Prop +' (' + YUnit + ')'].values[0]# Upper Y Value at T_h
            P_l_at_T_h=df_h[df_h['Pressure (' + PUnit + ')'].lt(P)].tail(1)['Pressure (' + PUnit + ')'].values[0]# Lower Pressure at T_l
            P_h_at_T_h=df_h[df_h['Pressure (' + PUnit + ')'].gt(P)].head(1)['Pressure (' + PUnit + ')'].values[0]# Upper Pressure at T_l

            Y_at_T_l = Y_l_at_T_l+(P - P_l_at_T_l)*((Y_h_at_T_l - Y_l_at_T_l)/(P_h_at_T_l - P_l_at_T_l))# Y Value at T_l
            Y_at_T_h = Y_l_at_T_h+(P - P_l_at_T_h)*((Y_h_at_T_h - Y_l_at_T_h)/(P_h_at_T_h - P_l_at_T_h))# Y Value at T_h

            Y_at_T = Y_at_T_l+(T - T_l)*((Y_at_T_h - Y_at_T_l)/(T_h - T_l))# Y Value double interpolated at the T and P

        fig = plt.figure()
        fig.set_figheight(7)
        fig.set_figwidth(12)

        ax1 = fig.add_subplot(111)
        plt.gcf().subplots_adjust(left=0.25)

        ax1.set_title('title')
        ax1.set_ylim([df_l['Pressure ' + '(' + PUnit + ')'].values.min(), df_l['Pressure ' + '(' + PUnit + ')'].values.max()])
        ax1.set_xlim([df_l[Prop + ' (' + YUnit + ')'].values.min(),df_l[Prop + ' (' + YUnit + ')'].values.max()])
        ax1.set(ylabel='Pressure' + ' ('+PUnit+')')

        if PUnit=='MPa':
            ax1_b = ax1.twinx()# Create a new Axes instance with an invisible x-axis and an independent y-axis positioned opposite to the original one (i.e. at right).
            ax1_b.set(ylabel='Pressure (pisa)')# set second y-axis label
            ax1_b.set_ylim([df_l['Pressure ' + '(' + PUnit + ')'].values.min()*145.038, df_l['Pressure ' + '(' + PUnit + ')'].values.max()*145.038])
            ax1_b.spines["left"].set_position(("axes", -0.1)) #Spines are the lines connecting the axis tick marks and noting the boundaries of the data area.
            ax1_b.spines["left"].set_visible(True)
            ax1_b.yaxis.set_label_position('left')
            ax1_b.yaxis.set_ticks_position('left')

            ax1_c = ax1.twinx()# Create a new Axes instance with an invisible x-axis and an independent y-axis positioned opposite to the original one (i.e. at right).
            ax1_c.set(ylabel='Pressure (Inches H2O)')# set second y-axis label
            ax1_c.set_ylim([df_l['Pressure ' + '(' + PUnit + ')'].values.min()*4018.65, df_l['Pressure ' + '(' + PUnit + ')'].values.max()*4018.65])
            ax1_c.spines["left"].set_position(("axes", -0.2)) #Spines are the lines connecting the axis tick marks and noting the boundaries of the data area.
            ax1_c.spines["left"].set_visible(True)
            ax1_c.yaxis.set_label_position('left')
            ax1_c.yaxis.set_ticks_position('left')
        df_l.plot(Prop + ' (' + YUnit + ')','Pressure ' + '(' + PUnit + ')',ax=ax1,label='T_high Table Data')
        df_h.plot(Prop + ' (' + YUnit + ')','Pressure ' + '(' + PUnit + ')',ax=ax1,label='T_low Table Data')
        ax1.scatter(Y_at_T, P, s=100, marker='o', color='blue')
        ax1.plot([Y_at_T,Y_at_T],[0,P], color='black', linestyle='--')
        ax1.plot([0,Y_at_T],[P,P], color='black', linestyle='--')
        ax1.grid(True)
        ax1.grid(which='major', linestyle='-', linewidth=.5, color='grey')
        ax1.minorticks_on()
        ax1.grid(which='minor', linestyle='-', linewidth=.1, color='grey')
        
        plt.show()
        print('At temperature ' + str(T) + ' ' + TUnit + ' and pressure ' + str(P) + ' ' + PUnit  + ' The ' + Prop +' is: '  + str(Y_at_T)+' ' + '('+YUnit+')' )
        return Y_at_T


#EXAMPLE
'''

NIST_Data.NIST_Props.scrape2spreadsheet(ID=['Water',
'Nitrogen',
'Hydrogen',
'Parahydrogen',
'Deuterium',
'Oxygen',
'Flourine',
'Carbon monoxide',
'Carbon dioxide',      
'Dinitrogen monoxide', 
'Deuterium oxide', 
'Methanol',
'Methane',
'Ethane',     
'Ethene',
'Propane',                       
'Propene',                 
'Propyne',          
'Cyclopropane',                             
'Isobutane',                          
'Pentane',                            
'2-Methylbutane',                        
'2,2-Dimethylpropane',
'Hexane',
'2-Methylpentane',
'Cyclohexane',
'Heptane',
'Octane',
'Nonane',
'Decane',
'Dodecane',
'Helium',
'Neon',
'Argon',
'Krypton',
'Xenon',
'Ammonia',
'Nitrogen trifluoride',
'Trichlorofluoromethane (R11)',
'Dichlorodifluoromethane (R12)',
'Chlorotrifluoromethane (R13)',
'Tetrafluoromethane (R14)',
'Dichlorofluoromethane (R21)',
'Methane, chlorodifluoro- (R22)',
'Trifluoromethane (R23)',
'Methane, difluoro- (R32)',
'Fluoromethane (R41)',
'1,1,2-Trichloro-1,2,2-trifluoroethane (R113)',
'1,2-Dichloro-1,1,2,2-tetrafluoroethane (R114)',
'Chloropentafluoroethane (R115)',
'Hexafluoroethane (R116)',
'Ethane, 2,2-dichloro-1,1,1-trifluoro- (R123)',
'Ethane, 1-chloro-1,2,2,2-tetrafluoro- (R124)',
'Ethane, pentafluoro- (R125)',
'Ethane, 1,1,1,2-tetrafluoro- (R134a)',
'1,1-Dichloro-1-fluoroethane (R141b)',
'1-Chloro-1,1-difluoroethane (R142b)',
'Ethane, 1,1,1-trifluoro- (R143a)',
'Ethane, 1,1-difluoro- (R152a)',
'Octafluoropropane (R218)',
'1,1,1,2,3,3,3-Heptafluoropropane (R227ea)',
'1,1,1,2,3,3-Hexafluoropropane (R236ea)',
'1,1,1,3,3,3-Hexafluoropropane (R236fa)',
'1,1,2,2,3-Pentafluoropropane (R245ca)',
'1,1,1,3,3-Pentafluoropropane (R245fa)',
'Octafluorocyclobutane (RC318)',
'Benzene',
'Toluene',
'Decafluorobutane',                                                        
'Dodecafluoropentane',
'Sulfur dioxide',  
'Hydrogen sulfide',
'Sulfur hexafluoride',   
'Carbonyl sulfide'],
Type='IsoTherm', #Type = IsoTherm (do not bother changing)
Digits=5, #Digits = Number of digits to be displayed in tables (does not effect accuracy of computations)
PLow=900, #PLow = Pressure Low range
PHigh=1100, #PHigh = Pressure High range
PInc=10, #PInc =  Pressure Increments between PHigh and Plow
T=list(range(0,1000,50)), #T= Temperature scope : [100,200,500,1000] or use list(range(start,stop, Increment))
RefState='DEF&TUnit', #RefState=DEF&TUnit
TUnit='F', #TUnit = Temperatures Units: K,C,F,R
PUnit='psia', #PUnit = Pressure Units: MPa  bar  atm.  torr  psia
DUnit='kg/m3', #DUnit = Density Units: mol/l  mol/m3  g/ml  kg/m3  lb-mole/ft3  lbm/ft3
HUnit='kJ/kg', #HUnit = Energy Units: kJ/mol  kJ/kg  kcal/mol  Btu/lb-mole  kcal/g  Btu/lbm
WUnit='m/s', #WUnit = Velocity Units: m/s  ft/s  mph
VisUnit='µPa*s', #VisUnit =Viscosity Units: µPa*s  Pa*s  cP  lbm/ft*s
STUnit='N/m') #STUnit = Surface Tension Units: N/m  dyn/cm  lb/ft  lb/in

'''


#QUICK EXAMPLE that can be run in iPython
'''
import NIST_Data_3_2_2020; NIST_Data_3_2_2020.NIST_Props.scrape_IsoTherm(ID=['Water',
'Nitrogen',
'Hydrogen',
'Deuterium',
'Oxygen',
'Flourine',
'Methanol',
'Methane'],
Type='IsoTherm', #Type = IsoTherm (do not bother changing)
Digits=5, #Digits = Number of digits to be displayed in tables (does not effect accuracy of computations)
PLow=900, #PLow = Pressure Low range
PHigh=1100, #PHigh = Pressure High range
PInc=10, #PInc =  Pressure Increments between PHigh and Plow
T=list(range(0,1000,50)), #T= Temperature scope : [100,200,500,1000] or use list(range(start,stop, Increment))
RefState='DEF&TUnit', #RefState=DEF&TUnit
TUnit='F', #TUnit = Temperatures Units: K,C,F,R
PUnit='psia', #PUnit = Pressure Units: MPa  bar  atm.  torr  psia
DUnit='kg/m3', #DUnit = Density Units: mol/l  mol/m3  g/ml  kg/m3  lb-mole/ft3  lbm/ft3
HUnit='kJ/kg', #HUnit = Energy Units: kJ/mol  kJ/kg  kcal/mol  Btu/lb-mole  kcal/g  Btu/lbm
WUnit='m/s', #WUnit = Velocity Units: m/s  ft/s  mph
VisUnit='µPa*s', #VisUnit =Viscosity Units: µPa*s  Pa*s  cP  lbm/ft*s
STUnit='N/m') #STUnit = Surface Tension Units: N/m  dyn/cm  lb/ft  lb/in
'''



'''
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt 
df1=df
df2=df.loc[df['Temperature (C)'] == 1000.0]

#fig = plt.figure()
#fig.set_figheight(7)
#fig.set_figwidth(12)
#ax1 = fig.add_subplot(111)
#plt.gcf().subplots_adjust(left=0.25)
#ax1.set_title('title')

df1.plot(x=df1.columns.values[2], y=df1.columns.values[3], style='o')
df2.plot(x=df2.columns.values[2], y=df2.columns.values[3], style='--',color='red')



dfa=df2[df2.columns.values[1]].values
dfb=df2[df2.columns.values[7]].values

dfc=df1[df1.columns.values[1]].values
dfd=df1[df1.columns.values[7]].values

plt.scatter(dfc, dfd, marker='o', color='blue')
plt.scatter(dfa, dfb, marker='o', color='red', linewidth=1)

plt.show()

'''

