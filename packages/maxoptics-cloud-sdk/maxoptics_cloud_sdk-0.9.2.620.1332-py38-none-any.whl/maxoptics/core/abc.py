"""The `abc` module provides some base classes."""
from attr import asdict


class Exportable:
    """
    .. _Exportable:

    The `Exportable` class is provides a minimal template of objects that are:

    1. json-serializable in as part of a MosProject Instance.
    2. able to preform self-replication (reflect).

    Some subclasses may provide their own implementations of relative methods.
    """

    @property
    def export(self):
        """Return must be json-serializable, which means be composed with base data structure."""

        ...

    def to_dict(self, *args, **kwargs):
        """The return could be composed by non-standard data structure."""
        return self.export

    def __deepcopy__(self, memodict={}):
        return self.reflected()

    def reflected(self, *args, **kwargs):
        """Beta feature.

        Return a replication of `self`.

        The new `'self'` will have same attributes but do not share them with the original in memory space.

        Mainly as a tool for data safety in concurrent operations.
        """
        from maxoptics.core.component.base.Component import ProjectComponent
        from maxoptics.core.component.base.Attrs import (
            ProjectComponentAttrsBase,
        )

        T = type(self)
        new_self = T(*args)

        def handle_single(val, reflected_, key_or_ind):
            if isinstance(val, dict):
                if not isinstance(reflected_[key_or_ind], dict):
                    reflected_[key_or_ind] = {}
                handle_dict(val, reflected_[key_or_ind])
                return

            elif isinstance(val, list):
                if not isinstance(reflected_[key_or_ind], list):
                    reflected_[key_or_ind] = []
                handle_list(val, reflected_[key_or_ind])
                return

            elif issubclass(T, ProjectComponent):
                if isinstance(val, ProjectComponentAttrsBase):
                    reflected_[key_or_ind] = val.reflected(new_self)
                    return

            elif issubclass(T, ProjectComponentAttrsBase):
                if isinstance(val, ProjectComponentAttrsBase):
                    reflected_[key_or_ind] = val.reflected(*args)
                    return

            if not isinstance(val, Exportable):
                reflected_[key_or_ind] = val
            else:
                reflected_[key_or_ind] = val.reflected()

        def handle_dict(dikt, reflected_d):
            for key, val in dikt.items():
                if key in ["__parent_ref__"]:
                    continue
                handle_single(val, reflected_d, key)

        def handle_list(lst, reflected_l):
            for i, item in enumerate(lst):
                diff_len = len(lst) - len(reflected_l)
                assert diff_len >= 0
                for i in range(diff_len):
                    reflected_l.append(None)
                handle_single(item, reflected_l, i)

        handle_dict(self.__dict__, new_self.__dict__)

        new_self.__dict__.update(**kwargs)
        return new_self


class ExportableAttrS(Exportable):
    """ExportableAttrS abc class for class with 'attr.define' form."""

    @property
    def export(self):
        """Turn self to a dict"""
        return asdict(self)
