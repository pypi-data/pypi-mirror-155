def create(values = None):
  # "specimen": {
  #   "id": ...
  #   "type": {
  #     "coding": [
  #       "system",
  #       "code",
  #       "display",
  #     ],
  #     "text": ...
  #   }
  # }
  # "bodySite": {
  #   "type": {
  #     "coding": [
  #       "system",
  #       "code",
  #       "display",
  #     ],
  #     "text": ...
  #   }
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