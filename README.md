### Quickstart
- Build images if there are any changes:
	```bash
	docker-compose build
	```
    This will build the API, Celery worker and crawler container images.
- Start api and celery task services:
	```bash
	docker-compose up -d companies-catalog-api catalog-updater
	```
    The `companies-catalog-api` API depends only on the mongo database instance. It knows nothing about `catalog-updater` celery worker, in fact - it does not know anything about how the db is populated.
- Create crawler container and log into interactive shell - this is where we'll be issuing crawling commands from:
	```bash
	sudo docker-compose run --rm scrapy-crawler
	```
    Note that I decided _not_ to use [scrapyd](https://scrapyd.readthedocs.io/en/stable/), it overcomplicated docker setup for little to no user experience gain.
- As required, we first need to create index file. To do so issue following command:
	```bash
	scrapy crawl sgmaritime_company_index -o company_index.jl
	```
    Once it's done, we have `company_index.jl` json-lines file containing information for the following profile crawler.
- To crawl companies listed in `company_index.jl` issue following `scrapy` command:
	```bash
    scrapy crawl sgmaritime_company_profiles -a companies_index_jl_path=company_index.jl -o company_profiles.jl
    ```
    For each company in the index, it will load profile page via `Splash` - deployed as `scrapy-splash` service in docker.
    
	This not only does create `company_profiles.jl` file, but sends the data to `catalog-updater` service. Scrapy does not know anything about what kind of database is used, just like the API service. Only thing it does is enqueueing Celery tasks.

### Architecture
![alt text](https://raw.githubusercontent.com/Ampretuzo/leadbook_demo/master/architecture.jpg "Logo Title Text 1")

### Notes
- We absolutely didn't have to use `Splash` to execute JavaScript activity - all the information was actually accessible straight via plain html. I integrated it just to demonstrate how web crawling/scraping works when we're dealing with JS-heavy websites.
- Even though there is [a very compelling case](https://blog.scrapinghub.com/2013/05/13/mongo-bad-for-scraped-data) of _not_ using mongo for this use case, I still think it's a good choice. One should choose technologies from immediate requirements and not come up with prophecies about the future when hundreds of terabytes are collected in the db. The flexibility and ease of use of MongoDB are enough to win it for me.
- Django would cut down development time by a factor of 5 at least, but I find Flask to be a much better fit for this case. Django is optimized for rapid development and social-websitey use cases. In this use case, where we're not having any user CRUD action going, Flask's flexibility (e.g. having no ORM lock-in) is a deciding factor. In the long run, one would benefit from it.
