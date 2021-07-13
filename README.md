# Etsy Web-Scraping 

This project strips the content and tags of etsy product webpages, and returns a that information as a csv. The program is currently set up to scrape the first 10 pages of each catagory, this can be changed by adjusting a value in pageScrapper.py.

## Workflow

flowchart TB

    subgraph S1
        direction TB
        B1{categoryScraper.py}
        B[Scrape urls from catagory pages]
    end

    subgraph S2
        direction TB
        C2{{Slurm Array}} --> C1{pageScraper.py}
        C[Get raw html]
    end

    subgraph S3
        direction TB
        D1{htmlStripper.py}
        D[HTML Extraction] --> E[Text Cleaning]
    end

    A((Source File)) -->|site_urls.csv| S1
    S1 --> |Pages folder| S2
    S2 --> |Dated folder of tared html| S3
    S3--> |scrapedEtsyPages.csv| F((Output CSV))

## To Run

To run this program:
 - Change all the filepaths, since the current program is hardcoded to use the original directory for the amazon/etsy scraping project. 
 - create the site_url.csv. 
 - Run categoryScraper.sbatch, pageScraper.sbatch, and htmlStripper.sbatch in order.
