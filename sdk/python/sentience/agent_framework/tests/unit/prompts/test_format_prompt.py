from sentience.agent_framework.agents.prompts import format_prompt


async def test_basic():
    template = "{{value1}} {{value2}}!"
    state = {
        "value1": "Hello",
        "value2": "world",
    }
    result = format_prompt.execute(template, state)
    assert result == "Hello world!"


async def test_repeating_values():
    template = "{{value1}} {{value1}} {{value2}} {{value2}}!"
    state = {
        "value1": "Hello",
        "value2": "world",
    }
    result = format_prompt.execute(template, state)
    assert result == "Hello Hello world world!"


async def test_extra_values():
    template = "{{value1}} {{value2}}!"
    state = {
        "value1": "Hello",
        "value2": "world",
        "value3": "asd",
    }
    result = format_prompt.execute(template, state)
    assert result == "Hello world!"
