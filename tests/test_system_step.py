#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `system_step` package."""

import pytest  # noqa: F401
import system_step  # noqa: F401


def test_construction():
    """Just create an object and test its type."""
    result = system_step.System()
    assert str(type(result)) == (
        "<class 'system_step.system.System'>"  # noqa: E501
    )
