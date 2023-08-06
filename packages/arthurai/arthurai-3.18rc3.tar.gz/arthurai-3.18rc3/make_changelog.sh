# Usage: bash make_changelog <filename>

file=$1

tags=`git tag --list --sort=-taggerdate`
rm -f $file
for tag in $tags
do
    if [[ -n $prev ]]
    then
        git log --oneline --first-parent --format='[%S] [%cs] %s' $prev...$tag >> $file
        echo "" >> $file
        git diff --compact-summary $prev $tag >> $file
        echo "" >> $file
    fi
    prev=$tag
done
