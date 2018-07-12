#! /bin/bash

BASE="/Users/bilbo"
ROOT="$BASE/tree"

# Depth 0
mkdir "$ROOT"

# Depth 1 - 3 dirs and 1 file
mkdir "$ROOT/a"
mkdir "$ROOT/b"
mkdir "$ROOT/c"
echo "dddd" > "$ROOT/F.txt"

# Depth 2 - 1 dir, 2 files in a. 2 dirs in b. 2 dirs, 1 file in c.
mkdir "$ROOT/a/aa"
echo "xxxx" > "$ROOT/a/Fa1.txt"
echo "xxii" > "$ROOT/a/Fa2.txt"
echo "yyyy" > "$ROOT/a/Fa3.txt"

mkdir "$ROOT/b/ba"
mkdir "$ROOT/b/bb"

mkdir "$ROOT/c/ca"
mkdir "$ROOT/c/cb"
echo "xxzz" > "$ROOT/c/Fc1.txt"

# Depth 3



echo "Tree structure and contained data file nodes generated at: $ROOT"

##
#

