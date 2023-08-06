# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['definite']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'definite',
    'version': '1.0.0',
    'description': 'Simple finite state machines.',
    'long_description': '# `definite`\n\nSimple finite state machines.\n\nPerfect for representing workflows.\n\n\n## Quickstart\n\n```python\nfrom definite import FSM\n\n# You define all the valid states, as well as what their allowed\n# transitions are.\nclass Workflow(FSM):\n    allowed_transitions = {\n        "draft": ["awaiting_review", "rejected"],\n        "awaiting_review": ["draft", "reviewed", "rejected"],\n        "reviewed": ["published", "rejected"],\n        "published": None,\n        "rejected": ["draft"],\n    }\n    default_state = "draft"\n\n# Right away, you can use the states/transitions as-is to enforce changes.\nworkflow = Workflow()\nworkflow.current_state() # "draft"\n\nworkflow.transition_to("awaiting_review")\nworkflow.transition_to("reviewed")\n\nworkflow.is_allowed("published") # True\n\n# Invalid/disallowed transitions will throw an exception.\nworkflow.current_state() # "reviewed"\n# ...which can only go to "published" or "rejected", but...\nworkflow.transition_to("awaiting_review")\n# Traceback (most recent call last):\n# ...\n# workflow.TransitionNotAllowed: "reviewed" cannot transition to "awaiting_review"\n\n\n# Additionally, you can set up extra code to fire on given state changes.\nclass Workflow(FSM):\n    # Same transitions & default state.\n    allowed_transitions = {\n        "draft": ["awaiting_review", "rejected"],\n        "awaiting_review": ["draft", "reviewed", "rejected"],\n        "reviewed": ["published", "rejected"],\n        "published": None,\n        "rejected": ["draft"],\n    }\n    default_state = "draft"\n\n    # Define a `handle_<state_name>` method on the class.\n    def handle_awaiting_review(self, new_state):\n        spell_check_results = check_spelling(self.obj.content)\n        msg = (\n            f"{self.obj.title} ready for review. "\n            f"{len(spell_check_results)} spelling errors."\n        )\n        send_email(to=editor_email, message=msg)\n\n    def handle_published(self, new_state):\n        self.obj.pub_date = datetime.datetime.utcnow()\n        self.obj.save()\n\n    # You can also setup code that fires on **ANY** valid transition with the\n    # special `handle_any` method.\n    def handle_any(self, new_state):\n        self.obj.state = new_state\n        self.obj.save()\n\n\n# We can pull in any Python object, like a database-backed model, that we\n# want to associate with our FSM.\nfrom news.models import NewsPost\nnews_post = NewsPost.objects.create(\n    title="Hello world!",\n    content="This iz our frist post!",\n    state="draft",\n)\n\n# We start mostly the same, but this time pass an `obj` kwarg!\nworkflow = Workflow(obj=news_post)\n\n# If you wanted to be explicit, you could also pass along the `initial_state`:\nworkflow = Workflow(\n    obj=news_post,\n    initial_state=news_post.state\n)\n\nworkflow.current_state() # "draft"\n\n# But when we trigger this change...\nworkflow.transition_to("awaiting_review")\n# ...it triggers the spell check & the email we defined above, as well as\n# hitting the `handle_any` method & updating the `state` field in the DB.\nnews_post.refresh_from_db()\nnews_post.state # "awaiting_review" !\n```\n\n\n## Installation\n\n`pip install definite`\n\n\n## Requirements\n\n* Python 3.6+\n\n\n## Testing\n\n`$ pytest .`\n\n\n## License\n\nNew BSD\n',
    'author': 'Daniel Lindsley',
    'author_email': 'daniel@toastdriven.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/toastdriven/definite',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
