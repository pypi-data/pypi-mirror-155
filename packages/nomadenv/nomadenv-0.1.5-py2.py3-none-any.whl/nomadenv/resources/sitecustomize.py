import traceback
import sys

def sitecustomize_main():
    import imp
    if sys.version_info[0] == 2:
        import importlib
        FinderBaseClass = object
        LoaderBaseClass = object
    else:
        import importlib.util
        import importlib.abc
        FinderBaseClass = importlib.abc.MetaPathFinder
        LoaderBaseClass = importlib.abc.Loader
    """
    For generating shebang pip is using using the sys.executable value  by default.
    This sitecustomize.py module install a MetaPathFinder in sys.meta_path to override
    the value in pip._vendor.distlib.scripts:ScriptMaker.executable when imported.
    This ensure all shebang are relative to the python environment.
    """

    # class DistlibMetaFinder(FinderBaseClass):
    #     """
    #     This MetaPathFinder subclasse is used to override the pip._vendor.distlib.scripts:ScriptMaker.executable value.
    #     """

    #     def find_module(self, fullname, path=None):
    #         if fullname != "pip._vendor.distlib.scripts":
    #             return
    #         for finder in sys.meta_path:
    #             print(finder)
    #             if finder is self:
    #                 continue
    #             loader = finder.find_module(fullname, path)
    #             print(finder, loader)
    #             if loader:
    #                 return self.get_loader(loader)
        
    #     def get_loader(self, base_loader):
    #         class DistlibLoader(LoaderBaseClass):

    #             def load_module(self, fullname):
    #                 module = base_loader.load_module(fullname)
    #                 self.patch_scripts_module(module)
    #                 print(module)
    #                 return module
                
    #             def patch_scripts_module(self, scripts_module):
    #                 scripts_module.ScriptMaker.executable = "$(dirname $(dirname \"$(readlink -f \"$0\")\"))/bin/python{}.{}".format(sys.version_info[0], sys.version_info[1])
                
    #             def create_module(self, spec):
    #                 mod = base_loader.create_module(spec)
    #                 self.patch_scripts_module(mod)
    #                 return mod

    #             def exec_module(self, module):
    #                 pass
    #         return DistlibLoader

    #     def find_spec(self, fullname, path, target=None):
    #         if fullname != "pip._vendor.distlib.scripts":
    #             return
    #         base_specs = None
    #         for finder in sys.meta_path:
    #             if finder == self:
    #                 continue
    #             if not hasattr(finder, "find_spec"):
    #                 continue
    #             specs = finder.find_spec(fullname, path, target)
    #             if not base_specs:
    #                 if specs:
    #                     base_specs = specs
    #         print(base_specs)
    #         return importlib.util.spec_from_loader(
    #             fullname, self.get_loader(base_specs)(), origin=base_specs.origin
    #         )


    class AbstractLoader(object):

        def patch_scripts_module(self, scripts_module):
            if sys.version_info[0] == 2 and sys.version_info[1] == 7 and sys.version_info[2] < 12:
                scripts_module.ScriptMaker.executable = """/bin/sh
'''exec' $(dirname $(dirname "$(readlink -f "$0")"))/bin/python{}.{} "$0" "$@"
' '''\n""".format(sys.version_info[0], sys.version_info[1])
            else:
                scripts_module.ScriptMaker.executable = "$(dirname $(dirname \"$(readlink -f \"$0\")\"))/bin/python{}.{}".format(sys.version_info[0], sys.version_info[1])
        
    class ModuleLoader(AbstractLoader):

        def __init__(self, fullname, path):
            super(ModuleLoader, self).__init__()
            self.fullname = fullname
            self.path = path
            if path is None:
                self.name = self.fullname
            else:
                self.name = fullname.rsplit('.', 1)[-1]
            self.infos = imp.find_module(self.name, path)
        
        
        def load_module(self, fullname):
            modfile, pathname, description = self.infos
            mod = imp.load_module(
                self.fullname,
                modfile,
                pathname,
                description,
            )
            
            self.patch_scripts_module(mod)
            return mod

    class SpecLoader(AbstractLoader):

        def __init__(self, base_specs):
            super(SpecLoader, self).__init__()
            self.base_specs = base_specs
        
        def load_module(self, fullname):
            mod = self.base_specs.loader.load_module(fullname)
            self.patch_scripts_module(mod)
            return mod
        
        def create_module(self, spec):
            mod = self.base_specs.loader.create_module(self.base_specs)
            self.patch_scripts_module(mod)
            return mod
    
    class DistlibMetaFinder(object):

        def find_module(self, fullname, path=None):
            if fullname != "pip._vendor.distlib.scripts":
                return
            loader = ModuleLoader(fullname, path)
            return loader
        
        def find_spec(self, fullname, path=None, target=None):
            if fullname != "pip._vendor.distlib.scripts":
                return
            base_specs = None
            for finder in sys.meta_path:
                if finder == self:
                    continue
                if not hasattr(finder, "find_spec"):
                    continue
                specs = finder.find_spec(fullname, path, target)
                if specs:
                    base_specs = specs
                    break
            loader = SpecLoader(base_specs)
            return importlib.util.spec_from_loader(
                fullname, loader, origin=base_specs.origin
            )

    DISTLIB_FINDER = DistlibMetaFinder()
    sys.meta_path.insert(0, DISTLIB_FINDER)
try:
    sitecustomize_main()
except Exception:
    sys.stderr.write("An error occured in sitecustomize.py ({})\n".format(__file__))
    sys.stderr.write(traceback.format_exc())