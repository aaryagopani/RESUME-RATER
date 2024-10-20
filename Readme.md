#Resume Rater

##Use of LLM API for creating a AI powered Resume Rating System

###gemini-1.5-flash-latest is used for rating the resume 

https://deepmind.google/technologies/gemini/flash/   **Link to read more about gemini**


The user uploads their resume in .pdf format
The text is extracted from the resume using pypdf2(python library)
The extracted text is then passed to the LLM API for rating
The rating is then displayed to the user


Python frameworks used is listed in requirements.txt(/requirements.txt)
