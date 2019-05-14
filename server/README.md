# Overview
Server and database. We use dynamoDB as our database, and use Flask as server framework.

# Recommendation
We do recommendation based on the fruit that the uses have taken. We store the weight of the fruit when the user put a fruit on weight scale. We also record the time that users eat the fruit if they decrease the amount of fruit on Android application. Then we calculate all of vitamin that users have taken based on the historical data. 

Then we set a recommend percent of each vitamin Ri. If Vi/(∑Vi *Ri) is the minimum amount all vitamin, that means that the user are taking less this kind of vitamin than other vitamin in the history. Then we will recommend fruit high in that vitamin to the user.
