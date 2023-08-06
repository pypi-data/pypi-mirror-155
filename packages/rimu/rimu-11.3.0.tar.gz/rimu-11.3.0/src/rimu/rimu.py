from rimu import api, options
from rimu.options import RenderOptions


def render(source: str, opts: RenderOptions = None) -> str:
    '''Exported render() API.'''
    if opts is None:
        opts = RenderOptions()
    # Implicit first-call API initialisation.
    if options.safeMode == -1:
        api.init()
    options.updateFrom(opts)
    return api.render(source)
