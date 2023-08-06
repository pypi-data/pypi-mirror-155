def create(values = None):
  # "therapyRecommendation": {
  #   "therapyName": []
  #   "therapySensitivity": ...
  # }
  record = {
    "calledBy": None,
    "test": None,
    "value": None,
    "units": None,
    "result": None,
    "threshold": None,
    "component": None,
    "interpretation": None,
    "therapyRecommendation": None,
  }
  if values!=None:
    record.update(values)
  return record