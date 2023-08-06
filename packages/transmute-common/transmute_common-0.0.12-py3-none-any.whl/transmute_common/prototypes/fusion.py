def create(values = None):
  record = {
    "name": None,
    "annotation": None,
    "5pGene": None,
    "3pGene": None,
    "read_count": None,
    "rpm": None
  }
  if values!=None:
    record.update(values)
  return record
