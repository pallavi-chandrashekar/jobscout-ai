def test_create_job_posting(client):
    response = client.post("/job-postings/", json={
        "url": "http://example.com/job",
        "title": "Software Engineer",
        "company": "Example Inc",
        "location": "Remote",
        "source": "LinkedIn",
        "trust_score": 85,
        "posted_date": "2025-07-27T00:00:00"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Software Engineer"
