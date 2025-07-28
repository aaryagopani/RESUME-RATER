<img width="1039" height="713" alt="Screenshot 2025-07-28 at 10 18 38 AM" src="https://github.com/user-attachments/assets/1b64ae25-39c7-4637-b975-8374d266d97a" /><img width="1039" height="713" alt="Screenshot 2025-07-28 at 10 18 38 AM" src="https://github.com/user-attachments/assets/942be3b7-5e0e-4374-81bb-ad69d261c935" />#Resume Rater

##Use of LLM API for creating an AI powered Resume Rating System

###gemini-1.5-flash-latest is used for rating the resume 

https://deepmind.google/technologies/gemini/flash/   **Link to read more about gemini**

You need to create .env file in your folder and paste the GEMINI_API_KEY in that

The user uploads their resume in .pdf format
The text is extracted from the resume using pypdf2(python library)
The extracted text is then passed to the LLM API for rating
The rating is then displayed to the user


Python frameworks used is listed in requirements.txt


Here are some of the images for the project


![alt text](<Screenshot 2025-07-28 at 10.18.38 AM.png>)

![alt text](<Screenshot 2025-07-28 at 10.20.22 AM.png>)