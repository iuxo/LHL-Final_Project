# Predicting League of Legends Wins
## Background
League of Legends is a online 5v5 MOBA (Multiplayer Online Battle Arena) game where the objective of the game is to destroy the enemy base before they destroy yours. Players fight minions, jungle monsters, and each other to gather resources, namely gold and levels, which they can spend to buy items and level up skills to become stronger than the enemy team.
## Goals
I wanted to have a project where I go through the entire data science workflow. One with these steps: Defining Goals and Objectives, Data Acquisition, Data Cleaning/Engineering, Modelling, Evaluation, (Deployment). Because I spent so much time playing this game in the past I thought, wouldn't it be interesting if I could apply my new data science knowledge to my love for gaming? So the goal for this project was to answer this question: Is it possible to predict which team will win based on stats taken from the 10 minute mark? If so, which feature is most important for predicting team wins?
## Steps taken for this project
### Data Acquisition:
I worked with the Riot Games API using different endpoints, gathering ~10000 high elo (Diamond 1 MMR) ranked games
* League-V4 was used to gather high ranked players' summoner (in game) names. These players were Diamond 1 at the time of gathering which is the top 1% of players. 
* Searching for match history requires getting the PUUID (Player Universally Unique IDentifier), so after obtaining their summoner names I had to input those into SUMMONER-V4 to grab their PUUIDs.
* After obtaining the PUUIDs for players, I then took each of those players last 10 ranked games played and obtained the match IDs using MATCH-V5 searching by PUUID.
* Then after getting the list of match IDs, I used MATCH-V5 again but this time made API calls to get the match timelines.
### Data Cleaning/Engineering
Each of the API calls returned a MatchTimelineDTO, where I parsed through the JSON object to get metadata, events, and winner obtaining stats for each of the sides (blue and red). Initially I stored the raw features in a custom class that had 22 features symmetrical for blue and red side. After further investigation, I realized I could take the difference of the two sides reducting the dimensionality of my problem from 22 features to 11 features.
### Modelling
For the baseline model I used a simple Logistic Regression Classifier which returned decent results, but eventually chose a Random Forest Classifer for my project because I could see which features were most important to the model when evaluating. 
### Evaluation
For this project, accuracy was the metric of choice. The dataset had a slight imbalance but not nearly enough to affect the model. False Positives and False Negatives were not as important in this project compared to other's like predicting cancer in patients. I only wanted to see how well my model could predict which team would win. Here were the metrics:
* Baseline (Logistic Regression with raw features): 67%
* Random Forest (raw features): 65%
* Random Forest (engineered features): 72%
* GridSearch: 73%
The feature engineering really made an impact improving the accuracy by 7%. Tuning hyper parameters also increased accuracy by 1%. There are so many factors that are unable to be modelled through stats and so many things can happen within a game where one side can throw their lead. For example, how good a player's mentality is towards the game, counter picks, or how well they can communicate to their team. Overall I was happy with how my model performed achieving 73% accuracy. 
## Results
To answer the initial questions I had, yes it is possible to predict which team SHOULD win at the 10 minute mark to a certain extent. 73% accuracy on predicting which team should win at the 10 minute mark. The features that were most important to the model were the difference in total gold, champions killed, and level which had 37%, 28%, 13% importance respectively. These percentages made sense to me as a difference in gold means a difference in items which equates to a difference in stats meaning the side with more gold usually is stronger. Killing champions gives the killer gold and experience, and because we can see that gold is very important to the model it makes sense that it comes second. Not to mention when players die in game they take time to respawn and walk to their lane losing valuable time which could be spent collecting resources. 
## Future Goals
My future goal would be to deploy this model and build a website where someone could search themselves up to get their past 10 games and the model's prediction for that game. Each game could have some more in depth analysis on what went wrong in the first 10 minutes of the game with graphs of the leads/difference between each team. 
