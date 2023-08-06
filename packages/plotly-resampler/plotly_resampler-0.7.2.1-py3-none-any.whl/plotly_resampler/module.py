from functools import wraps
from plotly_resampler import FigureResampler, FigureWidgetResampler

def register_express():
    import plotly.express
    
    px_funcnames = ['line', 'scatter']
    for funcname in px_funcnames:
        func = getattr(plotly.express, funcname)
        @wraps(func)
        def resampled_func(*args, **kwargs):
            return FigureResampler(func(*args, **kwargs))
        
        setattr(plotly.express, funcname, resampled_func)


import pandas as pd

# def get_x_y(args, kwargs):
#     if len(args):
#         if len(args) == 1:
#             data = args[0]
#             if isinstance(data, pd.DataFrame):
#                 if data.shape[1] == 1:
#                     data = data.values[:,0]
#                 else:

#                 pass

#     x = kwargs.get("x")
#     y = kwargs.get("y")
#     if isinstance(y, str):
#         y = args[0][y]
#     if isinstance(x, str):
#         x = args[0][x]
#     if y is None and len(args) == 1:
#         y = args[0]
#     return x, y, args, kwargs


def register_express_v2():
    import plotly.express
    
    px_funcnames = ['line', 'scatter']
    for funcname in px_funcnames:
        func = getattr(plotly.express, funcname)
        from inspect import getfullargspec
        print(getfullargspec(func))
        @wraps(func)
        def resampled_func(*args, **kwargs):
            # hf_x, hf_y = get_x_y(args, kwargs)
            # fig = 
            return FigureResampler(func(*args, **kwargs))
        
        setattr(plotly.express, funcname, resampled_func)

# def register_express_v2():
#     import plotly.express
    
#     px_funcnames = ['line', 'scatter']
#     for funcname in px_funcnames:
#         func = getattr(plotly.express, funcname)
#         @wraps(func)
#         def resampled_func(*args, **kwargs):
#             # print(args)
#             # print()
#             # print(kwargs)
#             # get_x_y(locals())
#             print(locals())
#             from plotly.express._core import apply_default_cascade
#             print(apply_default_cascade(locals()))
#             return FigureResampler(func(*args, **kwargs))
        
#         setattr(plotly.express, funcname, resampled_func)
