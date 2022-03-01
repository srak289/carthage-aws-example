from carthage import *
from carthage.config import ConfigLayout
from carthage.modeling import *

from .layout import layout as example

@inject(injector=Injector)
def carthage_plugin(injector):
    injector.add_provider(InjectionKey(CarthageLayout, layout_name="carthage_aws_example"), example)
    