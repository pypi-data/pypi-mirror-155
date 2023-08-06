class Selector():
	
    ###############################################################################################################
    #   For a dictionary (data), find the area which hasa  matching field + value
    #   e.g. data = [ {"id":"abc", "value":123}, {"id":"xyz", "value":333}]
    #   
    ###############################################################################################################
	def dict_search(self, data, selector, result_accum={}, cnt=1, loc_debug=False):

		if loc_debug: print(f"\nBEGIN: selector={selector}")
		if loc_debug: print(f"{'*'*cnt}DATA: [{data}] =?= [{ selector }]")

		selector_results = result_accum.copy()
		for item in data:  #go through each data item
			if loc_debug: print(f"{'-'*cnt}\nCheck each data item:\n{'-'*cnt}ITEM={item} ")

			for index, sel_key in enumerate(selector.keys()):  #Go through each of the query items
				if loc_debug: print(f"{'-'*cnt}{item} =?= {sel_key  }:{ selector[sel_key]  } ")

				if ( item == sel_key ): #If matches, then confirm
					if loc_debug: print(f"{'-'*cnt}ITEM KEY: [{item}] => [{sel_key}]") 

					if ( data[  sel_key ] == selector[sel_key] ):
						if loc_debug: print(f"{'-'*cnt}ITEM VALUE: [{data[  sel_key ]}] => [{selector[sel_key]}]") 
						selector_results[ item] =  data[ sel_key ] 

					elif isinstance( data[sel_key], dict) or isinstance( data[sel_key], list):
						if loc_debug: print(f"{'-'*cnt}ITEM VALUE DICT->: [{selector[sel_key]}] => [{data[  sel_key ]}]") 
						result = self.dict_search(  data[sel_key], selector[sel_key], selector_results, cnt+1)
						if result: return result  
				else:
					if isinstance(  item, dict):
						if loc_debug: print(f"{'-'*cnt}DICT1->: [{item}]  ")
						result = self.dict_search(  item, selector, selector_results, cnt+1)
						if result: return result 
					elif isinstance( data[item], list):
						if loc_debug: print(f"{'-'*cnt}LIST1->: [{item}] => [{ data[item] }]")
						result = self.dict_search(  data[item], selector, selector_results, cnt+1)
						if result: return result  	

			if len( selector_results.keys() ) == len(selector): 
				if loc_debug: print(f"found!::{selector_results}")
				if loc_debug: print(f"END\n\n")
				return data
			if loc_debug: print(f"END\n\n")
