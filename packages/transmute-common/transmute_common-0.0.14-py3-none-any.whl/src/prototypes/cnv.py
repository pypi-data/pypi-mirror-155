def create(values = None):
  record = {
    "genomeBuild": None,
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

    "interpretation": None
  }
  if values!=None:
    record.update(values)
  return record
