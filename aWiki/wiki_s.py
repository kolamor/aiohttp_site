import re

class FormatText:

	async def _cleanhtml(self, raw_html):

		# remove html tags
		cleantext = re.sub(r"<.*?>", "", raw_html)

		# remove the html comments
		cleantext = re.sub("(<!--.*?-->)", "", cleantext, flags=re.DOTALL)

		# remove lines with multiple spaces on them, happens after the regexe
		cleantext = "\n".join([r.strip() for r in cleantext.split("\n")])

		# remove multiple newlines which appeared after the regexes
		cleantext = re.sub(r"\n\n+", "\n\n", cleantext)

		# remove the edit things after the headings
		cleantext = cleantext.replace("[edit]", "")
		cleantext = cleantext.replace("(edit)", "")


		return cleantext


		async def text(self, html):

			return self._cleanhtml(html)



class Deser:

	@classmethod
	async def get_extracts(cls, json):

		data = json['query']["pages"]
		data = data[list(data.keys())[0]]["extract"]
		return data


	@classmethod
	async def get_html(cls, json):
		data = json["parse"]["text"]["*"]
		return data

	@classmethod
	async def get_urls(cls, json):
		data = json["query"].get("pages")
		if not data:
			raise PageNotFound("Unknown Page or error when getting page URLs")
		data = list(data.items())[0][1]
		pages = [data["fullurl"], data["editurl"]]
		return pages


	@classmethod
	async def get_media(cls, json):
		# print(json)
		pages = json["query"]["pages"]

		images = list(pages.values())[0].get("images")

		if not images:
			return []
		return images


