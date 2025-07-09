from typing import Optional

from typeguard import typechecked


class DialogScreenRelationParser:
    @typechecked
    def relation(self, relation_ocr: str) -> Optional[int]:
        try:
            return int(relation_ocr)
        except ValueError:
            return None
