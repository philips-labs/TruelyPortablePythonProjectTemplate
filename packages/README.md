# The packages Folder

**Description**
 
The purpose of this  contains handy modules needed to support 
portabilitiy and contains learnings and a template for sphinxdocumentation.
 
Because, in this framework, 
the directories "packages" and users sources are both in the PYTHONPATH,
any package in the users' sources can be moved to packages without change of 
behavior; in fact, any change in behavior marks an unwanted directory dependency that must
be corrected. 