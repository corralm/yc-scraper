import json
import scrapy


class YCombinator(scrapy.Spider):
    """Crawls ycombinator.com/companies and extracts data about each company."""
    name = 'YCombinatorScraper'
    start_urls = ['https://www.ycombinator.com/companies/helion-energy']

    def parse(self, response):
        rc = response.css
        # get the JSON object inside the <script> tag
        cl = 'script.js-react-on-rails-component'
        st = rc(f'{cl}[data-component-name="CompaniesShowPage"]::text').get()

        # load the JSON object and set the variable for the 'Company' data 
        jo = json.loads(st)
        jc = jo['company']
        yield {
            'company_id': jc['id'],
            'company_name': jc['name'],
            'short_description': jc['one_liner'],
            'long_description': jc['long_description'],
            'batch': jc['batch_name'],
            'status': jc['ycdc_status'] ,
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
