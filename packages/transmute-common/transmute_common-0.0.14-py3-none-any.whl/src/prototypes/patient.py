def create(values = None):
  record = {
    "patientId": None,
    "mrnFacility": None,
    "gender": None,
    "race": None,
    "ethnicity": None,
    "dateOfBirth": None
  }
  if values!=None:
    record.update(values)
  return record