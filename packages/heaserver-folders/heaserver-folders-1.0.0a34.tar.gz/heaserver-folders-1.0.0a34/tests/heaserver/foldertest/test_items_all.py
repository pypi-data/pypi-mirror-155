from .foldertestcase import ItemTestCase, FolderTestCase
from heaserver.service.testcase.mixin import DeleteMixin, GetAllMixin, GetOneMixin, PutMixin, PostMixin


class TestDeleteFolder(FolderTestCase, DeleteMixin):
    pass


class TestGetFolders(FolderTestCase, GetAllMixin):
    pass


class TestGetFolder(FolderTestCase, GetOneMixin):
    pass


class TestDeleteItem(ItemTestCase, DeleteMixin):
    pass


class TestGetItems(ItemTestCase, GetAllMixin):
    pass


class TestGetItem(ItemTestCase, GetOneMixin):
    pass


class TestPostItem(ItemTestCase, PostMixin):
    pass


class TestPutItem(ItemTestCase, PutMixin):
    pass
