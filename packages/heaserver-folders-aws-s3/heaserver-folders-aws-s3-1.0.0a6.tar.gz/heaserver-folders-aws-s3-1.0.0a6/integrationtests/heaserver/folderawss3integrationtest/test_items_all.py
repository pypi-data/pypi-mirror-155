from .folderawss3testcase import AWSS3ItemTestCase, AWSS3FolderTestCase
from heaserver.service.testcase.mixin import DeleteMixin, GetAllMixin, GetOneMixin, PutMixin, PostMixin


class TestDeleteFolder(AWSS3FolderTestCase, DeleteMixin):
    pass


class TestGetFolders(AWSS3FolderTestCase, GetAllMixin):
    pass


class TestGetFolder(AWSS3FolderTestCase, GetOneMixin):
    pass


class TestDeleteItem(AWSS3ItemTestCase, DeleteMixin):
    pass


class TestGetItems(AWSS3ItemTestCase, GetAllMixin):
    pass


class TestGetItem(AWSS3ItemTestCase, GetOneMixin):
    pass


class TestPostItem(AWSS3ItemTestCase, PostMixin):
    pass


class TestPutItem(AWSS3ItemTestCase, PutMixin):
    pass
