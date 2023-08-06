def create(values = None):
  record = {
    "sampleId": None,
    "analysisName": None,
    "analysisCenter": None,
    "analysisCenterSampleId":None,
    "qcFailed": None,
    "calls": []
  }
  if values!=None:
    record.update(values)
  return record
