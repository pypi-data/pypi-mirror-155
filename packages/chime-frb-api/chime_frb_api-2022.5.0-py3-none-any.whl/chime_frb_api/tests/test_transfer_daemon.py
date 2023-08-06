"""Test the transfer daemon."""

import time

import pytest

from chime_frb_api.modules.results import Results
from chime_frb_api.workflow import Work
from chime_frb_api.workflow.daemons import transfer

buckets_kwargs = {
    "debug": True,
    "authentication": False,
    "base_url": "http://0.0.0.0:8000",
}

results_kwargs = {
    "debug": True,
    "authentication": False,
    "base_url": "http://0.0.0.0:8005",
}


@pytest.fixture()
def works():
    """Works fixture."""
    works = []
    for i in range(3):
        works.append(
            Work(
                pipeline=f"sample-{i}",
                event=[i, i + 1],
                tags=[f"{i}"],
                site="chime",
                archive=bool(i // 5),
                user="tester",
            ).payload
        )
    return works


def test_transfer_sucessful_work(works):
    """Tests workflow transfer daemon for successful work."""
    for work_payload in works:
        work = Work.from_dict(work_payload)
        work.deposit(**buckets_kwargs)

    withdrawn = Work.withdraw(pipeline="sample-0", **buckets_kwargs)
    withdrawn.status = "success"
    withdrawn.update(**buckets_kwargs)

    status = transfer.transfer_work(
        buckets_kwargs=buckets_kwargs, results_kwargs=results_kwargs
    )
    assert status == {"successful_work_transferred": True}


def test_transfer_failed_work():
    """Tests workflow transfer daemon for failed work."""
    withdrawn = Work.withdraw(pipeline="sample-1", **buckets_kwargs)
    withdrawn.status = "failure"
    withdrawn.attempt = withdrawn.retries
    withdrawn.update(**buckets_kwargs)

    status = transfer.transfer_work(
        buckets_kwargs=buckets_kwargs, results_kwargs=results_kwargs
    )
    assert status == {
        "failed_work_transferred": True,
    }


def test_delete_stale_work():
    """Tests workflow transfer daemon for stale work."""
    withdrawn = Work.withdraw(pipeline="sample-2", **buckets_kwargs)
    # Set creation time to be older than cutoff time (14 days)
    withdrawn.status = "failure"
    withdrawn.creation = time.time() - (60 * 60 * 24 * 14) - 1
    withdrawn.update(**buckets_kwargs)

    status = transfer.transfer_work(
        buckets_kwargs=buckets_kwargs, results_kwargs=results_kwargs
    )
    assert status == {
        "stale_work_deleted": True,
    }


def test_cleanup_results():
    """Tests workflow transfer daemon cleanup results."""
    results = Results(**results_kwargs)
    for i in range(2):
        pipeline_results = results.view(
            pipeline=f"sample-{i}",
            query={},
            projection={"id": True},
        )
        deletion_status = results.delete_ids(
            pipeline=f"sample-{i}", ids=[pipeline_results[0]["id"]]
        )
        assert deletion_status == {
            f"sample-{i}": True
        }, f"Clean up results failed for pipeline sample-{i}"
