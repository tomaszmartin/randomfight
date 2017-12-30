# randomfight.com

Trying to predict mixed martial arts fights results using machine learning techniques.

## Gathering data

Data scraped of the fightmetric.com website using:
* `scrape_links()` for extracting list of fighters and fights for an event
* `scrape_event_data()` for extracting information about the event
* `scrape_fighter_data()` for extracting information about the fighter
* `scrape_fight_data()` for extracting information about the fight

All of those are combined in a `EventScraper` class, which:
* extract all fights and fighters from an event
* combine fight and fighters data
* returns list of fights combined with the information about fighters and the event

## Data

For each fight following data is collected:
* About the event:
  * Date
  * Attendance
* About the fighters:
  * Fight attributes like strikes thrown, takedowns etc.
  * Physical attributes like age, height, range, stance
* About the fight:
  * Time it lasted
  * Weight category
  * Position on the fight card
  * Is it a title fight

## Transforming data

Scraped data is transformed into format suitable for machine learning.
* All the statistics are calculated in time.
* Both fighters statistics are pre-fight so the attributes don't leek the outcome.

## Predicting results

Model is trained on data from fights older than 2016 and validated on fights past 2016.
Besides plain `win` and `loss` category targets can be also divided into:

* `win by decision`
* `win ko`
* `win by submission`
* `loss by decision`
* `loss ko`
* `loss by submission`
