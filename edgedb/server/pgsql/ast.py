##
# Copyright (c) 2008-2012 MagicStack Inc.
# All rights reserved.
#
# See LICENSE for details.
##

import weakref

from edgedb.lang.common import datastructures, ast
from edgedb.lang.edgeql import ast as qlast


class Base(ast.AST):
    pass


class ArgListNode(Base):
    __fields = ['name', ('args', list)]


class BinOpNode(Base):
    __fields = ['left', 'op', 'right', ('aggregates', bool), ('strong', bool)]


class VarNode(Base):
    __fields = ['name']


class IdentNode(Base):
    __fields = ['name']


class PathVarNode(VarNode):
    pass


class LiteralExprNode(Base):
    __fields = ['expr']


class ConstantNode(Base):
    __fields = ['value', 'index', 'expr', 'type', 'origin_field']


class UnaryOpNode(Base):
    __fields = ['op', 'operand']


class PostfixOpNode(Base):
    __fields = ['op', 'operand']


class PredicateNode(Base):
    __fields = [('expr', Base, None)]


class NullTestNode(Base):
    __fields = [('expr', Base)]


class SelectExprNode(Base):
    __fields = ['expr', 'alias', 'filter_expr']


class FromExprNode(Base):
    __fields = ['expr', 'alias']


class FuncAliasNode(Base):
    __fields = ['alias', 'elements']


class TableFuncElement(Base):
    __fields = ['name', 'type']


class RelationNode(Base):
    __fields = [
        ('concepts', frozenset),
        'alias',
        ('_bonds', dict),
        ('edgedbnode', object, None, True, None, True),
        ('outerbonds', list),
        ('proxyouterbonds', dict),
        ('aggregates', bool),
        'coldef']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._bonds = {}

    def bonds(self, key):
        bonds = self._bonds.get(key)
        if bonds:
            return list(bonds)

    def addbond(self, key, bond):
        if key not in self._bonds:
            self._bonds[key] = [bond]
        else:
            self._bonds[key].append(bond)

        return bond

    def updatebonds(self, node):
        for key, values in node._bonds.items():
            if key not in self._bonds:
                self._bonds[key] = list(values)
            else:
                self._bonds[key].extend(values)


class PseudoRelationNode(RelationNode):
    __fields = ['name']


class TableNode(RelationNode):
    __fields = ['name', 'schema']


class TableQueryNode(RelationNode):
    __fields = ['name', 'schema']


class SelectQueryNode(RelationNode):
    __fields = [
        'distinct', ('fromlist', list), ('targets', list), 'where',
        'where_weak', 'where_strong', ('from_only', bool), ('values', list),
        ('orderby', list), 'offset', 'limit', ('groupby', list), 'having',
        ('ctes', datastructures.OrderedSet), ('concept_node_map', dict),
        ('link_node_map', dict), ('linkmap', dict),
        ('subquery_referrers', list), 'op', 'larg', 'rarg', 'recursive',
        'text_override',
        'scls_rel',
        'rptr_rel'
    ]


class DMLNode(Base):
    pass


class OnConflictNode(Base):
    __fields = ['action', 'infer', ('targets', list), 'where']


class InsertQueryNode(DMLNode):
    __fields = [
        'fromexpr', ('cols', list), 'select', ('targets', list),
        ('subquery_referrers', list), 'alias',
        ('ctes', datastructures.OrderedSet),
        ('on_conflict', OnConflictNode, None),
        ('concept_node_map', dict)
    ]


class UpdateQueryNode(DMLNode):
    __fields = [
        'fromexpr', ('values', list), 'where', ('targets', list),
        ('subquery_referrers', list), ('ctes', datastructures.OrderedSet),
        ('concept_node_map', dict),
        'alias'
    ]


class UpdateExprNode(Base):
    __fields = ['expr', 'value']


class DeleteQueryNode(DMLNode):
    __fields = [
        'fromexpr', 'where', ('targets', list), ('subquery_referrers', list),
        ('ctes', datastructures.OrderedSet), 'alias', ('using', list),
        ('concept_node_map', dict)
    ]


class CompositeNode(RelationNode):
    __fields = [('queries', list), ('ctes', datastructures.OrderedSet),
                ('concept_node_map', dict)]


class CTENode(SelectQueryNode):
    __fields = [('referrers', weakref.WeakSet)]


class CTERefNode(Base):
    __fields = ['cte']


class CTEAttrRefNode(Base):
    __fields = ['cte', 'attr']


class JoinNode(RelationNode):
    __fields = ['left', 'right', 'condition', 'type']

    def copy(self):
        result = self.__class__()
        result.copyfrom(self)
        return result

    def copyfrom(self, other):
        self.left = other.left
        self.right = other.right
        self.condition = other.condition
        self.type = other.type


class ExistsNode(Base):
    __fields = ['expr']


class FieldRefNode(Base):
    __fields = ['table', 'field', 'origin', 'origin_field', 'indirection']


class SequenceNode(Base):
    __fields = [('elements', list)]


class SortExprNode(Base):
    __fields = ['expr', 'direction', 'nulls_order']


class FunctionCallNode(Base):
    __fields = [
        'name', ('args', list), 'over', ('aggregates', bool),
        ('noparens', bool), 'agg_sort', 'agg_filter'
    ]


class WindowDefNode(Base):
    __fields = ['partition', ('orderby', list), 'frame']


class IgnoreNode(Base):
    pass


class ArrayNode(Base):
    __fields = [('elements', list)]


class TypeCastNode(Base):
    __fields = ['expr', 'type']


class ParamRefNode(Base):
    __fields = ['param']


class IndirectionNode(Base):
    __fields = ['expr', 'indirection']


class RowExprNode(Base):
    __fields = [('args', list), 'origin_field']


class TypeNode(Base):
    __fields = ['name', 'typmods', 'array_bounds', ('setof', bool)]


class StarIndirectionNode(Base):
    pass


class IndexIndirectionNode(Base):
    __fields = ['lower', 'upper']


class CaseExprNode(Base):
    __fields = ['arg', 'args', 'default', 'filter_expr']


class CaseWhenNode(Base):
    __fields = ['expr', 'result']


class CollateClauseNode(Base):
    __fields = ['expr', 'collation_name']


class PgSQLOperator(ast.ops.Operator):
    pass


class PgSQLComparisonOperator(PgSQLOperator, ast.ops.ComparisonOperator):
    pass


LIKE = PgSQLComparisonOperator('~~')
NOT_LIKE = PgSQLComparisonOperator('!~~')
ILIKE = PgSQLComparisonOperator('~~*')
NOT_ILIKE = PgSQLComparisonOperator('!~~*')
SIMILAR_TO = PgSQLComparisonOperator('~')
NOT_SIMILAR_TO = PgSQLComparisonOperator('!~')
IS_DISTINCT = PgSQLComparisonOperator('IS DISTINCT')
IS_NOT_DISTINCT = PgSQLComparisonOperator('IS NOT DISTINCT')
IS_OF = PgSQLComparisonOperator('IS OF')
IS_NOT_OF = PgSQLComparisonOperator('IS NOT OF')


class PgSQLSetOperator(PgSQLOperator):
    pass


UNION = PgSQLSetOperator('UNION')
INTERSECT = PgSQLSetOperator('INTERSECT')
EXCEPT = PgSQLSetOperator('EXCEPT')

SortAsc = qlast.SortAsc
SortDesc = qlast.SortDesc
SortDefault = qlast.SortDefault

NullsFirst = qlast.NonesFirst
NullsLast = qlast.NonesLast
