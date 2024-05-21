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
        tx = rc('div[data-reactroot]::attr(data-page)').get()
        st = None

        try:
            ob = json.loads(tx)
            st = ob['props']
        except:
            # handle gracefully
            self.logger.warning(
                'No JSON object found in the response for %s' % response.url
            )

        if st:
            jc = st['company']
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
        else:
            self.logger.warning(
                'No props object found in page; YC may have modified their page format. Contact the repo owner'
            )
