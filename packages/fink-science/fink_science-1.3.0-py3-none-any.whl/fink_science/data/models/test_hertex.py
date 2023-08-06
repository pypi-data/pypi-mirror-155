import jpype
import jpype.imports
import glob

# just a pointer to janusgraph jars
jarpath = glob.glob('../../janusgraph_libs/*.jar')
jarpath.append('FinkBrowser.exe.jar')

jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", classpath=jarpath, convertStrings=True)

import java.lang
import java.util

from com.Lomikel.Januser import GremlinClient
from com.astrolabsoftware.FinkBrowser.Utils import Init
Init.init()

client = GremlinClient("134.158.74.85", 24444);

g = client.g();
print(g.V().hasLabel('alert').limit(1).valueMap().next());

client.close()
