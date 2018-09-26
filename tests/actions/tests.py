import os
import importlib

from shortcuts import actions
from tests.conftest import ActionTomlLoadsMixin


class TestActions:
    def test_all_actions_must_be_imported_in_the_init(self):
        """
        checks that all subclasses of BaseAction in files `shortcuts/actions/*.py`
        are imported in the `shortcuts/actions/__init__.py`
        """
        lib_actions = self._get_actions_from_module(actions)  # actions from shortcuts/actions/__init__.py

        files = os.listdir(os.path.dirname(actions.__file__))
        for module in files:
            if module == '__init__.py':
                continue
            module_name, ext = os.path.splitext(module)
            if ext != '.py':
                continue

            imported_module = importlib.import_module(f'shortcuts.actions.{module_name}')
            module_actions = self._get_actions_from_module(imported_module)

            msg = 'Seems like you have actions which are not imported in `shortcuts.actions.__init__.py`'
            assert module_actions - lib_actions == set(), msg

    def _get_actions_from_module(self, module):
        """Returns subclasses of the BaseAction from module"""
        module_actions = []
        for name, cls in module.__dict__.items():
            if isinstance(cls, type) and issubclass(cls, actions.BaseAction) and cls.keyword:
                module_actions.append(cls)
        return set(module_actions)


class TestURLEncodeAction(ActionTomlLoadsMixin):
    def test_dumps(self):
        action = actions.URLEncodeAction()
        exp_dump = {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.urlencode',
            'WFWorkflowActionParameters': {
                'WFEncodeMode': 'Encode',
            }
        }
        assert action.dump() == exp_dump

    def test_loads_toml(self):
        toml = f'''
        [[action]]
        type = "urlencode"
        '''
        self._assert_toml_loads(toml, actions.URLEncodeAction, {})


class TestURLDecodeAction(ActionTomlLoadsMixin):
    def test_dumps(self):
        action = actions.URLDecodeAction()
        exp_dump = {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.urlencode',
            'WFWorkflowActionParameters': {
                'WFEncodeMode': 'Decode',
            }
        }
        assert action.dump() == exp_dump

    def test_loads_toml(self):
        toml = f'''
        [[action]]
        type = "urldecode"
        '''
        self._assert_toml_loads(toml, actions.URLDecodeAction, {})
