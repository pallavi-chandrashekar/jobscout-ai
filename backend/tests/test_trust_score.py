import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

from app.services.trust_score import (
    compute_trust_score, _freshness_score, _feedback_score,
    _company_score, _quality_score,
)


class MockJobPosting:
    def __init__(self, **kwargs):
        self.title = kwargs.get("title")
        self.company = kwargs.get("company")
        self.company_url = kwargs.get("company_url")
        self.location = kwargs.get("location")
        self.description = kwargs.get("description")
        self.source = kwargs.get("source")
        self.salary_min = kwargs.get("salary_min")
        self.salary_max = kwargs.get("salary_max")
        self.posted_date = kwargs.get("posted_date")
        self.is_active = kwargs.get("is_active", True)


class MockFeedback:
    def __init__(self, outcome):
        self.outcome = outcome


class TestFreshnessScore:
    def test_inactive_posting(self):
        assert _freshness_score(datetime.now(timezone.utc), False) == 0

    def test_no_posted_date(self):
        assert _freshness_score(None, True) == 10

    def test_fresh_posting(self):
        recent = datetime.now(timezone.utc) - timedelta(days=3)
        assert _freshness_score(recent, True) == 25

    def test_stale_posting(self):
        old = datetime.now(timezone.utc) - timedelta(days=120)
        assert _freshness_score(old, True) == 2


class TestFeedbackScore:
    def test_no_feedbacks(self):
        assert _feedback_score([]) == 17

    def test_all_hired(self):
        feedbacks = [MockFeedback("hired")] * 5
        score = _feedback_score(feedbacks)
        assert score == 35

    def test_all_fake(self):
        feedbacks = [MockFeedback("fake")] * 5
        score = _feedback_score(feedbacks)
        assert score == 0

    def test_mixed_feedbacks(self):
        feedbacks = [MockFeedback("hired"), MockFeedback("ghosted"), MockFeedback("interviewed")]
        score = _feedback_score(feedbacks)
        assert 10 <= score <= 30


class TestCompanyScore:
    def test_no_info(self):
        assert _company_score(None, None) == 0

    def test_full_info(self):
        assert _company_score("Acme Corp", "https://acme.com") == 15

    def test_name_only(self):
        assert _company_score("Acme Corp", None) == 5


class TestQualityScore:
    def test_high_quality(self):
        job = MockJobPosting(
            title="Senior Software Engineer",
            location="Remote",
            description="A" * 200,
            salary_min=100000,
            source="linkedin",
        )
        score = _quality_score(job)
        assert score >= 20

    def test_red_flags(self):
        job = MockJobPosting(
            title="urgently hiring - guaranteed income",
            description="be your own boss and earn $$$",
        )
        score = _quality_score(job)
        assert score <= 5

    def test_empty_posting(self):
        job = MockJobPosting()
        score = _quality_score(job)
        assert score >= 0


class TestComputeTrustScore:
    def test_returns_detail(self):
        job = MockJobPosting(
            title="Engineer", company="Acme", company_url="https://acme.com",
            posted_date=datetime.now(timezone.utc) - timedelta(days=5),
            source="linkedin", salary_min=100000,
            description="A great role " * 20, location="Remote",
        )
        feedbacks = [MockFeedback("hired"), MockFeedback("interviewed")]
        result = compute_trust_score(job, feedbacks)
        assert 0 <= result.total <= 100
        assert result.confidence == "low"
        assert result.freshness_score == 25
        assert result.company_score == 15

    def test_high_confidence(self):
        job = MockJobPosting(title="Test", company="Test")
        feedbacks = [MockFeedback("hired")] * 15
        result = compute_trust_score(job, feedbacks)
        assert result.confidence == "high"
