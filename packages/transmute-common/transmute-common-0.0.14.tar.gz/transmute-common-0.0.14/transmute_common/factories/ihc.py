def create(values = None):
  # "therapyRecommendation": {
  #   "therapyName": []
  #   "therapySensitivity": ...
  # }
  record = {
    "test": None,
    "value": None,
    "threshold": None,
    "component": None,
    "gene": None,
    "expressionType": None,
    "intensity": None,
    "stainPercent": None,
    "result": None,
    "interpretation": None,
    "therapyRecommendation": None,
  }
  if values!=None:
    record.update(values)
  return record
