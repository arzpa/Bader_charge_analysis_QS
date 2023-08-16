#In order to use the script you need the coordinate.in where you copy the coordinates file as Cu --- ---- ---- to a 
#separate file and another file as ACF_cleaned.csv where is a copy of ACF.dat file where you have removed the 
#only the atoms and their charges (remove the useless top two and last 4 lines.). Also in the dictionary
#named valence_electrons add new elements if any.
coordinate_df = pd.read_csv('./input.in',
                     sep="\s+",
                     names=['atom_type','x','y','z'])
coordinate_df.drop(['x','y','z'],axis=1,inplace=True)
coordinate_df

acf_df = pd.read_csv('./ACF.dat',
                     sep="\s+",
                     names=['#','x','y','z','Charge','Min_dist','atomic_volume'])
acf_df.drop('#',axis=1,inplace=True)
acf_df

acf_df['atom_type'] = coordinate_df['atom_type']
acf_df = acf_df[['atom_type','x', 'y', 'z', 'Charge', 'Min_dist', 'atomic_volume']]


# z_threshhold is the distance you want to keep from max(z) too include it as surface atom
z_threshhold = 1.0
acf_df['surface_atom'] = np.where(acf_df['z'] > max(acf_df['z'])- z_threshhold,1,0)

elements_list = list(acf_df['atom_type'].unique())

valence_electrons = {'Ag':('ag_pbe_v1.4.uspp.F.UPF',19.00000000000),
                   'Au':('au_pbe_v1.uspp.F.UPF',11.00000000000),
                   'Co':('co_pbe_v1.2.uspp.F.UPF',17.00000000000),
                   'Fe':('Fe.pbe-spn-kjpaw_psl.0.2.1.UPF',16.0000000000),
                   'Ru':('Ru_ONCV_PBE-1.0.oncvpsp.upf',16.0000000000),
                   'Pd':('pd_pbe_v1.4.uspp.F.UPF',16.0000000000),
                   'Pt':('pt_pbe_v1.4.uspp.F.UPF',16.0000000000),
                   'Cu':('cu_pbe_v1.2.uspp.F.UPF',19.00000000000),
                   'Ni':('ni_pbe_v1.4.uspp.F.UPF',18.00000000000)}

list_atom_type = list(acf_df['atom_type'])
bader_charge_list = [valence_electrons.get(i)[1] for i in list_atom_type]
acf_df['bader_charge'] = bader_charge_list - acf_df['Charge']

#Saving the data
acf_df.to_csv('./charge_df.csv')


#Lets plot the bader charge diagrams
sns.set(font_scale = 1.5)
clrs = ['red','yellow','blue']
sns.barplot(x='atom_type',y='bader_charge',hue='surface_atom',data=acf_df,palette=clrs)
#plt.legend(title='Charge', fontsize=20)
plt.xlabel('Atom type', fontsize=16);
plt.ylabel('bader charge', fontsize=16);
plt.title('Charge analysis', fontsize=20)
plt.tight_layout()
plt.savefig('./average_bader_charge.jpg',dpi=800)
plt.show()

sns.set(font_scale = 1.5)
clrs = ['orange','green','blue']
sns.barplot(x='atom_type',y='bader_charge',data=acf_df,palette=clrs)
#plt.legend(title='Charge', fontsize=20)
plt.xlabel('Atom type', fontsize=16);
plt.ylabel('bader charge', fontsize=16);
plt.title('Charge analysis', fontsize=20)
plt.tight_layout()
plt.savefig('./total_bader_charge.jpg',dpi=800)
plt.show()


plt.figure(figsize = (15,8))
sns.set(font_scale = 1.5)
clrs = ['red','black']
b = sns.scatterplot(x='atom_type',y='bader_charge',hue='surface_atom',data=acf_df,palette=clrs)
b.set_xticklabels(acf_df.atom_type, size = 10,rotation=90)
#plt.legend(title='Charge', fontsize=20)
plt.xlabel('Atom type', fontsize=20);
plt.ylabel('bader_charge', fontsize=16);
plt.title('Charge analysis', fontsize=20)
plt.tight_layout()
plt.savefig('./bader_charge_atom_type.jpg',dpi=800)
plt.show()

