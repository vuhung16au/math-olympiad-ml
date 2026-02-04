from core.queue_controls import compute_queue_button_states


def test_controls_disabled_when_idle():
    s = compute_queue_button_states(solving=False, animating=False, paused=False)
    assert s["pause_enabled"] is False
    assert s["step_enabled"] is False
    assert s["cancel_enabled"] is False


def test_controls_while_solving_not_paused():
    s = compute_queue_button_states(solving=True, animating=False, paused=False)
    assert s["pause_enabled"] is True
    assert s["step_enabled"] is False
    assert s["cancel_enabled"] is True


def test_controls_while_paused():
    s = compute_queue_button_states(solving=True, animating=False, paused=True)
    assert s["pause_enabled"] is True
    assert s["step_enabled"] is True
    assert s["cancel_enabled"] is True

