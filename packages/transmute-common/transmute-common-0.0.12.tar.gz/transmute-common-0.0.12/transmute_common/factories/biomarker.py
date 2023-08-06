def create(values = None):
  record = {
    "test": None,
    "value": None,
    "units": None,
    "result": None,
    "interpretation": None,
    "threshold": None,
    "component": None,
    "therapyRecommendation": None,
  }
  if values!=None:
    record.update(values)
  return record