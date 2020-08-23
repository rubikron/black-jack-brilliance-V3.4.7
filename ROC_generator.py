# Happy is 0 and 1 is sad in the score returned by the AI
# 0 is our positive class
import requests
import json
import pandas as pd
import numpy as np

def get_prediction(data={"sentence":"I am sad."}):
	url = 'https://k3hn7n41xi.execute-api.us-east-1.amazonaws.com/Predict/56ff48c3-e2a9-4f23-b741-10af77f4bc1c'
	r = requests.post(url, data=json.dumps(data))
	response = getattr(r,'_content').decode("utf-8")
	#print(response)
	return response



# In order to calculate ROC, you need test data
# The test dataset for mood is uploaded
# Read the dataset
mood_test = pd.read_csv('black_jack_setpl2.csv')
dict_records_mood = mood_test.to_dict('records')
y_truth = []
p = 343
y_score = np.zeros((p,2))
label_mapping = {'hit': 0, 'stay': 1}

for sample in range(p):
	print(sample)
	data1 = dict_records_mood[sample]['pl1']
	data2 = dict_records_mood[sample]['pl2']
	data3 = dict_records_mood[sample]['dl1']
	data4 = dict_records_mood[sample]['round_number']
	prediction = get_prediction({"pl1": data1,"pl2": data2,"dl1": data3,"round_number": data4})
	score = json.loads(json.loads(prediction)['body'])['score']
	y_score[sample,:] = score[0]
	label = label_mapping[json.loads(json.loads(prediction)['body'])['predicted_label']]
	if (dict_records_mood[sample]['Action'] == 'hit'):
		y_truth.append(0)
	else:
		y_truth.append(1)

# ROC curve
# Compute ROC curve and ROC area for each class
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

fpr = dict()
tpr = dict()
roc_auc = dict()
n_classes = 2
# roc curve API: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html
for i in range(2):
	fpr[i], tpr[i], thresholds = roc_curve(y_truth, y_score[:,i], pos_label = i)
	roc_auc[i] = auc(fpr[i], tpr[i])

# Compute the ROC curve
plt.figure()

# line width
# positive class can be happy (0) or sad (1)
positive_class = 1
plt.plot(fpr[positive_class], tpr[positive_class], color='darkorange', lw=2, label='ROC curve')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()
