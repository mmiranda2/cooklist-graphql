import csv
import functools
from nltk import line_tokenize # Major
from .utils import stringlib


csv.register_dialect('google_recipe_sheet', quoting=csv.QUOTE_ALL, skipinitialspace=True)


class CookbookParser:
    def __init__(self, reader, sections=['ingredients', 'instructions', 'directions'], includes_headers=True):
        self.reader = reader
        self.includes_headers = includes_headers

    def standardize(row):
        return standardize_google_sheet_recipe(row)

    def serialize(self):
        if self.includes_headers:
            headers = next(self.reader)
        for i, row_data in enumerate(self.reader):
			recipe = self.standardize(row)	# empty char sometimes at beginning of recipe. assume true for the end too


class Standardizer:
    ### TODO: Bundle these attributes into a dataset "standards" metadata class, 
    ###       allowing program to coerce a data source X to a result Y following a ruleset R.
    ###       While passing in ORM insert/update functions to be called as desired.
    ###       If data sources vary widely could make the standard ruleset a graph, 
    ###       recursing through it to parse.
    section_standard = lambda x: x
    sections = []
    malforms = []
    standards = {
        'sections': Standardizer.sections,
        'malforms': Standardizer.malforms,
        'section_standard': Standardizer.section_standard
    }
    substitutions = [Standardizer.section_substitutions, Standardizer.other_substitutions]
    ###

    def __init__(self, data):
        self.data = data

    def __iter__(self):
        return self.corrections()
    
    def standardize(self, data):
        for change in self.corrections():
            self.fix(change)
        return self.data

    def corrections(self):
        for substitute in self.substitutions:
            for change in substitute(*self.standards):
                yield change
    
    def get_substitutions(self):
        return self.substitutions
    
    def set_substitutions(self, subs):
        self.substitutions = subs
    
    def fix(data, change):
        old_string, new_string = change
        return self.data.replace(old_string, new_string)


class GoogleSheetStandardizer(Standardizer):
    section_standard = stringmod.standard_section
    sections = ['ingredients', 'instructions', 'directions']
    malforms = [stringmod.bad_section_colon]
    standards = {
        'sections': GoogleSheetStandardizer.sections,
        'malforms': GoogleSheetStandardizer.malforms,
        'section_standard': stringmod.standard_section
    }
    substitutions = [Standardizer.section_substitutions, Standardizer.other_substitutions]

    def __init__(self, row, *args, **kwargs):
        row = row.strip()
        super().__init__(row, *args, **kwargs)
        
    @staticmethod
    def section_substitutions(sections, malforms):
        r_iterable = (
            (malforms(section), stringmod.standard_section(section), section, malforms)
            for section in sections 
            for malforms in malforms
        )
        return r_iterable

    @staticmethod
    def other_substitutions():
        r_iterable = (
            ('\n\n', '\n', None, None),
        )
        return r_iterable


def standardize_google_sheet_recipe(recipe_raw: str) -> str:
	recipe = row_data.strip()
	substitutions = get_substitutions()
	r_function = lambda recipe, sub: recipe.replace(*sub)
	return functools.reduce(r_function, substitutions, recipe)





###### Incomplete ###################
def parse():
    s = '\n\n'.join(['\n'.join(line_tokenize(row[0])) for row in reader ])

def parse_recipe(recipe, sections=['ingredients', 'instructions', 'directions']):
    recipe_lines = recipe.split('\n')
	
    section_heading_loc = {standard_section(section): -1 for section in sections}

    for i, row in enumerate(recipe_lines):
		if row in section_heading_loc:
			section_heading_loc[row] = i
    
    ordered_idxs = sorted(idx for k, idx in section_heading_loc.items())
	start = section_heading_loc[standard_section('ingredients')]
	end = min(idx for idx in ordered_idxs if idx > start)
	recipe_parsed = {
		'title': recipe_lines[0],
		'ingredients': recipe_lines[start:end],
		'raw': recipe
		'section_heading_loc': section_heading_loc
	}
	'''
	for section_heading, idx in ordered_sections:
		if idx >
    for i, section_heading in enumerate(ordered_sections):
        start = subsection[1] + 1
        end = ordered_sections[i+1][1] if i+1 < len(ordered_sections) else len(l)
        recipe[subsection[0]] = l[start:end]
	'''
    return recipe_parsed


def parse_recipe(pth):
	parsed = []
    s = '\n\n'.join(['\n'.join(line_tokenize(row[0])) for row in reader ])
	with open(pth, 'r') as f:
		reader = csv.reader(f, 'google_recipe_sheet')
        headers = next(reader)
		for i, (recipe_text,) in enumerate(reader):
            lines = line_tokenize(recipe_text)
			recipe = standardize_google_sheet_recipe(row_data)	# empty char sometimes at beginning of recipe. assume true for the end too
