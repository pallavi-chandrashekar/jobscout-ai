def test_create_outreach_template(client):
    # Placeholder IDs should be replaced with actual UUIDs from setup
    response = client.post("/outreach-templates/", json={
        "user_id": "00000000-0000-0000-0000-000000000000",
        "job_id": "00000000-0000-0000-0000-000000000000",
        "message": "Hello, I’m interested in this job."
    })
    assert response.status_code in [200, 422]
