![Alt text](images/header.png)<br>
# TRAVEL INSURANCE - DO YOU KNOW YOUR CUSTOMER

## IMPORTANT NOTICE
<i>For plotting plotly libraries are used throughout this project. As interactive plotly plots
are not available for preview at github, static images have been generated for preview and
embedded in the notebook (render_mode in the first cell of the notebook has been set to 'github').
For viewing of interactive plots it is adviced to clone this repository, follow the dependencies, 
listed in the 'requirements.txt' file (available in the project folder), open the notebook,
change the render_mode to 'interactive' and run 'Restart Kernel and Run All Cells' from the
jupyter menu.

KEEP IN MIND, THAT RESTARTING THIS NOTEBOOK WILL RE-RUN HYPERPARAMETER TUNING, WHICH IS COMPUTATIONALLY
COSTLY. IT MAY REQUIRE AT LEAST 10-15 MINUTES TO RECALCULATE ALL CALCULATIONS ON A RELATIVELY FAST MACHINE.
RESTART AT YOUR OWN CONSIDERATION.

Happy reading!</i>

## About the project
The project focuses at constructing a model for prediction of a travel company's customer's behaviour,
in particular - whether the customer would be willing to purchase a travel insurance policy.

## Insights and Conslusions
**Dataset**<br>
Total 1987 rows were split into training and test sets at a 80/20 ratio. The trainingset (1589 rows) contains 523 duplicated rows and 639 rows that may create potential outcome conflict. Although duplicated and conflicting rows may introduce bias and unnecessary noise, it was decided tokeep the data as it is for model training.

**Customers**<br>
The perfect customer of the Travel & Tours Company may be described as a representative of private sector (or self-employed) of 33-35 years of age with more than 5 persons in the family and annual income of more than 1.3 million INR. The perfect customer also likes to travel abroad and therefore has a frequent flyer status.

**PR AUC vs Accuracy**<br>
PR AUC was chosen over Accuracy as a key metric for model performance evaluation as it focuses on precision and recall, which are relevant for evaluating the performance of the positive class.

**Conclusions**<br>
Voting Ensemble achieves high accuracy (84%) and precision (91%), meaning it correctly classifies most instances and avoids false positives effectively. However, its recall is lower (60%), indicating it misses a significant portion of actual positives, with 57 false negatives. This trade-off suggests the model is conservative in predicting positives, favoring precision over recall, which may be suitable in scenarios where false positives are more critical than false negatives.

From a business perspective, the model's high precision implies it is effective at identifying customers likely to buy travel insurance, minimizing marketing efforts on uninterested customers. However, the lower recall indicates it misses nearly 40% of potential buyers, leading to lost opportunities for revenue. To maximize business impact, improving recall (e.g., by adjusting the decision threshold) could help identify more potential buyers, increasing overall sales while balancing marketing efficiency.

## Space for Improvement
Simulation and analysis of "what-if" scenario (virtual A/B experiment) for exploring potential gains with marketing campaigns targeted at domestic travellers.

Threshold tuning for final models for improvement of recall values.

## Dependencies
The dependencies are managed by <i>poetry</i> via pyproject.toml dependency file. Dependencies are listed below,
including compatible versions:

python = "^3.13"
pandas = "^2.2.3"
plotly = "^5.24.1"
scikit-learn = "^1.5.2"
phik = "^0.12.4"
ipykernel = "^6.29.5"
jupyterlab = "4.3.0"
black = "^24.10.0"
jupyterlab-code-formatter = "^3.0.2"
kaleido = "==0.1.*"
isort = "^5.13.2"
statsmodels = "^0.14.4"
mypy = "^1.14.0"

## Contents of the Project Folder
Folders:
data - folder with dataset in .csv format
helpers - folder with helper functions
images - folder with images of header for this readme and plot image .png files

Files:
poetry.lock - poetry settings file
pyproject.toml - poetry project dependencies file
travel_insurance.ipynb - project jupyter notebook
README.md - this file
