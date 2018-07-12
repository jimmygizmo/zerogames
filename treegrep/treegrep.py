#!/usr/bin/env python

########################################################################################################################

#
# treegrep.py  v1.0
# ---------------------
#
#    Treegrep is the solution to a job interview programming assignment for a Fortune 500 company
#    for a position involving hardware and software testing automation.
#    Traverses a directory tree recursively. Performs regular expression matches.
#    Generates a data structure and graph of results.
#
# Author: Jimmy Gizmo
# http://ninthdevice.com
# Version: 1.0
# Version date: 2018-07-11
# Created: 2018-07-11
#
# Developed under Python 2.7.10. Should work with recent 2.7.* versions. Only standard/core modules are used.
#

########################################################################################################################

#
# License: MIT.
# The MIT license is one of the most open, permissive and simple Open Source licenses. See LICENSE.txt at this URL:
# GitHub repository: https://github.com/jimmygizmo/zerogames
#
#
# The MIT License (MIT)
#
# Copyright (c) 2018 Jimmy Gizmo, Ninth Device
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

########################################################################################################################

#
# #### FEATURES IN VERSION 1.0 ####
#
# Only standard/core modules present in Python 2.7.10 are used, so no module installation is necessary.
#
# Full-featured POSIX command-line argument processing with a few basic initial commands implemented to control the
# logging verbosity level and other such facilities.
#
# Object-oriented python with a clean class structure intended as a solid-foundation to build a best-practice OO python
# application from. A Base class which is never instantiated provides global logging and configuration. An App class
# then adds the command-line processing and run() method as the starting point to take user input and then dispatch
# the specific operations the user is requesting.
#
# Powerful, industry-standard logging, implemented on a very simple and usable level. If this application grows into
# something big and complex, then one can move into the more advanced capabilities of the logging module. However,
# even the simplest of applications should have robust logging. The benefits are huge. Treegrep has a very good
# basic logging system in place out of the box. One can go a long way with the single --verbose switch to control
# just INFO and DEBUG logging levels. One should include DEBUG logging calls everywhere and take full advantage
# of the debugging, transparency, optimization, monitoring, audit and other benefits of rich DEBUG logging. Choose
# to make INFO vs. DEBUG logging calls based on the activity-level of the app, disk-space or personal taste.
#
# Easy-to-find and easy-to-edit in-code configuration through the use of a namespace-only "config" class in main.
# This strategy works well as a way to have infrequently-changing global config information directly in the code.
# Since configuration-in-code will not suit all needs, future versions could offer a clean
# and simple file-based configuration strategy which will be handled all in the Base class. This will further minimize
# the amount of stuff we are doing in __main__ and of course offer separation of code from configuration.
#
# Care has been taken to follow best practices in as many areas as possible. Best-practices known in the Python
# community as well as best practices learned by this author from nearly 20 years writing code and building
# infrastructure for the industry's top companies.
#
# Generous comments, doc strings, informative example text, clear yet concise object names;
# all contribute to assist the developer/maintainer in understanding key concepts and solving basic problems in a
# practical way.
#

########################################################################################################################

#
# PEP8 Coding-Style Recommendations
#
# The code in this application closely follows the PEP8 recommendations and is regularly validated with the
# PEP8 tool during development. Some examples are: Line width of 120 characters. Alignment of multi-element lists and
# other entities which span multiple lines for improved readability. 4 spaces for each indentation level. Thorough use
# of doc strings and much more. Other coding and commenting styles are used to include as much helpful information and
# structure as possible.
#

###############################################  PYTHON CORE LIBRARIES  ################################################


import logging
import argparse
import time
import os
import sys
import re
import json

# Other essential core modules you may want to use early in your new application:
# import io


############################################  3RD-PARTY (SITE) LIBRARIES  ##############################################


# For the evolution and extension of Treegrep, the following non-core modules, while they do require separate
# installation into Python's site-libraries, might be good considerations:

# While we are using the standard/core json module to generate our output data structure, another common choice
# of data format might be XML, and for that we could install the dicttoxml module.
# import dicttoxml


############################################  GLOBAL CONFIGURATION SETTINGS  ###########################################


class config:
    """This config class is used as a global namespace only. No instances are created. There are no methods. Used as a
    convenient way to access global, infrequently-changing configuration information. The lowercase name of config
    is intentional here. This is not a regular class, so its name is not capitalized like a regular class. The config
    values specified just below here are being set from __main__ and should be kept here near the top of the code.
    This class definition actually ends immediately here with 'pass' since all we want to do is create the namespace."""
    pass

config.app_nick = "treegrep"  # Application Nickname. This will be used to name logfiles and more so it should
# consist only of lower-case letters, numbers or underscore.

config.log_filename = config.app_nick + ".log"

# Directory where log files should be created.
config.log_path = "."  # . is current directory

# Fields and format for the log lines. Refer to the documentation for the 'logging' module.
config.log_format = '%(asctime)s:%(levelname)s:%(funcName)s:%(lineno)s %(message)s'

config.log_file = config.log_path + "/" + config.log_filename

# The default logging level to be used initially, prior to any adjustments made via command-line options:
config.default_log_level = logging.INFO
# Although there are many logging levels available in the logging module, we are keeping this application
# simple and will only use two: INFO and DEBUG, controlled with a single --verbose option. Feel free to call any
# of the log actions. You will see WARN, ERROR and CRITICAL messages in either INFO or DEBUG log_levels. We have not
# limited the message types/levels. We have only limited the selection of log level to a single --verbose switch.


#################################################  CLASS DEFINITIONS  ##################################################


class Base(object):
    """The 'Base' class is literally the base class of this application, the main purpose of which is to provide
    convenient access to logging and configuration. As this application evolves, other facilities and data at this
    base-level may be added to this class. Briefly, let's recall that there is the __main__ or global scope which
    is sort of a base to all classes in python. So in one sense, __main__ is a base of Base but in OO terms, Base is
    our base CLASS. Treegrep intends to follow best practices in OOP as well as in many other areas, so we
    want to have a minimum of objects (variables and functions etc.) in the global/main space. We should maintain a
    tendency to try to move anything in main to Base if possible, but not to an unreasonable degree.
    A bit more about main; Some things are very convenient to have in the main/global space, such as the config
    namespace we use as a clear, self-documenting place to edit infrequently-changing configuration information in
    Treegrep. In future versions of Treegrep, config might be handled in some other way, perhaps
    through loading a config file, entirely in the Base class and not involving the main namespace, but having config
    as a simple namespace in main near the top of the code is clean and convenient for now.
    Base should be inherited by all classes in Treegrep unless the class is so simple that it does not need
    access to logging or configuration data but since it is a good idea to have a LOT of ability to log information
    especially at the verbose/DEBUG level, then I can say that really ALL classes should inherit from Base or from
    another class which is a subclass of Base."""

    def __init__(self, config, logger):
        """Base is never instantiated. It is always inherited. However, this constructor is definitely used. Classes
        which inherit from Base will in most cases use python's super() call to invoke Base.__init__() in order to
        initialize config, logger and other objects into their own namespace(s). This will be done from within the
        __init__ of the sub-class. See App.__init__() for an example."""
        self.cfg = config
        self.log = logger

        # This log line is here for illustrative purposes and is only active if you change config.default_log_level
        # to DEBUG in the code. Command-line options have not been processed yet so --verbose cannot take effect yet.
        self.log.debug("Base class __init__ executed.")


class App(Base):
    """The App class is the central point of activity for this application. There should be only one instance of the App
    class and it is during the __init__ of this class when all processing of command-line arguments is done by calling
    the process_cmd_line() method. This is the application-specific processing during which you will validate the
    sanity of all supplied options and values and where you will provide thorough feedback to the user in case they
    have supplied any invalid options. The App class contains the application's run() method which is the point from
    which one should dispatch the highest level program operations. For example, as a command-line
    utility and handles multiple commands, then within App.run() one should detect the specific command and then
    dispatch/execute operations for that command. App inherits from Base, which provides convenient access to logging,
    configuration and possibly other facilities needed by App or other classes."""

    def __init__(self, config, logger, cmd_line_parser):
        """Constructor for App objects, of which there is currently only intended to be one instance. Command-line
        options are processed here by calling the method for that purpose, during which time related feedback or errors
        are thoroughly communicated to the user. Most initialization, sanity-checking and pre-dispatch user feedback
        should occur in process_cmd_line() or some other method which is always called by this __init__."""

        # App inherits from Base. No instance of Base is ever created, so we call the __init__ of Base like this
        # and thereby get the attributes from the __init__ of Base initialized here into App.
        super(App, self).__init__(config, logger)
        # self.cfg, inherited from Base, has now been initialized.
        # self.log, inherited from Base, has now been initialized.
        self.tree = None
        self.depth = -1  # Prior to starting traversal, such that root node is depth 0.
        # TODO: Implement depth. Currently lacking the method to calculate depth.
        self.node_count = 0  # TODO: Possibly move this to a static/class attribute of the Node class.

        self.output_data = {}  # Initialize the dictionary which will contain any output data generated during the
        # tree traversal and file scanning.

        self.arg = cmd_line_parser.parse_args()  # A namespace object is returned to self.arg here. See argparse docs.

        # This log line is here for illustrative purposes and is only active if you change config.default_log_level
        # to DEBUG in the code. Command-line options have not been processed yet so --verbose cannot take effect yet.
        self.log.debug("App class instantiated. Command-line options will now be processed.")

        self.rex = None

        self.process_cmd_line()

    def process_cmd_line(self):  # The term "command-line options" is interchangeable with "command-line arguments"
        if self.arg.verbose:  # See how we use the exact name of the option to access it. These can be different types.
            self.log.setLevel(logging.DEBUG)
            self.log.debug("Verbose mode is now active. Log level set to DEBUG.")
        else:
            self.log.info("Using default log level of " + logging.getLevelName(self.cfg.default_log_level))

        self.rex = re.compile(self.arg.keyword)


    def run(self):
        self.log.info("Application " + self.cfg.app_nick + " is now running.")

        abs_path = os.path.abspath(self.arg.root_dir)  # Arg name changed from original 'path' to 'root_dir' in order
        # to meet exact program specifications. TODO: Maybe change argument name back to 'path' later if appropriate.
        self.log.debug("os.path.abspath of path is: " + str(abs_path))

        if not os.path.isdir(abs_path):
            self.log.error("The --path value does not represent a valid directory in the filesystem.")
            sys.exit(1)

        #self.tree = Node(path=abspath, name="Root", type="dir")

        self.log.debug("Beginning traversal of the filesystem tree at the root path provided.")

        # Initialize the tree with the root node.
        # The filesystem will be traversed recursively, with the full hierarchy of child nodes being added to the root.
        # The tree is the root node and all of its child nodes, so a Node object (which IS the tree) will be returned.
        root_node = Node(path=abs_path, name="Root Node", node_type="dir", attributes=None)

        # Complete the tree by recursively processing the root node to add all child nodes, returning the full tree.
        self.tree = self.process_dir(root_node)

        print
        print "RESULTS:"
        print
        print self.output_data
        print

        # Generate bar chart. Output csv data for D3 bar chart graphing module.
        with open("./bar-data.csv", "w+") as file_obj:  # w+ overwrite file if it exists
            line = "date,value\n"  # D3 fields header. NOTE: date is an artifact of adapting the graph I had. Ignore.
            file_obj.write(line)
            for key in self.output_data.keys():
                val = self.output_data[key]
                line = '"' + key + '",' + str(val) + "\n"
                file_obj.write(line)


    def process_dir(self, current_node):
        Node.current_traversal_depth += 1  # Class attribute. # TODO: Should we access it like this here?
        # TODO: OR .. we could make a class method to: increase_current_traversal_depth()
        # TODO: Similarly: decrease_depth() get_max_depth()
        self.node_count += 1  # A variable in the App class, parallel to Node.count
        # Note that the class attribute Node.count should also increment automatically.
        # Node.count should also be accessible through any instance as node_instance.count/self.count etc.
        # TODO: Probably will just go with Node.count. Then deprecate App's self.node_count.
        type = None

        self.log.debug("- - Processing directory at path of current node: " + str(current_node.path))

        # Recursive processing
        for dir_item in os.listdir(current_node.path):
            dir_item.rstrip()  # On Windows and possibly all OSes, trailing newline must be stripped.
            # TODO: Test on Linux and OSX as well to determine if os.listdir returns trailing newlines on them as well.
            path_dir_item = os.path.join(current_node.path, dir_item)
            #abs_path_dir_item = os.path.abspath(dir_item)  # Not necessary. We just composed the absolute path.
            abs_path_dir_item = path_dir_item
            self.log.debug("- - - - ## Creating new Node.")
            self.log.debug("- - - - Path of current dir_item is: " + str(abs_path_dir_item))
            self.log.debug("- - - - New Node name: " + str(dir_item))

            if os.path.isdir(abs_path_dir_item):
                node_type = 'dir'
                self.log.debug("- - - - New Node is of type 'dir'")
                new_child_node = Node(path=abs_path_dir_item, name=dir_item, node_type="dir", attributes=None)
                current_node.add_child(new_child_node)
                self.log.debug("- - - - Node count: " + str(Node.count))
                # RECURSE FURTHER
                self.process_dir(new_child_node)
            else:
                node_type = 'file'
                self.log.debug("- - - - New Node is of type 'file'")
                new_file_node = Node(path=abs_path_dir_item, name=dir_item, node_type="file", attributes="coming soon")
                current_node.add_file(new_file_node)
                self.log.debug("- - - - Node count: " + str(Node.count))
                # Files are just added to their current node with no recursion involved.

                # Update output data structure
                if self.process_file(abs_path_dir_item):
                    (containing_dir, file_part) = os.path.split(abs_path_dir_item)  # The portable way
                    if containing_dir in self.output_data.keys():
                        self.output_data[containing_dir] += 1
                    else:
                        self.output_data[containing_dir] = 1

        self.log.debug("- - Completed processing directory: " + current_node.path)

        return current_node

    def process_file(self, file):
        with open(file) as file_obj:
            fdata = file_obj.read()
        if self.rex.match(fdata):
            self.log.info("- - - - Keyword/regex * MATCHED *: " + str(file))
            return True
        else:
            return False


class Node(object):
    """Node objects make up the data of the tree structure. Instances of Node are linked to each other via the 'children'
    attribute which is of type list, the elements of which are themselves Node objects. A Node can be of type 'file'
    or type 'dir'. Only Nodes of type 'dir' can have any children. Nodes of type file have more attributes than nodes
    of type 'dir'."""
    # Class attributes:
    count = 0
    current_traversal_depth = -1  # -1 means traversal has not yet begun. root node is depth 0.
    max_traversal_depth = -1  # max will parallel current upwards in value during traversal and then stay at max

    def __init__(self, path, name, node_type, attributes):
        self.__class__.count += 1
        self.path = path
        self.name = name
        self.node_type = node_type  # "dir", "file"
        # TODO: Consider adding a "root" type which would be a special kind of dir type for the root node.
        self.attributes = attributes # file attributes for Nodes of type 'file'
        self.children = []  # list of child Node objects for Nodes of type 'dir'
        self.files = []  # list of contained Node objects for Nodes of type 'file'
        self.file_regex_match_count = 0  # Count of files which match the keyword/regex supplied in program arguments

    def add_child(self, child):
        if not self.node_type == "dir":
            print "Adding child Node failed. Current node is not of type 'dir'. Only dir Nodes can contain child " \
            "dir Nodes."
            return  # Not currently a fatal error. TODO: Figure out a good way to handle exceptions within the Node
            # class because we don't want logging in this class.
        else:
            self.children.append(child)

    def add_file(self, file):
        if not self.node_type == "dir":
            print "Adding file Node failed. Current node is not of type 'dir'. Only dir Nodes can contain file."
            return  # Not currently a fatal error. TODO: Figure out a good way to handle exceptions within the Node
            # class because we don't want logging in this class.
        else:
            self.children.append(file)

    def child_count(self):
        return len(self.children)

    def file_count(self):
        return len(self.files)


########################################################  MAIN  ########################################################


def main():
    """The starting point for program execution. main() is not called if this file is imported as a python module.
    main() exits with an integer process exit status of 0 for success and a non-zero integer for any error condition.
    Specific non-zero values will depend on your application, your environment and how you choose to implement such
    conventions, perform error trapping, etc. 0 for success is mandatory. Non-zero values are up to you. main()
    initializes the global logger and starts this application with App.run(). When the program is almost done operating,
    the last part of main() can then perform any finalization and cleanup prior to exit. This application does not
    currently support importing as a module, although it could with some minimal changes."""

    root_logger_name = config.app_nick + "-main"

    logging.basicConfig(filename=config.log_file,
                        format=config.log_format,
                        level=config.default_log_level)

    logger = logging.getLogger(root_logger_name)

    start_time_machine = time.time()
    start_time_human = time.asctime(time.localtime(start_time_machine))
    logger.info("")  # We append to an existing log file, so a blank line and dashes make the startup more visible.
    logger.info("- - - - - - - - - - Initializing " + config.app_nick + " " + start_time_human)
    logger.info("Instantiated root logger: " + root_logger_name)

    app = App(config, logger, cmd_line_parser)
    app.run()

    return 0


################################################  MAIN EXECUTION BEGINS  ###############################################


#### ARGPARSE COMMAND-LINE OPTIONS AND HELP CONFIGURATION ####

#
# The argparse module is configured below.
#
# An 80-character ruler is provided below and the instructional text discusses in detail that you can choose to use
# either full-width-wrapping text or fixed-formatting and therefore fixed-width text for doing things like indenting
# or inserting blank-lines or avoiding the need to escape apostrophes, quotes, newlines or other characters.
# The important point to make here, is that IF you use fixed-formatting .. DON'T exceed 80 characters in width,
# because many console windows might be open at this typical default width. Also, most unix and linux commands have
# their help-text limited to 80 characters. What you should not do is use fixed-formatting over 80 characters, because
# although this is not going to break anything, it means you will end up with a bunch of lines with only one or a few
# words on them in-between the longer lines. Ugly as heck. If you want longer lines, just use the wrapping style.
# I show you how to intermix both styles easily below. Argparse documentation does not go into this level of detail.
#
# One more important point; this formatting technique is dependent upon using the argparse option:
# formatter_class=argparse.RawDescriptionHelpFormatter
#
# See below and see the documentation for the argparse module for more information.
#

################################################################################
# These bars are 80 characters wide, useful for fixed-formatting in argparse.
# Use triple-quotes """ around the description to achieve fixed-formatting.
################################################################################

cmd_line_parser = argparse.ArgumentParser(
    description="""    This program takes an argument root_dir and traverses the
    entire directory tree under it, scanning any files encountered for a match
    to the regular expression supplied in the --keyword argument. A log file is 
    generated which can be put into debug logging mode using the --verbose
    argument. Upon completion, a CSV file is output for rendering of a bar chart
    of the results. A data structure in python-dictionary/JSON format is also
    printed upon completion.""",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    add_help=True)

cmd_line_parser.add_argument(
    '--verbose',
    action='store_true',
    help='Include a high level of detail in the log and in any output to the user. This option changes the log level'
         ' from INFO to DEBUG. The specific types of information which will be added and whether it is added just to'
         ' the log or also to user output will depend on the application.')

cmd_line_parser.add_argument(
    '--root_dir',
    action='store',
    help='Path at which to begin the traversal of the filesystem. This must be a directory.'
         ' String representing a valid path to a directory on the current filesystem.')
    # --root_dir is currently required to be a directory to meet provided specifications, but technically it could be
    # any kind of node.

cmd_line_parser.add_argument(
    '--keyword',
    action='store',
    help='A regular expression to be used to search any file encountered in the tree. If the regular expression matches'
         ' anywhere in a file, then the file will be identified and included in output.')

# Command-line parsing has now been configured and we can start initializing and then running the application.

status = main()  # Start program execution.
exit(status)  # Program execution ends, returning the integer returned by main to the shell as the process exit status.


##
#
