def create(values = None):
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
    "specimenType": None,
    "specimenId": None,
    "age": None
  }
  if values!=None:
    record.update(values)
  return record