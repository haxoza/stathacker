import settings
from utils import load_from_string


def run():
    classes = [load_from_string(klass) for klass in settings.PLUGINS]
    callbacks = [load_from_string(klass) for klass in settings.CALLBACKS]
    for klass in classes:
        instance = klass()
        instance.run(settings.DOMAIN)
        results = instance.get_results()
        if results:
            for callback in callbacks:
                callback(instance, results)


if __name__ == '__main__':
    run()
