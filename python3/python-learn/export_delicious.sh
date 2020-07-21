#!/bin/sh
#
# NAME
#        Delicious.sh - Download your bookmarks
#
# SYNOPSIS
#        Delicious.sh <username> <password> <save path>
#
# DESCRIPTION
#        Downloads the bookmarks at Delicious as an XML file.
#
#        How to export at midnight every day:
#
#        First, make sure nobody else can read your crontab. If not, they can
#        get access to your password, and I'm not good at sympathy.
#
#        $ git clone git://github.com/l0b0/export.git
#
#        $ crontab -e
#
#        Insert a new line with the following contents (replacing the example
#        paths and login with your own):
#
#        @midnight /.../export/Delicious.sh user password /.../bookmarks.xml
#
# BUGS
#        https://github.com/l0b0/export/issues
#
# COPYRIGHT AND LICENSE
#        Copyright (C) 2010, 2011 Victor Engmark
#
#        This program is free software: you can redistribute it and/or modify
#        it under the terms of the GNU General Public License as published by
#        the Free Software Foundation, either version 3 of the License, or
#        (at your option) any later version.
#
#        This program is distributed in the hope that it will be useful,
#        but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#        GNU General Public License for more details.
#
#        You should have received a copy of the GNU General Public License
#        along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
set -o errexit -o nounset

if [ $# -ne 3 ]
then
    echo 'Wrong parameters - See the documentation on top of the script'
    exit 1
fi

USERNAME="$1"
PASSWORD="$2"
EXPORT_PATH="$3"

# Export
EXPORT_URL=https://api.del.icio.us/v1/posts/all
EXPORT_DATE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
chunk_size=1000 # Delicious now only supports exporting 1000 bookmarks at a time
header_lines=3
chunk_lines=$(($chunk_size + $header_lines))
EXPORT_COMPATIBILITY='
s#^<posts \(tag="[^"]*"\) \(total="[^"]*"\) \(user="[^"]*"\)>#<posts \3 update="'$EXPORT_DATE'" \1 \2>#;
s#^<post \(description="[^"]*"\) \(extended="[^"]*"\) \(hash="[^"]*"\) \(href="[^"]*"\) private="[^"]*" shared="[^"]*" \(tag="[^"]*"\) \(time="[^"]*"\)/>#  <post \4 \3 \1 \5 \6 \2 meta="" />#'
EXPORT_REMOVE_LINES='3,${/^</d}'
bookmark_prefix='<post '

> "$EXPORT_PATH" # Empty bookmarks file

bookmarks_count() {
    # How many bookmarks have we fetched?
    grep -o "${bookmark_prefix}" "$EXPORT_PATH" | wc -l || true
}

while [ $(($(bookmarks_count) % $chunk_size)) -eq 0 ]
do
    wget \
        --user="$USERNAME" --password="$PASSWORD" \
        -O- \
        --no-check-certificate \
        "$EXPORT_URL?start=$(bookmarks_count)" >> "$EXPORT_PATH"
done
sed -i -e 's#><#>\n<#g' "$EXPORT_PATH" # Introduce newlines
sed -i -e "$EXPORT_COMPATIBILITY" "$EXPORT_PATH"
sed -i -e "$EXPORT_REMOVE_LINES" "$EXPORT_PATH"
echo '</posts>' >> "$EXPORT_PATH"

