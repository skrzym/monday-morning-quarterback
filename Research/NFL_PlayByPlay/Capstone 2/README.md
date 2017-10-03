Capstone 2 is located in ***"Research\NFL_PlayByPlay\Capstone 2"***

In this folder there are 3 notebooks. Each is listed below with a short description of what is inside.

* **GetDriveInfo.ipynb** - Data Preprocessing for collecting all overall drive results from every NFL play.
* **Combine Old and New.ipynb** - Merging gathered drive data with existing play-by-play data so each play has a corresponding drive result associated with it.
* **Build Stronger Model.ipynb** - This final notebook goes through and converts the drive results categorical response into a binary response with scoring related drive results being coded as a success and all other being coded as a failure. The data is also processed for one-hot encoding of the 3 new inputs compared to Capstone 1:
    * posteam - Team with the ball
    * DefensiveTeam - Team trying to stop the play
    * PlayType - our response factor from Capstone 1 now an input along with all our other inputs for support to tell us if picking this PlayType (Run, Pass, Field Goal, Punt, QB Kneel) is a good or bad decision.

    This is required for the scikit-learn RandomForestClassifier because to my knowledge it can't handle categorical factors like R or H20 implementations can.

    The notebook then Runs a RandomizedSearchCV over
    * Max Depth
    * Max Features
    * Min Samples Split
    * Min Samples Leaf
    * Bootstrap
    * Criterion

    Doing 10 fold CV internally.

    Then the best parameters are determined, a new RFC is fitted with these hyperparameters, and it is scored against the hold-out test data to see performance changes.
    This file aslo has built out plots for ROC and Precision vs Recall to see how the classifier is performing.
