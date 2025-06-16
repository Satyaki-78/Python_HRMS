def get_path(*args):
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    upper_base_dir = os.path.dirname(base_dir)
    icon_path = os.path.join(upper_base_dir,*args)
    if os.path.exists(icon_path):
        return icon_path
    else:
        return None