print("Precision: {:.2f}%".format(precision_score(y_test, y_pred, average='weighted') * 100))
print("Recall: {:.2f}%".format(recall_score(y_test, y_pred, average='weighted') * 100))
print("F1 Score: {:.2f}%".format(f1_score(y_test, y_pred, average='weighted') * 100))