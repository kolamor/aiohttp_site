

limit_text_extracts = {
	
	'prop' : 'extracts',
	'exchars' : 100,   # The value must be between 1 and 1,200.
	'exsentences' : 1, # 1-10, not recommend
	'exlimit' : 20,    # No more than 20 allowed
	'exintro' : '', # Return only content before the first section.
	'explaintext' : '', # Return extracts as plain text instead of limited HTML.
	'exsectionformat' : 'wiki', # (plain) - No formatting,
								# (wiki) - Wikitext-style formatting (== like this ==)
								# (raw) - This module's internal representation (section
								#        titles prefixed with <ASCII 1><ASCII 2><section level><ASCII 2><ASCII 1>).
	'excontinue' : 1, # When more results are available, use this to continue. Type: integer


}

action_wiki = {
	
	'titles' : '',
	'prop' : 'images',
	'list' : 'allimages',
}

class BaseKw:

	def __init__(self, *args, **kwargs):

		self.format = kwargs['format'] if 'format' in kwargs else 'json'
		if 'exchars' in kwargs:
			self.exchars = kwargs['exchars']
		if 'exsentences' in kwargs:
			self.exsentences = kwargs['exsentences']
		if 'exlimit' in kwargs:
			self.exlimit = kwargs['exlimit']
		if 'exsectionformat' in kwargs:
			self.exsectionformat = kwargs['exsectionformat']
		if 'excontinue' in kwargs:
			self.excontinue = kwargs['excontinue']


		if 'exintro' in kwargs or args:
			self.exintro = ''
		if 'explaintext' in kwargs or args:
			self.explaintext = ''

class QueryExtracts(BaseKw):


	"""docstring for ActionExtracts"""
	def __init__(self, titles, *args, **kwargs):

		super().__init__(*args, **kwargs)
		self.titles = str(titles)

		self.action = kwargs['action'] if 'action' in kwargs else 'query'
		self.prop = kwargs['prop'] if 'prop' in kwargs else 'extracts'


		

class ParsePage(BaseKw):

	def __init__(self, page, *args, **kwargs):

		super().__init__(*args, **kwargs)
		self.page = page
		self.action = kwargs['action'] if 'action' in kwargs else 'parse'

class OpenSearch(BaseKw):
	"""docstring for """

	def __init__(self, search, *args, **kwargs):

		super().__init__(*args, **kwargs)
		self.search = search
		self.action = kwargs['action'] if 'action' in kwargs else 'opensearch'

		if 'namespace' in kwargs:
			self.namespace = kwargs['namespace']
		if 'limit' in kwargs:
			self.limit = kwargs['limit']

		
class UrlSearch(BaseKw):
	"""docstring for UrlSearch"""
	def __init__(self, gapfrom, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.gapfrom = gapfrom
		self.action = kwargs['action'] if 'action' in kwargs else 'query'
		self.prop = kwargs['prop'] if 'prop' in kwargs else 'info'
		self.generator = kwargs['generator'] if 'generator' in kwargs else 'allpages'
		self.inprop = kwargs['inprop'] if 'inprop' in kwargs else 'url'
		self.gaplimit = kwargs['gaplimit'] if 'gaplimit' in  kwargs else 1

class MediaSearch(BaseKw):
	'''  '''
	def __init__(self, titles, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.titles = str(titles)
		self.action = kwargs['action'] if 'action' in kwargs else 'query'
		self.prop = kwargs['prop'] if 'prop' in kwargs else 'images'



		
class QueryDesigner():

	async def get_html(self, page, *args, **kwargs):
		query = ParsePage(page, *args, **kwargs)
		return query.__dict__

	async def get_markdown():
		pass

	async def opensearch(self, search, *args, **kwargs):
		query = OpenSearch(search, *args, **kwargs)
		return query.__dict__

	async def get_urls(self, gapfrom, *args, **kwargs):
		query = UrlSearch(gapfrom, *args, **kwargs)
		return query.__dict__
		query = MediaSearch(titles, *args, **kwargs)
		return query.__dict__

	async def get_extracts(self, titles, *args, **kwargs):
		'''get_summary'''
		query = QueryExtracts(titles, *args, **kwargs)
		return query.__dict__



def main():
	a = QueryExtracts('xbox')
	b = ParsePage('xbox')
	c = OpenSearch('xbox')
	d = UrlSearch('xbox')
	e = MediaSearch('xbox')
	print(a.__dict__, b.__dict__, c.__dict__, d.__dict__, e.__dict__)

if __name__ == '__main__':
	main()


