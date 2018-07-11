#!/usr/bin/env python

# Written by Jimmy Gizmo, July 9, 2018. Copyright (c) 2018. MIT License.

# PROBLEM STATEMENT:
# Suppose we want to pre-process JSON strings to strip out C-style line comments. An example might look like this:
# // this is a comment
# { // another comment
# true, "foo", // 3rd comment
# "http://www.ariba.com" // comment after URL
# }
# Write a function to strip line comments without using regular expressions. Think about the other corner cases.

# ASSUMPTIONS:
# No comments span multiple lines, which is implied since all of the comments in the example json data/file are
# line-end comments.

# COMMENTS:
# Valid JSON cannot contain comments like //... or /* ... */ unless of course actual data elements are added to
# contain the comment information such as:
# { "_comment": "This is a comment in valid JSON, included as a valid data element." }
# The implication is that such _comment data would need to be ignored by anything consuming the JSON.
# So one can see a potential need for such a solution as this question # 5.

json_data = """
// this is a comment
{ // another comment
true, "foo", // 3rd comment
"http://www.ariba.com" // comment after URL
}
"""

for line in json_data:
    


##
#
