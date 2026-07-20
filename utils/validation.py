from pathlib import Path
from utils.exceptions import ValidationError
def validate_a2l(v):
 p=Path(v)
 if not v.strip():raise ValidationError("Please select an A2L file.")
 if p.suffix.lower()!=".a2l":raise ValidationError("The selected file must have the .a2l extension.")
 if not p.is_file():raise ValidationError(f"File not found: {p}")
 return p.resolve()
