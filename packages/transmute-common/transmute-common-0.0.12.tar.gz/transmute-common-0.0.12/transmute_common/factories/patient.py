def create(values = None):
  # "name": {
  #   "text": ...
  #   "family": ...
  #   "given": ...
  #   "prefix": ...
  #   "suffix": ...
  # }
  record = {
    "patientId": None,
    "name": None,
    "mrnFacility": None,
    "sex": None,
    "race": None,
    "ethnicity": None,
    "dateOfBirth": None
  }
  if values!=None:
    record.update(values)
  return record