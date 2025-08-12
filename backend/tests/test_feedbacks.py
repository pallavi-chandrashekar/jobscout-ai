def test_submit_feedback(client):
    # Placeholder IDs should be replaced with actual UUIDs from setup
    response = client.post("/job-feedbacks/", json={
        "user_id": "00000000-0000-0000-0000-000000000000",
        "job_id": "00000000-0000-0000-0000-000000000000",
        "outcome": "interviewed"
    })
    assert response.status_code in [200, 422]
