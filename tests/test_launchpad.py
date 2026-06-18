from launchpad import Launchpad, Idea, Template, Metric

def test_validate_idea():
    launchpad = Launchpad()
    idea = Idea("My Web App", "A web app for selling products")
    assert launchpad.validate_idea(idea) == "Idea validated successfully"

def test_validate_idea_invalid():
    launchpad = Launchpad()
    idea = Idea("", "A web app for selling products")
    assert launchpad.validate_idea(idea) == "Invalid idea: name and description are required"

def test_get_templates():
    launchpad = Launchpad()
    templates = launchpad.get_templates()
    assert len(templates) == 2
    assert templates[0].name == "Web App"
    assert templates[1].name == "Mobile App"

def test_get_dashboard():
    launchpad = Launchpad()
    idea = Idea("My Web App", "A web app for selling products")
    launchpad.validate_idea(idea)
    metrics = launchpad.get_dashboard()
    assert len(metrics) == 1
    assert metrics[0].name == "Number of Ideas"
    assert metrics[0].value == 1
