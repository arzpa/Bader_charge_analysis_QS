import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


CuNi_N2_adsite3_folder_path = '/Users/parastooagharezaei/Downloads/4_bader_charge/6-CuNi-N2-adsite3/ACF.dat'
number_atoms = 66
#import the data in ACF.dat as it is
#For skip rows check in the file to see which lines you do not need in the file(the first and a few last line for example)
df_CuNiN2_adsite3 = pd.read_csv(CuNi_N2_adsite3_folder_path, 
                 sep="\s+", 
                 skiprows=[0,1,68,69,70,71],  
                 names=['#','x','y','z','Charge','Min_dist','atomic_volume'])
df_CuNiN2_adsite3.set_index('#', inplace=True)

#Make a atomic positions file by copying atomic coordinates in this RP-surface.in file (remember that you should not have any extra line other than as many atoms as you) 
atoms_df = pd.read_csv('/Users/parastooagharezaei/Downloads/4_bader_charge/6-CuNi-N2-adsite3/coordinate.in', 
                 sep="\s+",
                 names = ['atom','x','y','z'])
atoms_df.index = np.arange(1, len(atoms_df)+1)

#Appending atom_type column to the original_df
atom_types_column = atoms_df['atom']
df_CuNiN2_adsite3['atom_type'] = atom_types_column

#Cleaning the table
df_CuNiN2_adsite3 = df_CuNiN2_adsite3[['atom_type','x', 'y', 'z', 'Charge', 'Min_dist', 'atomic_volume']]

#Adding if each atom is surface atom or not
surface_atoms_index = [26,27,28,29,30,31,32,56,57,58,59,60,61,62,63,64] #the index list of surface_atoms
surface_column = list()
for i in range(1,number_atoms+1):
    surface_column.append(0)
df_CuNiN2_adsite3['surface_atom'] = surface_column
for index, row in df_CuNiN2_adsite3.iterrows():
    if index in surface_atoms_index:
        df_CuNiN2_adsite3.at[index,'surface_atom'] = 1

#bader_charge
full_shell_cu = 19 #zval (number of valence electrons in pseudopotential files)
full_shell_ni = 18 #zval (number of valence electrons in pseudopotential files)
full_shell_n2 = 5  #zval (number of valence electrons in pseudopotential files)
list_bader = list()
for i in range(1,number_atoms+1):
    if df_CuNiN2_adsite3.at[i,'atom_type'] == 'Cu':
        list_bader.append(full_shell_cu-float(df_CuNiN2_adsite3.at[i,'Charge']))
    elif df_CuNiN2_adsite3.at[i,'atom_type'] == 'Ni':
        list_bader.append(full_shell_ni-float(df_CuNiN2_adsite3.at[i,'Charge']))
    elif df_CuNiN2_adsite3.at[i,'atom_type'] == 'N':
        list_bader.append(full_shell_n2-float(df_CuNiN2_adsite3.at[i,'Charge']))
df_CuNiN2_adsite3['bader_charge'] = list_bader
df_CuNiN2_adsite3 = df_CuNiN2_adsite3[['atom_type', 'bader_charge', 'x', 'y', 'z', 'Charge', 'Min_dist', 'atomic_volume',
       'surface_atom']]

list_atom_type_number = list()
for i in range(1,number_atoms+1):
    list_atom_type_number.append('{0}_{1}'.format(df_CuNiN2_adsite3.at[i,'atom_type'],i))

df_CuNiN2_adsite3['type_number'] = list_atom_type_number
df_CuNiN2_adsite3 = df_CuNiN2_adsite3[['atom_type', 'type_number','bader_charge', 'x', 'y', 'z', 'Charge', 'Min_dist',
       'atomic_volume', 'surface_atom']]

#Saving the data
df_CuNiN2_adsite3.to_csv('/Users/parastooagharezaei/Downloads/4_bader_charge/6-CuNi-N2-adsite3/cleaned_CuNi_N2_adsite3.csv',index=True)

sns.set(font_scale = 1.5)
clrs = ['red','yellow','blue']
sns.barplot(x='atom_type',y='bader_charge',hue='surface_atom',data=df_CuNiN2_adsite3,palette=clrs)
#plt.legend(title='Charge', fontsize=20)
plt.xlabel('Atom type', fontsize=16);
plt.ylabel('bader charge', fontsize=16);
plt.title('Charge analysis', fontsize=20)
plt.tight_layout()
plt.savefig('/Users/parastooagharezaei/Downloads/4_bader_charge/6-CuNi-N2-adsite3/average_bader_charge.jpg',dpi=800)
plt.show()

sns.set(font_scale = 1.5)
clrs = ['orange','green','blue']
sns.barplot(x='atom_type',y='bader_charge',data=df_CuNiN2_adsite3,palette=clrs)
#plt.legend(title='Charge', fontsize=20)
plt.xlabel('Atom type', fontsize=16);
plt.ylabel('bader charge', fontsize=16);
plt.title('Charge analysis', fontsize=20)
plt.tight_layout()
plt.savefig('/Users/parastooagharezaei/Downloads/4_bader_charge/6-CuNi-N2-adsite3/total_bader_charge.jpg',dpi=800)
plt.show()


plt.figure(figsize = (15,8))
sns.set(font_scale = 1.5)
clrs = ['red','black']
b = sns.scatterplot(x='type_number',y='bader_charge',hue='surface_atom',data=df_CuNiN2_adsite3,palette=clrs)
b.set_xticklabels(df_CuNiN2_adsite3.type_number, size = 10,rotation=90)
#plt.legend(title='Charge', fontsize=20)
plt.xlabel('Atom_number', fontsize=20);
plt.ylabel('bader_charge', fontsize=16);
plt.title('Charge analysis', fontsize=20)
plt.tight_layout()
plt.savefig('/Users/parastooagharezaei/Downloads/4_bader_charge/6-CuNi-N2-adsite3/Bader_charge_atom_type.jpg',dpi=800)
plt.show()


#Digit report of average charges
#Average charges calculations
sub_surface_Cu = df_CuNiN2_adsite3[(df_CuNiN2_adsite3.surface_atom == 0)&(df_CuNiN2_adsite3.atom_type == 'Cu')][['bader_charge']].sum()/df_CuNiN2_adsite3[(df_CuNiN2_adsite3.surface_atom == 0)&(df_CuNiN2_adsite3.atom_type == 'Cu')][['bader_charge']].count()
surface_Cu = df_CuNiN2_adsite3[(Cdf_CuNiN2_adsite3.surface_atom == 1)&(df_CuNiN2_adsite3.atom_type == 'Cu')][['bader_charge']].sum()/df_CuNiN2_adsite3[(df_CuNiN2_adsite3.surface_atom == 1)&(df_CuNiN2_adsite3.atom_type == 'Cu')][['bader_charge']].count()
sub_surface_Ni = df_CuNiN2_adsite3[(df_CuNiN2_adsite3.surface_atom == 0)&(df_CuNiN2_adsite3.atom_type == 'Ni')][['bader_charge']].sum()/df_CuNiN2_adsite3[(df_CuNiN2_adsite3.surface_atom == 0)&(df_CuNiN2_adsite3.atom_type == 'Ni')][['bader_charge']].count()
surface_Ni = df_CuNiN2_adsite3[(df_CuNiN2_adsite3.surface_atom == 1)&(df_CuNiN2_adsite3.atom_type == 'Ni')][['bader_charge']].sum()/df_CuNiN2_adsite3[(df_CuNiN2_adsite3.surface_atom == 1)&(df_CuNiN2_adsite3.atom_type == 'Ni')][['bader_charge']].count()

Cu_charge = df_CuNiN2_adsite3[df_CuNiN2_adsite3.atom_type == 'Cu'][['bader_charge']].sum()/df_CuNiN2_adsite3[df_CuNiN2_adsite3.atom_type == 'Cu'][['bader_charge']].count()

Ni_charge = df_CuNiN2_adsite3[df_CuNiN2_adsite3.atom_type == 'Ni'][['bader_charge']].sum()/df_CuNiN2_adsite3[df_CuNiN2_adsite3.atom_type == 'Ni'][['bader_charge']].count()


print("""The average charges are as follow:\n
        sub_surface Cu atoms charge:{0},\n
        surface Cu atoms charge:{1},\n
        sub_surface Ni atoms charge:{2},\n
        surface Ni atoms charge:{3},\n
        average Cu atoms charge:{4},
        average Ni atoms charge: {5}""".format(sub_surface_Cu,surface_Cu,sub_surface_Ni,surface_Ni,Cu_charge,Ni_charge))

#Reading the datafile
pd.set_option('display.max_rows', None)
df_CuNiN2_adsite3 = pd.read_csv('/Users/parastooagharezaei/Downloads/4_bader_charge/1-Cu50Ni50/1-bader/cleaned_Cu50Ni50.csv')
df_CuNiN2_adsite3.set_index('#',inplace=True)








