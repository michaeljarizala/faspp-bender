import importlib
import pkgutil

package_name = __name__

for _, module_name, _ in pkgutil.iter_modules([__path__[0]]):
    importlib.import_module(f"{package_name}.{module_name}")
