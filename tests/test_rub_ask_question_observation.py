import os

def test_rub_ask_question_observation_artifact_exists():
    """
    Test that the observation period artifact for the ask_question UI lock during the Rub phase exists.
    """
    artifact_path = "artifacts/rub_ask_question_observation.md"
    assert os.path.exists(artifact_path), f"Observation artifact {artifact_path} must exist."
    
    with open(artifact_path, "r") as f:
        content = f.read()
        assert "hit-rate" in content.lower(), "Artifact must mention evaluating the hit-rate."
        assert "escape hatch" in content.lower(), "Artifact must mention the escape hatch."
