"""Provides 'Query' and related classes and types"""

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Union, cast

from bson import ObjectId

from nawah.exceptions import (InvalidQueryOperTypeException,
                              InvalidQueryStepAttrLenException,
                              InvalidQueryStepAttrTypeException,
                              InvalidQueryStepLenException,
                              InvalidQueryStepTypeException,
                              UnknownQueryOperException)

from ._jsonpath import JSONPath
from ._var import Var

if TYPE_CHECKING:
    from nawah.types import (NawahQueryOperAnd, NawahQueryOperOr,
                             NawahQuerySpecial, NawahQueryStep)

logger = logging.getLogger("nawah")

SPECIAL_ATTRS = [
    "$search",
    "$sort",
    "$skip",
    "$limit",
    "$extn",
    "$soft",
    "$attrs",
    "$group",
    "$geo_near",
    "$deleted",
]


# [TODO] Remove Var type from QUERY_OPERS after implementing QueryMod type
QUERY_OPERS = {
    "$eq": (Var, type(None), str, int, float, list, dict, ObjectId),
    "$ne": (Var, type(None), str, int, float, list, dict, ObjectId),
    "$gt": (Var, str, int, float),
    "$gte": (Var, str, int, float),
    "$lt": (Var, str, int, float),
    "$lte": (Var, str, int, float),
    "$all": (Var, list),
    "$in": (Var, list),
    "$nin": (Var, list),
    "$regex": (Var, str),
}


@dataclass(kw_only=True)
class Query:
    pipe: list[
        Union["NawahQueryStep", "NawahQueryOperOr", "NawahQueryOperAnd"]
    ] = field(default_factory=cast(Any, list))
    special: "NawahQuerySpecial" = field(default_factory=cast(Any, dict))

    def __post_init__(self):
        if not self.pipe:
            self.pipe = []
        if not isinstance(self.pipe, list):
            raise Exception(
                f"Value for 'pipe' should be of type 'list'. Got '{type(self.pipe)}' "
                "instead"
            )

        if not self.special:
            self.special = {}
        if not isinstance(self.special, dict):
            raise Exception(
                f"Value for 'special' should be of type 'dict'. Got '{type(self.special)}' "
                "instead"
            )

        self.reset_index()

    @property
    def index(self) -> dict[str, list[tuple[str, Any]]]:
        return self._index

    def reset_index(self):
        self._index = {}
        _index_query_pipe(pipe=self.pipe, special=self.special, index=self._index)

    def __contains__(self, k):
        if k[0] == "$":
            return k in self.special

        if ":" not in k:
            logger.warning(
                "Query.__contains__ is called with deprecated format: %s. Implicitly, appending ':$eq'",
                k,
            )
            k = f"{k}:$eq"

        return k in self.index

    def __getitem__(self, k):
        if k[0] == "$":
            return self.special[k]

        if ":" not in k:
            logger.warning(
                "Query.__getitem__ is called with deprecated format: %s. Implicitly, appending ':$eq'",
                k,
            )
            k = f"{k}:$eq"

        return QueryItem(self.index[k], self, ":*" in k)

    def __setitem__(self, k, v):
        if k[0] != "$":
            raise Exception("Query.__setitem__ used against non Query Special Attr")

        self.special[k] = v

    def __delitem__(self, k):
        if k[0] != "$":
            raise Exception("Query.__delitem__ used against non Query Special Attr")

        del self.special[k]

    def append(
        self,
        o: Union["NawahQueryStep", "NawahQueryOperOr", "NawahQueryOperAnd"],
        /,
    ):
        self.pipe.append(o)
        self.reset_index()


class QueryItem(list):
    def __init__(self, item_list, query, full_repr):
        self._item_list = item_list
        self._query = query
        super().__init__(
            [value if full_repr else value[list(value)[0]] for path, value in item_list]
        )

    def __setitem__(self, i, o):
        iterable = [i]
        if i == "*":
            iterable = range(len(self))

        for ii in iterable:
            self._item_list[ii][1][list(self._item_list[ii][1])[0]] = o

    def __delitem__(self, i):
        iterable = [i]
        if i == "*":
            iterable = range(len(self))

        for ii in iterable:
            item_path = self._item_list[ii][0].split(".")
            item_parent_path = ".".join(item_path[:-1])
            item_parent = JSONPath(item_parent_path).parse(self._query.pipe)
            del item_parent[int(item_path[-1])]

        # Reset query index, then retrieve value for index to force re-index
        self._query.reset_index()
        self._query.index  # pylint:disable=pointless-statement


def _validate_query_step(step, /):
    """Validates value of provided \'Query\' step per \'Query Arg Oper\'. If failed, raises
    \'InvalidQueryArgException\' or \'UnknownQueryArgException\' if \'Query Arg Oper\' is unknow"""

    if not isinstance(step, dict):
        raise InvalidQueryStepTypeException(step_type=type(step))

    if len(step) != 1:
        raise InvalidQueryStepLenException(step_items=tuple(step))

    step_key = list(step)[0]

    if not isinstance(step_key, str):
        # [TODO] Custom Exception
        raise Exception()

    if step_key in ("$and", "$or"):
        if not isinstance(step[step_key], list):
            # [TODO] Custom exception
            raise Exception()

        for child_step in step[step_key]:
            _validate_query_step(child_step)

        return

    if not isinstance(step[step_key], dict):
        raise InvalidQueryStepAttrTypeException(step_attr_type=type(step[step_key]))

    if len(step[step_key]) > 1:
        raise InvalidQueryStepAttrLenException(step_attr_items=tuple(step[step_key]))

    step_oper = list(step[step_key])[0]

    if step_oper not in QUERY_OPERS:
        raise UnknownQueryOperException(
            attr_name=step_key,
            attr_oper=step_oper,
        )

    step_val = step[step_key][step_oper]
    _validate_query_step_val(
        step=step, step_key=step_key, step_oper=step_oper, step_val=step_val
    )


def _validate_query_step_val(*, step, step_key, step_oper, step_val):
    if not isinstance(step_val, QUERY_OPERS[step_oper]):
        raise InvalidQueryOperTypeException(
            attr_name=step_key,
            attr_oper=step_oper,
            attr_type=QUERY_OPERS[step_oper],
            attr_val=step_val,
        )

    if isinstance(step_val, list):
        for i, child_step_val in enumerate(step_val):
            # User Query Operator $eq to test against all allowed values for list items
            # IMPORTANT: Appending index to step_key is to prevent nested call from checking
            # step_key again and finding the value to be _id and trying to update step_val
            _validate_query_step_val(
                step=step,
                step_key=f"{step_key}.{i}",
                step_oper="$eq",
                step_val=child_step_val,
            )

    if isinstance(step_val, dict):
        for child_step_attr, child_step_val in step_val.items():
            if not isinstance(child_step_attr, str):
                # [TODO] Custom exception
                raise Exception()

            # User Query Operator $eq to test against all allowed values for dict values
            # IMPORTANT: Appending item key to step_key is to prevent nested call from checking
            # step_key again and finding the value to be _id and trying to update step_val
            _validate_query_step_val(
                step=step,
                step_key=f"{step_key}.{child_step_attr}",
                step_oper="$eq",
                step_val=child_step_val,
            )

    if step_key == "_id":
        if isinstance(step_val, list):
            step[step_key][step_oper] = [
                ObjectId(child_step_val) for child_step_val in step_val
            ]
            return

        if not isinstance(step_val, (str, ObjectId)):
            # [TODO] Custom exception
            raise Exception()

        step[step_key][step_oper] = ObjectId(step_val)


def _index_query_pipe(
    *,
    pipe: list[Union["NawahQueryStep", "NawahQueryOperOr", "NawahQueryOperAnd"]],
    special: "NawahQuerySpecial",
    index=dict[str, list[tuple[str, Any]]],
    path="",
):
    if not pipe:
        pipe = []

    if not special:
        special = {}

    for i, step in enumerate(pipe):
        _validate_query_step(step)

        step_key = list(step)[0]

        if step_key in ("$or", "$and"):
            _index_query_pipe(
                pipe=cast(Any, step)[step_key],
                special=special,
                index=index,
                path=f"{path}{i}.",
            )
            continue

        step_cond = step[step_key]  # type: ignore
        step_oper = list(step_cond)[0]
        wild_attr_name = f"{step_key}:*"
        query_attr_name = f"{step_key}:{step_oper}"
        if wild_attr_name not in index:
            index[wild_attr_name] = []
        if query_attr_name not in index:
            index[query_attr_name] = []
        index[wild_attr_name].append((f"{path}{i}", step_cond))
        index[query_attr_name].append((f"{path}{i}", step_cond))
