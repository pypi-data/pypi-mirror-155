"""Main entry for react-native.

Provides functionality similar to the App component in an App.js file.

Note:
    Using AppProxy as an iterator to traverse Component tree.
"""
import json
import logging
import subprocess
from typing import Optional, List, Any
from collections.abc import Iterable, Iterator

from sweetpotato.app import App
from sweetpotato.config import settings


class AppIterator(Iterator):
    """
    Concrete Iterators implement various traversal algorithms. These classes
    store the current traversal position at all times.
    """


    _position: int = None
    _reverse: bool = False

    def __init__(self, collection, reverse: bool = False) -> None:
        self._collection = collection
        self._reverse = reverse
        self._position = -1 if reverse else 0

    def __next__(self):
        """
        The __next__() method must return the next item in the sequence. On
        reaching the end, and in subsequent calls, it must raise StopIteration.
        """
        try:
            value = self._collection[self._position]
            self._position += -1 if self._reverse else 1
        except IndexError:
            raise StopIteration()

        return value


class AppTree(Iterable):
    """
    Concrete Collections provide one or several methods for retrieving fresh
    iterator instances, compatible with the collection class.
    """

    def __init__(self, collection=None) -> None:
        if collection is None:
            collection = []
        self._collection = collection

    def __iter__(self) -> AppIterator:
        """
        The __iter__() method returns the iterator object itself, by default we
        return the iterator in ascending order.
        """
        return AppIterator(self._collection)

    def get_reverse_iterator(self) -> AppIterator:
        return AppIterator(self._collection, True)

    def add_item(self, item: Any):
        self._collection.append(item.write_component())


class AppProxy:
    """Main entry for react-native.

    Keyword Args:
        theme: UI Kitten theme, may be 'dark' or 'light'.
        state: App state, see `https://reactnative.dev/docs/state`.

    Attributes:
        _app_repr: String representation of App.js file.

    Todo:
        * Refactor away from the Component parent.
    """

    def __init__(
            self,
            theme: Optional[str] = None,
            state: Optional[dict] = None,
            children: Optional[list] = None,
    ) -> None:
        if state is None:
            state = {}
        if theme is None:
            theme = {}
        application = App(theme=theme, state=state, children=children)
        collection = AppTree()
        print(list(map(collection.add_item, application._children)))
        # for i in application._children:
        #     collection.add_item(i)


        print(list(collection))
        self._app_repr = settings.APP_REPR

    def write_state(self) -> str:
        """Writes App component state inside App.js file in JSON format.

        Returns:
            String representation of App component state.
        """
        return "".join([f"{k}: {json.dumps(v)},\n" for k, v in self._state.items()])

    def write_import(self) -> dict:
        """Gathers child components and self imports.

        Returns:
            All child imports.

        Todo:
            * Remove hard coding of imports.
        """
        imports = {
            self._package: self._react_component,
            "react-native-safe-area-context": "SafeAreaProvider",
            "'./src/components/RootNavigation'": "* as RootNavigation",
            "@react-native-async-storage/async-storage": "AsyncStorage",
            "expo-secure-store": "* as SecureStore",
        }

        if settings.USE_UI_KITTEN:
            imports["@ui-kitten/components"] = "ApplicationProvider"
            imports["@eva-design/eva"] = "* as eva"
        if settings.USE_AUTHENTICATION:
            imports["./src/Login.js"] = "Login"
            imports["@react-navigation/native-stack"] = "createNativeStackNavigator"
        imports["@react-navigation/native"] = "NavigationContainer"

        return imports

    def write_imports(self) -> str:
        """Writes react-native imports to App.js file.

        Returns:
            String representation of all imports.
        """
        import_dict = {}
        imports = [child.write_import() for child in self._children]
        imports.append(self.write_import())
        for item in imports:
            for key, value in item.items():
                if key not in import_dict:
                    import_dict[key] = set()
                import_dict[key].add(value)

        import_str = ""
        for key, value in import_dict.items():
            if list(value)[0] in [
                "* as RootNavigation",
                "* as eva",
                "* as SecureStore",
                "AsyncStorage",
            ]:
                value = list(value)[0]
            import_str += f'import {value} from "{key}";'.replace("'", "")
        return import_str

    def write_variables(self) -> str:
        """Writes const variables (if present) to App.js file.

        Returns:
            String representation of all variables.
        """
        variables = "\n".join(set(child.write_variables() for child in self._children))
        if settings.USE_AUTHENTICATION:
            variables += "\nconst Stack = createNativeStackNavigator();"
        return variables

    def write_file(self) -> None:
        """
        Writes formats all .js files

        Returns:
            None
        """
        with open(
                f"{settings.REACT_NATIVE_PATH}/App.js", "w", encoding="utf-8"
        ) as file:
            file.write(self._app_repr)
        try:
            subprocess.run(
                f"cd {settings.REACT_NATIVE_PATH} && yarn prettier",
                shell=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            logging.warning(f"{e}\nTrying yarn install...")
            subprocess.run(
                f"cd {settings.REACT_NATIVE_PATH} && yarn install",
                shell=True,
                check=True,
            )
            self.write_file()

    def compile_app(self) -> None:
        """Calls all relevant methods to write App.js file.

        Returns:
            None
        """
        self._app_repr = self._app_repr.replace("<IMPORTS>", self.write_imports())
        self._app_repr = self._app_repr.replace("<FUNCTIONS>", self.write_functions())
        self._app_repr = self._app_repr.replace("<VARIABLES>", self.write_variables())
        self._app_repr = self._app_repr.replace("<APP>", self.write_component())
        self._app_repr = self._app_repr.replace("<STATE>", self.write_state())
        self.write_file()

    def run(self) -> None:
        """Starts a React native expo client through a subprocess.

        Returns:
            None
        """
        self.compile_app()
        subprocess.run(
            f"cd {settings.REACT_NATIVE_PATH} && expo start",
            shell=True,
            check=True,
        )


