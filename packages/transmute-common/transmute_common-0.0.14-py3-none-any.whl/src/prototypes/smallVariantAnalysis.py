def create(values = None):
  record = {
    "sampleId": None,
    "analysisName": None,
    "pipelineName": None,
    "pipelineVersion": None,
    "analysisCenter": None,
    "analysisCenterSampleId":None,
    "panelName": None,
    "subpanelName": None,
    "subpanelType": None,
    "qcFailed": None,
    "calls": []
  }
  if values!=None:
    record.update(values)
  return record
