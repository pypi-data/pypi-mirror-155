def create(values = None):
  record = {
    "calledBy": None,
    "genomeBuild": None,
    "orientation": None,
    "strand": None,
    "coordinateSystem": None,
    "sequenceType": None,
    "chrom": None,
    "pos": None,
    "ref": None,
    "alt": None,
    "type": None,
    "exact": None,
    "length": None,
    "start": None,
    "end": None,
    "readDepth": None,

  }
  if values!=None:
    record.update(values)
  return record
