from datetime import datetime
from typing import Optional

from beanie import Document


class Model(Document):
    """Base class for models saved to db. Inherits from and replaces
    beanie 'Document' class where needed, and adds `created_at` and
    `updated_at` fields for every class object.

    """

    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None
    