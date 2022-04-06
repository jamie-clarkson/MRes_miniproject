# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 08:58:21 2022

@author: Jamie
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random

carbon_stored=pd.read_csv('carbon_stored.csv',encoding='cp1252')
carbon_flux=pd.read_csv('flux.csv',encoding='cp1252')
carbon_combined=pd.read_csv('carbon_combined.csv',encoding='cp1252')
habitats_distinctiveness=pd.read_csv('distinct_diff_time2.csv')


def biodiversity_calculator(post_intervention,size,distinctiveness,condition,strategic_location,connectivity,difficulty =0,time_to_target_condition=0,off_site_risk=0):
    """
    Parameters
    ----------
    post_intervention : Boolean
        if we are calculating the biodiversity units post intervention (True) or pre intervention (False). 
    size : float
        Habitat size in hectares.
    distinctiveness : float
        Distinctiveness value.
    condition : float
        condition value.
    strategic_location : float
        strategic location value.
    connectivity : float
        connectivity value.
    difficulty : float, optional
        DESCRIPTION. The default is 0. Difficulty value for post intervention habitat
    time_to_target_condition : float, optional
        DESCRIPTION. The default is 0. Time to target condition value for post intervention habitat
    off_site_risk : float, optional
        DESCRIPTION. The default is 0. Off site risk value for post intervention habitat

    Returns
    -------
    biodiversity_units : float
        DESCRIPTION. The biodiversity units

    """
    if post_intervention == False:
        biodiversity_units = size*distinctiveness*condition*strategic_location*connectivity   #formula for pre intervention biodiversity units
        return biodiversity_units
    if post_intervention == True:
        biodiversity_units = size*distinctiveness*condition*strategic_location*connectivity*difficulty*time_to_target_condition*off_site_risk   #formula for post intervention biodiversity units
        return biodiversity_units
        
def carbon_calculator(size,storage,flux,years = 30,post_intervention=False):
    """
    Parameters
    ----------
    size : float
        Habitat size in hectares.
    storage : float
        Carbon already stored in that habitat, in tonnes per hectare
    flux : float
        Carbon that will be removed over time, in tonnes per hectare per year
    years : float, optional
        The default is 30. Timescale over which to do removal calculation
    post_intervention : Boolean, optional
        The default is False. If we are calculating the carbon post intervention (True) or pre intervention (False). 
        
    Returns
    -------
    carbon_removed: float
        The caron stored over the time period

    """
    if post_intervention == False:
        carbon_removed = size*(storage - flux*years)   #I'm currently unsure whether to use the storage or not - probably should consider it for a pre intervention habitat but not post
    if post_intervention == True:
        carbon_removed = size*(0*storage - flux*years) 
    return carbon_removed    #positive is good



          
def evaluate_biodiversity_before(habitats_before):
    """
    Parameters
    ----------
    habitats_before : Dictionary
        the habitat values for the habitat pre intervention, as items in a dicitonary.

    Returns
    -------
    B0 : float
        biodiversity units for the habitat pre intervention.
    """
    B0 = 0
    for habitat_values_before in habitats_before:
        b0 = biodiversity_calculator(False, habitat_values_before['size'], habitat_values_before['distinctiveness'], habitat_values_before['condition'], habitat_values_before['strategic_location'], habitat_values_before['connectivity']) 
        B0 = B0 + b0
    return B0
      
def evaluate_biodiversity_after(habitats_after):
    """
    Parameters
    ----------
    habitats_after : Dictionary
        the habitat values for the habitat post intervention, as items in a dicitonary.
        
    Returns
    -------
    B1 : float
        biodiversity units for the habitat pre intervention.

    """
    B1 = 0
    for habitat_values_after in habitats_after:
        b1 = biodiversity_calculator(True, habitat_values_after['size'], habitat_values_after['distinctiveness'], habitat_values_after['condition'], habitat_values_after['strategic_location'], habitat_values_after['connectivity'],habitat_values_after['difficulty'],habitat_values_after['time_to_target_condition'],habitat_values_after['off_site_risk'])
        B1 = B1 + b1
    return B1

def evaluate_carbon_before(habitats_before):
    """
    Parameters
    ----------
    habitats_before : Dictionary
        the habitat values for the habitat pre intervention, as items in a dicitonary.

    Returns
    -------
    C0 : float
        carbon stored over 30 years if the same habitat continued to exist.

    """
    C0 = 0
    for habitat_values_before in habitats_before:
        c0 = carbon_calculator(habitat_values_before['size'],habitat_values_before['storage'],habitat_values_before['flux'],years = 30,post_intervention=False)
        C0 = C0 + c0
    return C0
        
def evaluate_carbon_after(habitats_after):
    """
    Parameters
    ----------
    habitats_after : Dictionary
        the habitat values for the habitat post intervention, as items in a dicitonary.

    Returns
    -------
    C1 : float
        carbon stored over 30 years with the new habitat.

    """
    C1 = 0
    for habitat_values_after in habitats_after:
        c1 = carbon_calculator(habitat_values_after['size'],habitat_values_after['storage'],habitat_values_after['flux'],years = 30,post_intervention=True)
        C1 = C1 + c1        
    return C1  
        
def generate_habitat_before():
    """
    Returns
    -------
    habitat_values : Dictionary
        Generates a random habitat, random size etc.

    """
    #pick a random from the habitat distinctiveness list
    distinctiveness_hab = habitats_distinctiveness.sample()  
    habitat = list(distinctiveness_hab['Habitat'])[0]
    carbon_hab = carbon_combined.loc[(carbon_combined['Habitat'] == habitat)].sample()                 
    habitat_name = habitat + ', ' + list(carbon_hab['Subtype'])[0] + ', ' +  list(distinctiveness_hab['Subtype'])[0]      
    
    storage = float(carbon_hab['Carbon stored (t C ha-1)'])
    flux = float(carbon_hab['Carbon flux (t CO2e ha-1 y-1 )'])
    distinctiveness = int(distinctiveness_hab['Distinctiveness_score'])
    
    condition = random.choice([3,2.5,2,1.5,1])
    strategic_location = random.choice([1.15,1.1,1])
    
    if distinctiveness >= 6:
        connectivity = 1.1
    else:
        connectivity = 1
      
    size = np.random.uniform(5,20)  #random size between 5 and 20 hectares

    
     
    habitat_values={
        'habitat_name':habitat_name,
        'Habitat':habitat,
        'Distinct_subtype':list(distinctiveness_hab['Subtype'])[0],
        'Carbon_subtype':list(carbon_hab['Subtype'])[0],
        'size':size,
        'storage':storage,
        'flux':flux,
        'distinctiveness':distinctiveness,
        'condition':condition, 
        'strategic_location':strategic_location, 
        'connectivity':connectivity, 
    }
    
    
    return habitat_values

global allowed_habitat_changes

""" dictionary of allowed new habitat types, for a given previous habitat type """
allowed_habitat_changes ={
    'Farmland':['Farmland','Woodland','Semi-natural grasslands','Heathlands'],     
    'Woodland':['Farmland','Woodland','Semi-natural grasslands','Heathlands'],     
    'Semi-natural grasslands':['Farmland','Woodland','Semi-natural grasslands','Heathlands'],     
    'Peatland':['Peatland'],     
    'Heathlands':['Farmland','Woodland','Semi-natural grasslands','Heathlands'],     
    }


def change_allowed(habitat_before,habitat_after):
    """
    Parameters
    ----------
    habitat_before : Dictionary
        the habitat before 
    habitat_after : Dictionary
        the habitat after.

    Returns
    -------
    bool
        whether the habitat after is allowed, given the habitat before.

    """
    hab_type_before = habitat_before['Habitat']
    hab_type_after  = habitat_after['Habitat']
    allowed_habitat_type_after = allowed_habitat_changes[hab_type_before]
    
    if hab_type_after not in allowed_habitat_type_after:
        return False
    condition_before = habitat_before['condition']
    condition_after = habitat_after['condition']
    difference_in_condition = condition_after - condition_before
    
    if difference_in_condition > 1:
        return False
    return True
    


def generate_habitat_after(habitat_before,size,Habitat,Distinct_subtype,Carbon_subtype,condition):
    """
    Parameters
    ----------
    habitat_before : Dictionary
        the habitat values before
    size : float
        size of new habitat
    Habitat : String
        Type of new habitat (this is the broad habitat category, e.g. woodland, farmland, heathland)
    Distinct_subtype : String
        Distinctiveness subtype of new habitat (e.g. Mountain heaths and willow scrub)
    Carbon_subtype : String
        Carbon subtype of new habitat (e.g. Blanket Bog 200cm)
    condition : Float
        Condition of new habitat (e.g. good)

    Returns
    -------
    habitat_values: Dictionary
        the habitat values of the new habitat (if change in habitat is allowed)
    OR 
    'Combination_not_allowed': String
        (if change in habitat is not allowed)

    """
    habitat_name = Habitat + ', ' + Carbon_subtype + ', ' +  Distinct_subtype    
    
    carbon_hab = carbon_combined.loc[(carbon_combined['Habitat'] == Habitat)&(carbon_combined['Subtype'] == Carbon_subtype)]              
    distinctiveness_hab = habitats_distinctiveness.loc[(habitats_distinctiveness['Habitat'] == Habitat)&(habitats_distinctiveness['Subtype'] == Distinct_subtype)]    
    
    storage = float(carbon_hab['Carbon stored (t C ha-1)'])
    flux = float(carbon_hab['Carbon flux (t CO2e ha-1 y-1 )'])
    distinctiveness = int(distinctiveness_hab['Distinctiveness_score'])
    


    strategic_location = habitat_before['strategic_location']
    
    if distinctiveness >= 6:
        connectivity = 1.1
    else:
        connectivity = 1
    condition_values ={
        'Good':3,
        'Fairly Good':2.5,
        'Moderate':2,
        'Fairly Poor':1.5,
        'Poor':1,
        'N/A Agricultural':1,
        'N/A Other':0,        
        }
    
    
    
    difficulty = float(distinctiveness_hab['Difficulty of creation or accelerated succession'])
    time_to_target_condition = float(distinctiveness_hab['Time to target condition for habitat creation - ' +str(condition)])
    if time_to_target_condition == 999:        #these are some that were specified as not allowed by the biodiverstiy metric 2.0 technical supplement pdf
        return 'Combination_not_allowed'
    habitat_values={
        'habitat_name':habitat_name,
        'Habitat':Habitat,
        'Distinct_subtype':Distinct_subtype,
        'Carbon_subtype':Carbon_subtype,
        'size':size,
        'storage':storage,
        'flux':flux,
        'distinctiveness':distinctiveness,
        'condition':condition_values[condition], 
        'strategic_location':strategic_location, 
        'connectivity':connectivity, 
        'difficulty':difficulty,
        'time_to_target_condition':time_to_target_condition,
        'off_site_risk':1,
    }
    
    allowed = change_allowed(habitat_before, habitat_values)   #work out if the change is allowed
    if allowed == False:
        return 'Combination_not_allowed'
    if allowed == True:
        return habitat_values
    

def calculate_all_changes(habitats_before,habitats_after):
    """
    Parameters
    ----------
    habitats_before : Dictionary
        Habitat values before.
    habitats_after : Dictionary
        Habitat values after.

    Returns
    -------
    B_change : float
        Change in biodiversity units
    C_change : float
        Change in carbon sequestered (positive value means more carbon is sequestered with the new habitat than would
                                      have been the case with the old habitat)

    """
    B0 = evaluate_biodiversity_before(habitats_before)
    C0 = evaluate_carbon_before(habitats_before)
    B1 = evaluate_biodiversity_after(habitats_after)
    C1 = evaluate_carbon_after(habitats_after)
    
    B_change = B1-B0
    C_change = C1-C0
    return B_change,C_change


random_habitat_before = generate_habitat_before()

#uncomment to specify a specific habitat
#random_habitat_before = {'habitat_name': 'Farmland, Arable / cultivated land, Intensive orchards', 'Habitat': 'Farmland', 'Distinct_subtype': 'Intensive orchards', 'Carbon_subtype': 'Arable / cultivated land', 'size': 13.85438003606401, 'storage': 120.0, 'flux': 0.29, 'distinctiveness': 2, 'condition': 1.5, 'strategic_location': 1, 'connectivity': 1}


def run_through_all_otions(habitat_before):
    """
    Parameters
    ----------
    habitat_before : Dictionary
        Habitat values before.

    Returns
    -------
    dataframe : dataframe
        A dataframe of all the possible post intervention habitats, 
        including the change in their biodiversity units and carbon storage units

    """
    list_of_habitats = []
    list_of_biodiversity_changes = []
    list_of_carbon_changes = []
    habs = []
    new_size = habitat_before['size']
    """
    idea is, starting from the habitat before, generate every possible habitat after, and calculate all the changes, then plot it
    go through the distinctiveness habitats first, for each of those go through the possible carbon habitats. Also check if the 
    habitat change and condition change are allowed
    """
    for i in range(0,len(habitats_distinctiveness)):
        distinctiveness_hab = habitats_distinctiveness.iloc[i]
        Habitat = distinctiveness_hab['Habitat']
        Distinct_subtype = distinctiveness_hab['Subtype']
        possible_carbon_habs = carbon_combined.loc[(carbon_combined['Habitat'] == Habitat)]
        for k in range(0,len(possible_carbon_habs)):
            carbon_hab = possible_carbon_habs.iloc[k]
            Carbon_subtype = carbon_hab['Subtype']
            conditions = ['Good','Fairly Good','Moderate','Fairly Poor','Poor','N/A Agricultural','N/A Other']
            for condition in conditions:
                habitat_after = generate_habitat_after(habitat_before, new_size, Habitat, Distinct_subtype, Carbon_subtype, condition)
                if habitat_after != 'Combination_not_allowed':
                    changes = calculate_all_changes([habitat_before], [habitat_after])
                    list_of_habitats.append(habitat_after['habitat_name'])
                    list_of_biodiversity_changes.append(changes[0])
                    list_of_carbon_changes.append(changes[1])
                    #print(changes)
                    
                    
                    habs.append(habitat_after)
                    # new_df = pd.DataFrame.from_dict(habitat_after)
                    # if i == 0 and k == 0:
                    #     all_new_habitats = new_df
                    # else:
                    #     all_new_habitats.append(new_df)
            
    dataframe = pd.DataFrame (habs)    
    dataframe['Biodiversity_changes']=list_of_biodiversity_changes
    dataframe['Carbon_changes']=list_of_carbon_changes
    return dataframe
x=run_through_all_otions(random_habitat_before)

"""colours for plotting"""

colors = {'Peatland': 'orange', 
          'Farmland': 'brown', 
          'Woodland': 'green',
          'Heathlands':'pink',
          'Hedgerow':'grey',
          'Orchards':'tomato',
          'Semi-natural grasslands':'limegreen',
          'Coastal Habitats':'cadetblue',
          'Marine Habitats':'steelblue',
          }

"""plot the options on a scatter graph"""
plt.scatter(x['Biodiversity_changes'],x['Carbon_changes'],c=[colors[i] for i in x['Habitat']],alpha= 1)
plt.axhline(0,color='k',linewidth=0.5)
plt.axvline(0,color='k',linewidth=0.5)
ax = plt.gca()
XLIM = ax.get_xlim()
#x_min =
YLIM = ax.get_ylim()
#y_min
for C in colors:
    plt.scatter(700,700,c=colors[C],label=C,alpha=1)
ax.set_xlim(XLIM)
ax.set_ylim(YLIM)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), shadow=False, ncol=2,frameon=False)
# plt.axhline(0,color='k',linewidth=0.5)
# plt.axvline(0,color='k',linewidth=0.5)
plt.xlabel('Biodiversity change')
plt.ylabel('Change in carbon sequestered \n (tonnes over 30 years)')
plt.title('Previous habitat: \n' +str(random_habitat_before['habitat_name']))
name = random_habitat_before["habitat_name"]
plt.savefig('Calculator_example_from'  + str(name) +'.png',dpi=300,bbox_inches="tight")
plt.show()

#all_habs = x['Habitat'].value_counts(dropna=False)