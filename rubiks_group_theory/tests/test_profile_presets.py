from core.profile_presets import get_profile_settings


def test_teaching_profile_settings():
    s = get_profile_settings("teaching")
    assert s["animation_duration_ms"] == 320
    assert s["solution_delay"] == 650
    assert s["compact_ui"] is False
    assert s["show_explanations"] is True


def test_speed_profile_settings():
    s = get_profile_settings("speed")
    assert s["animation_duration_ms"] == 120
    assert s["solution_delay"] == 120
    assert s["compact_ui"] is True
    assert s["show_explanations"] is False

