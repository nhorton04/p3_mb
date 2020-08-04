# Predicting Income from Census Data

### Introduction:

The US Census is an decennial survey dating back to 1790. Article 1, Section 2 of the Constitution states that the country must conduct a count of its population once every 10 years (although the census began occurring annually starting in the year 2000). The chief purpose of the census is to count every person living in the United States, in order to determine the number of seats each state will have in the House of Representatives. It's also used to draw congressional and state legislative districts.

The results of the census determine how billions of dollars in federal funding are allocated every year - to hospitals, fire departments, schools, roads, and other resources. Far more than just a simple tally of the population, the census provides a treasure trove of demographic and economic data. It is just waiting to be modeled by machine learning algorithms.

### Objective:

Using classification, can we predict an individual's income bracket by looking at their answers to the questions on the census? (Excluding those regarding income, of course). We will use a classification algorithm to make predictions, and try to determine the most suitable model for this specific question.

### Methodology:

Data was downloaded from IPUMS (Integrated Public Use Microdata Series) for the year 2018. In csv format, the dataset initially had 269 features, but many were technical codes for tracking data across different years. Per the website's "About" section: `"Our signature activity is harmonizing variable codes and documentation to be fully consistent across datasets. This work rests on an extensive technical infrastructure developed over more than two decades, including the first structured metadata system for integrating disparate datasets."`

I used the sklearn random forest feature importance module to visualize the features by importance. The exact order of features varied each time I ran the code (I guess because it's based off the results of random forest, which introduces some randomness / variability into the equation?) but followed the same general pattern, with 'UHRSWORK' (usual hours worked per week) consistently coming in first or second place. I also removed features such as 'EDUCD', because it is the same as 'EDUC' but the 'D' stands for detailed, which just means there were more 'outlier' codes added as possible values for the column, but mostly identical to the non-detailed row. Next!

### Feature Engineering:

![Features](https://i.imgur.com/GTFiw9L.png)

*Education level, usual number of hours worked per week, occupation, value of home, bachelor's degree major, age, sex, and travel time to work.*

I undersampled the dataset using "Near Miss" undersampling.

![Before](https://i.imgur.com/H0i5IfA.png)

---
![After](https://i.imgur.com/O51IKw9.png)

However, my R2 scores plummeted when I ran the balanced data in the models, so I just used the imbalanced data. The minority class is about 1/2 the size of the majority class, so it isn't *extremely* imbalanced in the first place.

---

Another thing that I thought would help but didn't was standardization using sklearn's StandardScaler. This made R2 scores nosedive even worse than the undersampled data, so I avoided this for my final models as well.


### Results: <br>



## Citations
#### Census info:
https://2020census.gov/en/what-is-2020-census.html

#### Dataset:
Steven Ruggles, Sarah Flood, Ronald Goeken, Josiah Grover, Erin Meyer, Jose Pacas and Matthew Sobek. IPUMS USA: Version 10.0 [dataset]. Minneapolis, MN: IPUMS, 2020. https://doi.org/10.18128/D010.V10.0
