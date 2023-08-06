from .handler import FileHandler, Serializer


@Serializer.register_handler("json")
class JsonHandler(FileHandler):
    def load(self, path: str) -> dict:
        import json as _json

        with open(path, "r") as f:
            return _json.load(f)

    def dump(self, data: dict, path: str) -> None:
        import json as _json

        with open(path, "w") as f:
            _json.dump(data, f, sort_keys=False, indent=4)


@Serializer.register_handler(["yaml", "yml"])
class YamlHandler(FileHandler):
    def load(self, path: str) -> dict:
        try:
            from ruamel.yaml import YAML

            _yaml = YAML()
            _yaml.indent(mapping=4, sequence=6, offset=3)
            with open(path, "r") as f:
                return _yaml.load(f)
        except ModuleNotFoundError:
            import yaml as _yaml

            with open(path, "r") as f:
                return _yaml.safe_load(f)

    def dump(self, data: dict, path: str) -> None:
        try:
            from ruamel.yaml import YAML

            _yaml = YAML()
            _yaml.indent(mapping=4, sequence=6, offset=3)
        except ModuleNotFoundError:
            import yaml as _yaml

        with open(path, "w") as f:
            _yaml.dump(data, f)


@Serializer.register_handler("pkl")
class PickleHandler(FileHandler):
    def load(self, path: str) -> dict:
        import pickle as _pickle

        with open(path, "w") as f:
            return _pickle.load(f)

    def dump(self, data: dict, path: str) -> None:
        import pickle as _pickle

        with open(path, "w") as f:
            _pickle.dump(data, f)


@Serializer.register_handler("toml")
class TomlHandler(FileHandler):
    def load(self, path: str) -> dict:
        import toml as _toml

        with open(path, "r") as f:
            return _toml.load(f)

    def dump(self, data: dict, path: str) -> None:
        import toml as _toml

        from .helpers import MultilinePreferringTomlEncoder

        with open(path, "w") as f:
            _toml.dump(data, f, MultilinePreferringTomlEncoder())


@Serializer.register_handler(["", "txt"])
class PlanTextHandler(FileHandler):
    def load(self, path: str) -> dict:
        with open(path, "r") as f:
            return {"data": f.readlines()}

    def dump(self, data: dict, path: str) -> None:
        if "data" not in data:
            raise ValueError("keyword 'data' must be in the dictionary.")
        with open(path, "w") as f:
            f.writelines(data["data"])
