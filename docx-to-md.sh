#!/bin/bash

#depends: w2m from ruby: 
# gem install word-to-markdown

the_dir=$(pwd)

for f in *\ *; do mv "$f" "${f// /_}"; done

rm $the_dir/Condition_Era/~*
rm $the_dir/Condition_Occurrence_Combinations/~*

for f in *; do
    if [ -d ${f} ]; then
        # Will not run if no directories are available
	touch $the_dir/$f.md
	for fl in $(ls -d -1 $the_dir/$f/*.*); do
		w2m ${fl} >> $the_dir/$f.md
		echo *-*-*-*-* >> $the_dir/$f.md
	done
    fi
done

mkdir md
mv $the_dir/*.md $the_dir/md/

for f in *_*; do mv "$f" "${f//_/ }"; done

