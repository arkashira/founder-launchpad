from founder_launchpad import suggest_tech_stack, display_tech_stack
import pytest

def test_suggest_tech_stack():
    stack = suggest_tech_stack()
    assert len(stack.frontend) >= 1
    assert len(stack.backend) >= 1
    assert len(stack.database) >= 1
    assert len(stack.hosting_provider) >= 1
    for item in stack.frontend + stack.backend + stack.database + stack.hosting_provider:
        assert item.name
        assert item.description
        assert item.cost_estimate > 0

def test_display_tech_stack():
    stack = suggest_tech_stack()
    output = display_tech_stack(stack)
    assert "Frontend:" in output
    assert "Backend:" in output
    assert "Database:" in output
    assert "Hosting Provider:" in output
    for item in stack.frontend + stack.backend + stack.database + stack.hosting_provider:
        assert item.name in output
        assert item.description in output
        assert f"${item.cost_estimate:.2f}" in output

def test_empty_tech_stack():
    class EmptyTechStack:
        frontend = []
        backend = []
        database = []
        hosting_provider = []
    with pytest.raises(AttributeError):
        display_tech_stack(EmptyTechStack())
