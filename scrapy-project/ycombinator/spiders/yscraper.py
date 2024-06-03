import json
import scrapy


def make_start_urls_list():
    """Returns a list with the start urls."""
    with open('scrapy-project/ycombinator/start_urls.txt', 'r') as f:
        return eval(f.read())


class YCombinator(scrapy.Spider):
    """Crawls ycombinator.com/companies and extracts data about each company."""
    name = 'YCombinatorScraper'
    start_urls = make_start_urls_list()

    def parse(self, response):
        rc = response.css
        # get the JSON object inside the <script> tag
        # cl = 'script.js-react-on-rails-component'
        # st = rc(f'{cl}[data-component-name="CompaniesShowPage"]::text').get()
        st = response.css('[data-page]::attr(data-page)').get()
        if 1 is not None:
            # load the JSON object and set the variable for the 'Company' data
            jo = json.loads(st)['props']
            jc = jo['company']
            yield {
                'company_id': jc['id'],
                'company_name': jc['name'],
                'short_description': jc['one_liner'],
                'long_description': jc['long_description'],
                'batch': jc['batch_name'],
                'status': jc['ycdc_status'],
                'tags': jc['tags'],
                'location': jc['location'],
                'country': jc['country'],
                'year_founded': jc['year_founded'],
                'num_founders': len(jc['founders']),
                'founders_names': [f['full_name'] for f in jc['founders']],
                'team_size': jc['team_size'],
                'website': jc['website'],
                'cb_url': jc['cb_url'],
                'linkedin_url': jc['linkedin_url'],
            }
