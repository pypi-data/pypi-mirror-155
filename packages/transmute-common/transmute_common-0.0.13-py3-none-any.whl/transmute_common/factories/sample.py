def create(values = None):
  # "specimen": {
  #   "accession": ...
  #   "type": {
  #     "code": ...
  #     "display":...
  #     "system": ...
  #   }
  #   "collectedTime": ...
  #   "receivedTime": ...
  #   "collector": ...
  # }
  # "bodySite": {
  #   "code": ...
  #   "display":...
  #   "system": ...
  # }
  record = {
    "sampleId": None,
    "patientId": None,
    "tumorContent": None,
    "disease": None,
    "diseaseOntology": None,
    "detailedDisease": None,
    "detailedDiseaseOntology": None,
    "alternativeDiseaseSystems": None,
    "indication": None,
    "sourceType": None,
    "specimen": None,
    "bodySite": None,
    "age": None
  }
  if values!=None:
    record.update(values)
  return record