# DouTuLa_Scraper
A crawler to scrape images from [斗图啦](www.doutula.com)

## A little about the project
- Images are stored in file system, path is set by `FILES_STORE` in `settings.py`
- Used MongoDB as database, schema:
  * `gifs`: metadata of images
  * `tags`: tags that used to describe a image
  * `img_to_tag`: many-to-many relation between images and tags
- Database connection can be changed in `settings.py`:
  * `MONGO_URI`
  * `MONGO_PORT`
  * `MONGO_DB`
  * `IMAGES_COLLECTION`
  * `TAGS_COLLECTION`
  * `RELATION_COLLECTION`
  
## How to run
Make sure [Scrapy](https://scrapy.org/) and [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup) are installed, and a working MongoDB is running. Then simply run 
```shell
scrapy crawl doutula
```
If you wish to stop and resume scraping in the furture, run commend:
```shell
scrapy crawl doutula -s JOBDIR=job
```
