# randomfight.com

Trying to predict mixed martial arts fights results using machine learning techniques.

## Gathering data

Data scraped from sherdog.com website.

## Data

For each fight following data is collected:
* About the event
* About the fighters
* About the fight

## Transforming data

Scraped data is transformed into format suitable for machine learning. 
Statistics are calculated in time, pre-fight so the attributes don't leek the outcome.

## Predicting results

Model is trained on data from fights older than 2016 and validated on fights past 2016.
Besides plain `win` and `loss` category targets can be also divided into:

* `win by decision`
* `win by ko`
* `win by submission`
* `loss by decision`
* `loss by ko`
* `loss by submission`
