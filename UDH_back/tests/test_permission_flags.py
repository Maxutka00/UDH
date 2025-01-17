import unittest
from udh_backend.api.utils.permission_flags import PermissionFlags, _PermissionsEnum


class TestPermissionFlags(unittest.TestCase):

    def test_simple(self):
        abstract_user = PermissionFlags()
        self.assertEqual(abstract_user.serialize(), 0, "At the start the serialization has to be 0!")
        self.assertFalse(bool(abstract_user.user), "At the start user ast to be False")
        abstract_user.user.set(True)
        self.assertTrue(bool(abstract_user.user), "No changed was applied after abstract_user.user.set(True)")
        abstract_user.user.set(False)
        self.assertFalse(bool(abstract_user.user), "No changed was applied after abstract_user.user.set(False)")

    def test_serialize(self):
        abstract_user = PermissionFlags()
        abstract_user.user.set(True)
        abstract_user.admin.set(True)
        raw = abstract_user.serialize()
        raw_user_admin = _PermissionsEnum.user | _PermissionsEnum.admin
        self.assertEqual(raw, raw_user_admin, "Raw user was not expected")

    def test_check_presence(self):
        abstract_user = PermissionFlags()

        for field in _PermissionsEnum.__dict__:
            field: str
            if field.startswith("_"):
                continue
            self.assertTrue(field in abstract_user.__dict__, f"Attribute {field} was not found at PermissionFlags")


    def test_iterate(self):
        abstract_user = PermissionFlags()

        for field in _PermissionsEnum.__dict__:
            field: str
            if field.startswith("_"):
                continue
            if field not in abstract_user.__dict__:
                continue
            attr = abstract_user.__getattribute__(field)
            self.assertFalse(attr, f"Initial value of {field} has to be False, not True")
            attr.set(True)
            self.assertTrue(attr, f"Attribute was not affected by attr.set(True)")

    def test_import(self):
        abstract_user = PermissionFlags()

        abstract_user.user.set(True)
        serialized = abstract_user.serialize()

        another_abstract_user = PermissionFlags(serialized)
        self.assertTrue(another_abstract_user.user, "Serialized data was damaged onTrue")
        new_serialized = abstract_user.serialize()
        self.assertEqual(new_serialized, serialized, "Serialized data was damaged onCompare")

    def test_multiple_set(self):
        abstract_user = PermissionFlags()
        abstract_user.user.set(True)
        abstract_user.user.set(True)
        self.assertTrue(abstract_user.user, "Multiple set(True) calls were not expected")
        inverted_user = ~abstract_user.serialize()
        # user consist only _PermissionsEnum.user
        self.assertEqual(inverted_user & _PermissionsEnum.user, 0, "Inverted user was not expected")


if __name__ == '__main__':
    unittest.main()
