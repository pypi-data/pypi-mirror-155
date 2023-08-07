#!/usr/bin/env python3

"""
** Help for the documentation. **
---------------------------------

The *deformation* documentation is made to be generated automatically from the *pdoc3* tool.

* If you want to generate the documentation yourself, please follow the steps below:
    * *install pdoc3* : ``pip install pdoc3``
    * *generate documentation* :
        ``pdoc3 deformation/ -c latex_math=True --force --http localhost:8080``
    * *display documentation* : in a browser, explore http://localhost:8080/deformation/
* If you want to consult the official documentation:
    * Go to the site http://python-docs.ddns.net/deformation/.
"""

import inspect


def make_pdoc(obj_names, obj_refs):
    """
    ** Allows to simplify the description of object aliases. **

    Parameters
    ----------
    obj_names : list
        The list of object names, often the constant *__all__*.
    obj_refs : dict
        To each object name, associate the object itself.
        This dictionary can be retrieved with *globals()* or *locals()*.

    Returns
    -------
    __pdoc__ : dict
        Each object or attribute name is associated with
        a short description that refers to the full description.
        This dictionary must be associated to the variable __pdoc__ which is interpreted by *pdoc3*.
    """
    def path(obj_refs, obj):
        return (
            inspect.getsourcefile(obj_refs[obj]).split('deformation/')[-1][:-3]
            .replace('/', '.')
            .replace('.__init__', '')
        )
    return {
        **{
            obj: f'Alias to ``deformation.{path(obj_refs, obj)}.{obj}``'
            for obj in obj_names
            if inspect.ismodule(obj_refs[obj]) or inspect.isclass(obj_refs[obj])
            or inspect.ismethod(obj_refs[obj]) or inspect.isfunction(obj_refs[obj])
        },
        **{
            f'{cl}.{meth}': False
            for cl in obj_names
            if inspect.isclass(obj_refs[cl])
            for meth in obj_refs[cl].__dict__
            if not meth.startswith('_')
        },
    }
