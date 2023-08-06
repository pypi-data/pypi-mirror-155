def create(values = None):
  # "therapyRecommendation": {
  #   "therapyName": []
  #   "therapySensitivity": ...
  # }
  record = {
    "calledBy": None,
    "genomeBuild": None,
    "coordinateSystem": None,
    "chrom": None,
    "gene": None,
    "refCN": None,
    "cn": None,
    "lowCI": None,
    "lowCIThreshold": None,
    "highCI": None,
    "highCIThreshold": None,
    "log2": None,
    "hotspot": None,
    "call": None,
    "location": None,
    "interpretation": None,
    "therapyRecommendation": None,
  }
  if values!=None:
    record.update(values)
  return record
