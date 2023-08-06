# pylint: disable=W0622
"""cubicweb-api application packaging information"""


modname = "cubicweb_api"
distname = "cubicweb-api"

numversion = (0, 3, 1)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "This cube is the new api which will be integrated in CubicWeb 4."
web = "https://forge.extranet.logilab.fr/cubicweb/cubes/api"

__depends__ = {
    "cubicweb": ">= 3.36.0",
    "PyJWT": ">= 2.4.0",
    "pyramid-openapi3": ">= 0.14",
}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python :: 3",
    "Programming Language :: JavaScript",
]
