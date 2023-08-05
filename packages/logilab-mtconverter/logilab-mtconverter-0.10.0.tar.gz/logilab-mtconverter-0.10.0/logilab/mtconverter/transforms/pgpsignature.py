from logilab.mtconverter.transform import Transform
from logilab.mtconverter import TransformData


class pgpsignature_to_text(Transform):
    name = "gpgsignature_to_text"
    inputs = ("application/pgp-signature",)
    output = "text/plain"

    def _convert(self, trdata: TransformData) -> str:
        return trdata.data
