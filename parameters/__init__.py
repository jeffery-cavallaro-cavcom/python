"""
Application Parameter Management

Application execution is modified by input parameter values that can be
supplied on the command line (argparse), by environment variables (os.environ),
from an INI-style configuration file (configparser), and from compiled default
values.  The parameters module facilitates the definition and collection of
these values from these various input sources.  When a parameter value exists
in multiple sources, priority is according to the order specified above.

Each parameter is defined by a Parameter instance.  The parameter instance
specifies the name of the parameter and whether the parameter value can be
supplied from a command line option, a command line argument, an environment
variable, a configuration file, or a default value.  All of the parameters for
an application are added to a ParameterSet instance.  Once the parameter set is
defined, the values can be collected with a single collect method call.  The
selected values are returned via a dictionary that is indexed by parameter
name.

A parameter set overrides the default help action of argparse with an action
that displays not only the defined command line options and arguments, but also
all accepted environment variables and configurataion file parameters.
"""
