# OpenAlex 
by bomi kang, duke

The process has two parts: one in Bash and one in Python.

In the Bash script, we grab paper-level data from OpenAlex using AWS, download it, and unzip the files.

In Python, we take those unzipped files, pull out the info we need, and organize it for analysis.


As the final output, we’ll have key details for each paper: the title, authorship info, publication date, abstract (encoded), keywords, and locations. I’ve filtered the data to include only works published after 2004 to focus on more recent research.

