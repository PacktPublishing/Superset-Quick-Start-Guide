import pandas as pd


def load_and_create_mod_dataset():
	"""
	Method to load Dyadic_COW_4.0.csv from COW_Trade_4.0 dataset.
	This dataset was published by:
		Katherine Barbieri, University of South Carolina (Katherine.barbieri@sc.edu)
			&
		Omar M. G. Keshk, The Ohio State University (keshk.1@osu.edu) February 19, 2017
	It contains bilateral trade flows from 1840-2014.	
	The directory contains
		1) Dyadic_COW_4.0.csv
		2) COW Trade Data Set Codebook.pdf
		3) National_COW

	http://www.correlatesofwar.org/data-sets/bilateral-trade


	The trade values are in US million $ at their 2017 economic value
	Variables used in this analysis:


	Observation year
	importer1: Country A
	importer2: Country B
	flow1: Imports of Country A from Country B in US millions of current dollars
	flow2: Imports of Country A from Country B in US millions of current dollars
	smoothtotrade: Smoothed total trade values (obtained by first summing Flow1 and Flow2 and then applying smoothing).
	spike1: Indicator variable, with 1 equal to changes in flow1 value between period t and t+1 exceeding 50%.
	spike2: Indicator variable, with 1 equal to changes in flow2 value between period t and t+1 exceeding -50%.
	dip1: Indicator variable, with 1 equal to changes in flow1 trade value between period t and t+1 exceeding -50%.
	dip2: Indicator variable, with 1 equal to changes in flow2 trade value between period t and t+1 exceeding -50%.
	trdspike: Indicator variable, with 1 equal to changes in total trade value between period t and t+1 exceeding 50%.
	tradedip: Indicator variable, with 1 equal to changes in total trade value between period t and t+1 exceeding -50%.
	"""
	# load dataframe
	df = pd.read_csv('Dyadic_COW_4.0.csv')
	# select the columns listed above
	select_columns = ['year', 'importer1', 'importer2', 'flow1', 'flow2', 'smoothtotrade', 'spike1', 'spike2', 'dip1', 'dip2', 'trdspike', 'tradedip', 'source1', 'source2']
	df = df[select_columns]
	# remove if source1 or source2 = -9 which means missing data
	df = df[(df.source1!=-9) & (df.source2!=-9)]
	# time filter: 1991 to 2014
	df = df[df.year > 1990]
	# select bilateral trade flows only between
	# the top K nations that traded the most during this time period
	K = 50
	select_nations = df.groupby('importer1').agg({'smoothtotrade': sum}).reset_index().sort_values('smoothtotrade', ascending=False).head(K).importer1.values
	df = df[(df.importer1.isin(select_nations)) & (df.importer2.isin(select_nations))]
	# Separate outgoing and incoming trade flows into separate rows
	select_columns = ['year', 'importer1', 'importer2', 'flow1', 'flow2', 'spike1', 'spike2', 'dip1', 'dip2']
	df = df[select_columns]
	
	df_mod_outflow = df[['year', 'importer1', 'importer2', 'flow1', 'spike1', 'dip1']].copy()
	df_mod_outflow['importer'] = df_mod_outflow['importer1']
	df_mod_outflow['exporter'] = df_mod_outflow['importer2']
	df_mod_outflow['import_in_us_billion'] = round(df_mod_outflow['flow1']/1000.0, 2)
	df_mod_outflow['import_spike_next_year'] = df_mod_outflow['spike1']
	df_mod_outflow['import_dip_next_year'] = df_mod_outflow['dip1']
	for col in ['importer1', 'importer2', 'flow1', 'spike1', 'dip1']:
		del df_mod_outflow[col]

	df_mod_inflow = df[['year', 'importer1', 'importer2', 'flow2', 'spike2', 'dip2']].copy()
	df_mod_inflow['importer'] = df_mod_inflow['importer2']
	df_mod_inflow['exporter'] = df_mod_inflow['importer1']
	df_mod_inflow['import_in_us_billion'] = round(df_mod_inflow['flow2']/1000.0, 2)
	df_mod_inflow['import_spike_next_year'] = df_mod_inflow['spike2']
	df_mod_inflow['import_dip_next_year'] = df_mod_inflow['dip2']
	for col in ['importer1', 'importer2', 'flow2', 'spike2', 'dip2']:
		del df_mod_inflow[col]

	df_mod = pd.concat([df_mod_inflow, df_mod_outflow], axis=0)		

	# Load file for country to eregion mapping
	df_c = pd.read_csv('CountryByRegion.csv')
	country_to_region = {row.Country.strip(): row.Region.strip() for idx, row in df_c.iterrows()}
	df_mod['exporter_region'] = df_mod['exporter'].map(country_to_region.get)
	df_mod['importer_region'] = df_mod['importer'].map(country_to_region.get)

	df_mod.to_csv('Dyadic_COW_4.0_modified.csv', index=False)


if __name__=='__main__':
	load_and_create_mod_dataset()