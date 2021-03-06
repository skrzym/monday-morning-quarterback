# Springboard Capstone 1 Proposal - Monday Morning Quarterback
## What is the problem you want to solve.
Football is a set-play strategy execution sport. Your offense has the opportunity to execute a multitude of different strategies for each play, but no matter what you do your options are as follows:

* Run
* Pass
* Punt
* Kneel
* Kick a field goal

One of these needs to be chosen first for any game situation.
This is a problem that has a vast amount of data available to help make a decision and that is what this project intends to investigate and deliver.

## Who is your client and why do they care about this problem? In other words, what will your client DO or DECIDE based on your analysis that they wouldn’t have otherwise?

My direct client would be any NFL coach or quarterback who needs to make these decisions successfully to stay employed. However, this analysis and model would also be beneficial to any football enthusiast. Millions of people watch football each week. For every play of every game a viewer can have their own opinion on what the team should do next. This project intends to analyze those opinions as well and see how well they stack up against reality.

##	What data are you going to use for this? How will you acquire this data?

The main dataset comes from the NFL. I will be using two different API’s built by enthusiasts to access the very messy JSON data stream that the NFL offers. First is a python module called nflgame. The second is an R library named NFLscrapR.

For the viewer sentiment analysis my data will primarily come from an open dataset from Crowd Flower. In it there are various football situations that contain user decisions on what should be the next appropriate action. The dataset was generated by the company through a survey format given to users of its service.

Viewer sentiment data will also be collected through a web app that will be created for the project. People who wish to explore the model and test it out on various situations will need to answer a few scenario questions first. This allows the dataset to grow, and also allows the user to see how their decision making skills fair against other users as well as the real NFL data itself.

##	In brief, outline your approach to solving this problem (knowing that this might change later).

### Milestone 1 Deliverables
1. Complete wire framing of web app end result
2. Perform initial exploratory analysis of all data
3. Decide on tools and platform to be used for web app design, hosting, and service of the site

### Milestone 2 Deliverables
1. Play-decision Model complete and ready to be implemented via API
2. Site moved from wire framing state to working page minus the API implementation

### Milestone 3 Deliverables
1. Completed API
2. Integration of API into Website

### Final Milestone Deliverables
1. Report
2. Slides
3. Web app complete and working properly
4. API working and documented correctly

##	What are your deliverables? Typically, this would include code, along with a paper and/or a slide deck.

List of deliverables:

1. Exploratory Notebooks (including code to wrangle data using the APIs)
2. Paper detailing the analysis and generated model used on the web app
3. Slide deck walking through the problem, exploration of the data, and use of the web app
4. Web application that gathers more viewer sentiment data and showcases the play-decision model
5. API for the play-decision model to be used by the web app or standalone for other developers to use.
