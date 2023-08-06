def download_to_compute_capacityfactor(func):
    """Decorator to handle capacity factor from capacity and generation.
    in :py:meth:`..data_source.ParsingDataSourceBase.download`
    and :py:meth:`..data_source.ParsingDataSourceBase.load`.

    :param func: Function to be decorated.
    :type func: function
    """

    # Define decorating function
    def inner(self, variable_component_names=None, **kwargs):
        # Add capacity factor to variable to load names
        variable_component_to_load_names = add_capacityfactor(
            variable_component_names, **kwargs)

        # Call function and return
        return func(self, variable_component_to_load_names, **kwargs)

    return inner


def compute_capacityfactor(func):
    """Decorator to handle capacity factor from capacity and generation.
    in :py:meth:`..data_source.ParsingDataSourceBase.download`
    and :py:meth:`..data_source.ParsingDataSourceBase.load`.

    :param func: Function to be decorated.
    :type func: function
    """

    # Define decorating function
    def inner(self, variable_component_names=None, **kwargs):
        # Add capacity factor to variable to load names
        variable_component_to_load_names = add_capacityfactor(
            variable_component_names, **kwargs)

        # Call function
        ds = func(self, variable_component_to_load_names, **kwargs)

        # Get capacity factor
        variable_name = 'capacityfactor'
        if variable_name in variable_component_names:
            # Get capacity factor
            ds[variable_name] = self._get_capacityfactor(ds, **kwargs)

        # Select variables
        ds_sel = {}
        for variable_name in variable_component_names:
            ds_sel[variable_name] = ds[variable_name]

        return ds_sel

    return inner


def add_capacityfactor(variable_component_names, **kwargs):
    """Add capacity factor to :py:obj:`variable_component_to_load_names`.

    :param variable_component_names: Names of components to load per
      variable.
    :type variable_component_names: mapping from :py:class:`str`
      to collection

    :returns: Names of components to load per variable with
      capacity factor added.
    :rtype: mapping from :py:class:`str` to collection
    """
    # Add capacity and generation to variables to load
    variable_name = 'capacityfactor'
    variable_component_to_load_names = variable_component_names.copy()
    if variable_name in variable_component_names:
        # Make sure that generation and capacity are loaded
        variable_component_to_load_names.update(
            {'generation': variable_component_names[variable_name],
             'capacity': variable_component_names[variable_name]})

        # Remove capacity factor from variables to load
        del variable_component_to_load_names['capacityfactor']

    return variable_component_to_load_names
