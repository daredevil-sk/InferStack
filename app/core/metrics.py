from prometheus_client import Counter

prediction_counter = Counter('model_predictions_total', 'Total number of prediction requests')