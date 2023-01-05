# *Split and grade*

A simple tool for filling in Moodle gradesheets and generating feedback attachments.

This application receives:

* An input PDF file containing all the submissions for a given assignment.

* A group gradesheet (in CSV format) that contains the grade and the number of pages of each submission.

* A Moodle gradesheet (in CSV format) without grades.

and generates:

* The same Moodle gradesheet as above, but with the grades taken from the group gradesheet.

* A directory that contains, for each student, the segment of the input PDF file corresponding to their submission. We can create a ZIP file directly from that directory and upload it to Moodle as assignment feedback.

