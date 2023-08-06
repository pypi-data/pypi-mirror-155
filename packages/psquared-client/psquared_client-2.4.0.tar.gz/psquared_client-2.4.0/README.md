# `psquared_client` project #

The `psquared_client` project contains both the `psquared_client` package that
provides a python interface to a PSqaured server, and the `pp-cli` command line
interface that uses that package to all copmmand line access to the server.


## `pp-cli` executable ##

More details about the `pp-cli` executable can be found using its help option

    pp-cli -h

but here are some examples of retrieving information.
(_Note:_ unless  you are using the default local PSquared server you will need to the the environmental
variable `PP_APPLICATION` to point the server you want to use.)

*   To list the currently active configurations

        pp-cli

*   To list the known versions of a given configuration

        pp-cli -i <configuration>


*   To display the current state of one or more items for a configuration/version.

        pp-cli -i -V <version> <configuration> item ...

*   To display the history of one or more items for a configuration/version.

        pp-cli -H -V <version> <configuration> item ...

*   As an alternate, the list of items to be acted upon can be supplied in a file with one item per line.
    Thus the following displays the current state of a set of items listed in a file for a configuration/version.

        pp-cli -i -f <file> -V <version> <configuration>


Here are some examples of commands that affect the state of PSquared.
(_Note:_ you may need an authorized certificate to execute these types of commands.)

*   To submit one or more items for processing with a configuration/version.

        pp-cli -i -s -V <version> <configuration> item ...

*   To resolve the failure of one or more items for a configuration/version.

        pp-cli -i --resolve -V <version> <configuration> item ...

    The other transitions, `submit`, `cancel`, `reset`, 'abandon` and `recover` have similar options.


## `psquared_client` package ##

The `psquared_client` package provides the `PSquared` class that can be used to
access a PSqaured server and a `Display` module that can display the responses
of a PSquared server in a readable format.


### `PSquared` class ###

The `PSquared` class provides various documents in reponse to a request to the
PSquared server. The documents are in the form of a standard python
`ElementTree`. Currently the following methods are supported.

*   `get_application` - returns the application document at the URL
*   `get_configuration` - returns the configuration document the named configuration
*   `get_report` - returns the requested report document
*   `execute_submissions` - submits a list of items for processing
*   `execute_transitions` - execute a transition for a list of items


### `Display` module ###

The `Display` modules provides various methods for displaying the reponses that
result from a request to the PSquared server. Currently the following methods
are supported.

*   `configurations` - displays all the configurations contained in an application document
*   `versions` - displays all the versions of a named configuration
*   `entry` - displays the state of a given item
*   `info` - displays the states of a set of items contained in a report
*   `histories` - displays the history of one or more items contained in history document
