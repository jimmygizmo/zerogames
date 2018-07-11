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
#
# NOTE: A corner case occurs when there are multiple URLs in a line.
#

json_data = """// this is a comment
{ // another comment
true, "foo", // 3rd comment
"http://www.ariba.com" // comment after URL
}
"""

json_data_lines = json_data.splitlines()
output = []

print

def process_line(line, comment_index):
    #print "SUBSTRING: " + line[index-1:comment_index] + "\n"
    if line[comment_index-1:comment_index] == ':':
        print "URL SEEN: " + line + "\n"
        print "URL CLUE BEFORE //: " + line[comment_index-1:comment_index] + "\n"
        print "CONTINUING THROUGH REMAINDER OF THIS LINE"
        line_remainder = line[comment_index+2:len(line)]
        print "LINE REMAINDER: " + line_remainder + "\n"
        find_comment_in_line_or_remainder(line_remainder, remainder_index)
    else:
        print "COMMENT PRESENT: " + line + "\n"

def find_comment_in_line_or_remainder(line_or_remainder, remainder_index):
    comment_index = line.find('//')
    return comment_index


for line in json_data_lines:
    remainder_index = 0  # Always the case when we begin processing a line
    comment_index = find_comment_in_line_or_remainder(line, remainder_index)
    if comment_index == -1:
        print "NO COMMENT: " + line + "\n"
        output.append(line)
        continue
    else:
        process_line(line, comment_index)

##
#
