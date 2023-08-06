from .componenttestcase import ComponentTestCase
from heaserver.service.testcase.mixin import GetAllMixin


class TestGetAllRootItems(ComponentTestCase, GetAllMixin):  # type: ignore
    pass
