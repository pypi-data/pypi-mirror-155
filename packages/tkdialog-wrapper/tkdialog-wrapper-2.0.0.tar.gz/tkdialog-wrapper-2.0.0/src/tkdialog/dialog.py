from pathlib import Path
import pickle

import tkinter as tk
import tkinter.filedialog as tkfiledialog
from typing import Any, Callable, Optional, Union, Dict


def open_dialog(ext: Optional[str] = None,
                initialdir: Union[str, Path] = '.',
                **kwargs) -> str:
    """Make a file open dialog

    Parameters
    ----------
    ext : str
        A default extension of the dialog.
        The first character must be period.
    initialdir : str or pathlib.Path, default='.'
        An initial directory of the dialog

    kwargs will be passed to `tkinter.filedialog.askopenfilename`.
    See also [tkinter document](https://tkdocs.com/shipman/tkFileDialog.html).

    Returns
    --------
    str
        the selected filename
        If the dialog is canceled, an empty string is returned.
    """
    opt_default: Dict[str, Any] = {}

    if initialdir is None:
        initialdir = Path.cwd()
    opt_default['initialdir'] = Path(initialdir)

    if ext is not None:
        if str(ext)[0] != '.':
            raise RuntimeError('The first character must be period.')
        opt_default['defaultextension'] = ext
        opt_default['filetypes'] = [('', '*' + ext),
                                    ('all', '*')]

    _opt = dict(opt_default, **kwargs)

    root = tk.Tk()
    root.withdraw()
    root.wm_attributes("-topmost", True)

    return tkfiledialog.askopenfilename(**_opt)


def saveas_dialog(ext: Optional[str] = None,
                  initialdir: Union[str, Path] = '.',
                  **kwargs) -> str:
    """Make a file save dialog

    Parameters
    ----------
    ext : str
        A default extension of the dialog.
        The first character must be period.
    initialdir : str or pathlib.Path, default='.'
        An initial directory of the dialog

    kwargs will be passed to `tkinter.filedialog.askopenfilename`.
    See also [tkinter document](https://tkdocs.com/shipman/tkFileDialog.html).

    Returns
    --------
    str
        the selected filename
        If the dialog is canceled, an empty string is returned.
    """
    opt_default: Dict[str, Any] = {}

    if initialdir is None:
        initialdir = Path.cwd()
    opt_default['initialdir'] = Path(initialdir)

    if ext is not None:
        if str(ext)[0] != '.':
            raise RuntimeError('The first character must be period.')
        opt_default['defaultextension'] = ext
        opt_default['filetypes'] = [('', '*' + ext),
                                    ('all', '*')]

    _opt = dict(opt_default, **kwargs)

    root = tk.Tk()
    root.withdraw()
    root.wm_attributes("-topmost", True)

    return tkfiledialog.asksaveasfilename(**_opt)


def load_pickle_with_dialog(ext: str = '.pkl',
                            initialdir: Union[str, Path] = '.',
                            **kwargs) -> Any:
    """Load a pickled file selected by a file open dialog.

    Parameters
    ----------
    ext : str
        A default extension of the dialog.
    initialdir : str or pathlib.Path, default='.'
        An initial directory of the dialog
    kwargs : optional
        See `open_dialog`.

    Returns
    -------
    Any
        The loaded data
        If the dialog is canceled, `None` is returned.
    """
    fn = open_dialog(ext, initialdir, **kwargs)
    if fn == '':  # canceled
        return None

    with Path(fn).open('rb') as f:
        data = pickle.load(f)
    return data


def dump_pickle_with_dialog(obj: Any,
                            ext: str = '.pkl',
                            initialdir: Union[str, Path] = '.',
                            dump_func: Callable = pickle.dump,
                            **kwargs) -> Union[None, Path]:
    """Pickle an object as a file selected by a file save dialog.

    Parameters
    ----------
    ext : str
        A default extension of the dialog.
    initialdir : str or pathlib.Path, default='.'
        An initial directory of the dialog
    dump_func : callable, default `pickle.dump`
        If you want to use `cloudpickle`, assign `dump_func` like:
        ```
        import cloudpickle
        path_pkl = dump_pickle_with_dialog(obj, dump_func=cloudpickle.dump)
        ```
    kwargs : optional
        See `saveas_dialog`.

    Returns
    --------
    pathlib.Path or None
        a Path object corresponding to the dumped file, pathlib.Path
        If the dialog is canceled, `None` is returned.
    """
    fn = saveas_dialog(ext, initialdir, **kwargs)
    if fn == '':  # canceled
        return None
    # note: 上書き確認はtkinterがやってくれるのでここではチェックしない

    p = Path(fn)
    with p.open('wb') as f:
        dump_func(obj, f)

    return p
