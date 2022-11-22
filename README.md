# yelp-scraper
## Overview:
yelp.com is a website where we can find restaurant details around the world. In this project, we'll scrape the website and store all the details into Firebase database. Firebase database is a Nosql database and supports faster query execution. After storing the data, we'll build a Flask app to execute different queries and deploy it to the GCP.

## How to type query in the URL?
- To search for a specific restaurant: /search?name=< name of the restaurant >
  - Returns a single document.
- To search for restaurants above specific rating eg 4.5: /search?rating=4.5 
  - Returns list of sorted documents by rating in descending order.
- To search for restarants of specific price_type eg $$$ : /search?price_type=$$$
  - Returns list of sorted documents by restaurant name in ascending order.
- To search for restaurants near a specific location: /search?latitude=< lat >&longitude< lon >
  - Returns nearest restaurants within 5km radius. In 'Nearest restaurant first' order.


## Lat Lon endpoint:
![Lat Lon endpoint](https://user-images.githubusercontent.com/40913151/203238863-050450c3-57c2-4e61-96fe-73732d3bfc14.png)

## Name endpoint:
![Name endpoint](https://user-images.githubusercontent.com/40913151/203238923-ade63b86-c6ab-4447-a4e1-d0fcd8c43dda.png)

## Price_type endpoint:
![Price_type endpoint](https://user-images.githubusercontent.com/40913151/203238973-3c8905a9-87f4-4b6b-b683-7e55168f6bcc.png)

## Rating endpoint: 
![Rating endpoint](https://user-images.githubusercontent.com/40913151/203238980-7722522d-3774-4fd2-923c-af8d1791b05b.png)

## GCP deployment steps:
- Go to your cloud console
- Open cloud shell and execute following commands
- $ git clone <this repository>
- $ cd yelp-scraper
- $ gcloud app deploy
- Choose the region closest to your location.
- Done. Your application will be deployed and you'll be provided with a URL.
