# Module version stage suffix map
_specifier_ = {'alpha': 'a', 'beta': 'b', 'candidate': 'rc', 'final': ''}


# Module version
version_info = (0, 0, 0, 'alpha', 9)

version_end = '' if version_info[3] == 'final' else _specifier_[version_info[3]]+str(version_info[4])
__version__ = f'{version_info[0]}.{version_info[1]}.{version_info[2]}{version_end}' 