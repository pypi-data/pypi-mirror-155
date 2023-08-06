"""Test the work object."""

import pytest

from chime_frb_api.workflow import Work


def test_bad_instantiation():
    """Test that the work object can't be instantiated without a pipeline."""
    with pytest.raises(TypeError):
        Work()


def test_bad_pipeline():
    """Test that the work object can't be instantiated with empty pipeline."""
    with pytest.raises(ValueError):
        Work(pipeline="", parameters={})


def test_post_init_set():
    """Test post init assignment."""
    work = Work(pipeline="test")
    work.parameters = {}


def test_work_lifecycle():
    """Test that the work cannot be mutated between deposit and fetch stages."""
    work = Work(pipeline="test")
    work_again = Work(**work.payload)
    assert work.payload == work_again.payload


def test_json_serialization():
    """Test that the work can be serialized to JSON."""
    work = Work(pipeline="test")
    assert work.json is not None
    assert isinstance(work.json, str)


def test_check_work_payload():
    """Test that the work payload is correct."""
    work = Work(pipeline="test", parameters={"hi": "low"})
    assert work.payload["pipeline"] == "test"
    assert work.payload["parameters"] == {"hi": "low"}


def test_make_work_from_dict():
    """Test that the work object can be instantiated from a dictionary."""
    work = Work(pipeline="test", parameters={"hi": "low"})
    work_from_dict = Work.from_dict(work.payload)
    work_from_json = Work.from_json(work.json)
    assert work == work_from_dict == work_from_json


def test_validation_after_instantiation():
    """Check if work validation works after instantiation."""
    work = Work(pipeline="a")
    with pytest.raises(TypeError):
        work.pipeline = 2
    with pytest.raises(TypeError):
        work.parameters = 2
