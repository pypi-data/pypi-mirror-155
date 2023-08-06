from os.path import dirname, basename, isfile
import glob

modules = glob.glob(dirname(__file__) + "/*.py")

__all__ = [basename(fich)[:-3] for fich in modules if isfile(fich)]
