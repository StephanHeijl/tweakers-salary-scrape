# tweakers-salary-scrape

This code scrapes self-reported salary data from Gathering of Tweakers and allows for basic analysis
of the facts presented in the forum threads.

![A histogram showing adjusted salaries](https://raw.githubusercontent.com/StephanHeijl/tweakers-salary-scrape/master/AdjustedSalaries.png)

```
pip install scrapy
scrapy runspider tweakspider -o messages.json -s DOWNLOAD_DELAY=5 -s CONCURRENT_REQUESTS=1
```
