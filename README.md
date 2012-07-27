Firefox_4_Plus_Examiner
===================

Parses Firefox databases eg. for digital forensics. Works with Firefox 4 and later. Firefox changed the format of its databases in version 4, so some of the older analyzing tools broke.

Usage:

1) Press Button 'Start'

2) Select path to Firefox Profile

3) Select path where the output files shall be written

FFFE parses (and therefore needs) the following databases:

places.sqlite

cookies.sqlite

downloads.sqlite

formhistory.sqlite

signons.sqlite


Resultion files are TAB separated csv to import in Excel, Open Office etc.