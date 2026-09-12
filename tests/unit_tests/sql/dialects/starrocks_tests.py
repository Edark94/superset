# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import pytest
import sqlglot
from sqlglot import exp

from superset.sql.dialects.starrocks import (
    _STARROCKS_AGGREGATE_COLUMN_CONSTRAINTS,
    StarRocks,
    StarRocksParser,
)


@pytest.mark.parametrize("keyword", _STARROCKS_AGGREGATE_COLUMN_CONSTRAINTS)
def test_aggregate_column_constraint_parsers_bind_keyword(keyword: str) -> None:
    """
    Each aggregate-column keyword must map to a parser returning its own name.
    """
    parser = StarRocksParser.CONSTRAINT_PARSERS[keyword]
    result = parser(StarRocksParser())

    assert isinstance(result, exp.Var)
    assert result.name == keyword


@pytest.mark.parametrize("keyword", _STARROCKS_AGGREGATE_COLUMN_CONSTRAINTS)
def test_aggregate_column_constraint_round_trip(keyword: str) -> None:
    sql = f"CREATE TABLE t (k1 INT, v1 BIGINT {keyword})"
    ast = sqlglot.parse_one(sql, StarRocks)

    constraints = [c.sql(StarRocks) for c in ast.find_all(exp.ColumnConstraint)]
    assert constraints == [keyword]
    assert ast.sql(StarRocks) == sql
