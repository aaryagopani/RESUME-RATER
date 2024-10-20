import os
import PyPDF2
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain.output_parsers import RegexParser
from functions import get_gemini_response_first, format_review
from flask import Flask, render_template, request, redirect, url_for

# This code is to load the environment variables from a .env file into your program's environment
load_dotenv()


# This code is use to load the API key securely and establish autenthication
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# This line of code connects to a specific model within the genai library
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")


# This code is to generate the response from the model we choose


# input_prompt = """
# You are an expert for reviewing resume of people and you have to rate the resume
# The resume is a pdf that has been extracted as text and is given below
# {text}
# Give the three positive points and three negative points(you roast the resume as a part of negative points) in the given format
# 1.Positive Points
#   a. First Positive Point
#   b. Second Positive Point
#   c. Third Positive Point
# 2.Negative Points
#   a. First Negative Point
#   b. Second Negative Point
#   c. Third Negative Point
  
# Also rate my resume out of 5, the answer can be even in decimal format like 4.8
# If the text is not about a resume than give the below answer directly
# Output in HTML Format
# {default_answer}
# """

input_prompt = """You're an expert resume reviewer with years of experience. Analyze the uploaded document and respond as follows:

1. If it's not a resume:
   <div id="false-doc">
   <p>{default_answer}</p>
   </div>
   End your response here.

2. If it is a resume, provide this review:


<div class="content">
<h3>Quick Take</h3>
<div class="quick-take">
<p>Give a 2-sentence overview of the resume's quality.</p>
</div>
</div>

<div class="content"  id="positive-points">

<h3>Top 3 Strengths</h3>
<ul>
  <li><strong class="strength">Best Feature:</strong> Highlight the most impressive aspect.</li>
  <li><strong class="strength">Notable Achievement:</strong> Mention a standout accomplishment.</li>
  <li><strong class="strength">Effective Element:</strong> Point out another positive feature.</li>
</ul>
</div>

<div class="content"  id="negative-points">

<h3>Top 3 Improvements Needed</h3>
<ul>
  <li><strong class="improvement">Major Weakness:</strong> Identify the biggest issue (add a touch of humor if appropriate).</li>
  <li><strong class="improvement">Missing Component:</strong> Note an important missing or underdeveloped section.</li>
  <li><strong class="improvement">Enhancement Opportunity:</strong> Suggest another area for improvement.</li>
</ul>
</div>

</div>

<div class="content" id="rating">
<h3>Industry Fit & Rating</h3>
<p class="rating">Rate the resume X.X/5</p>
<p class="quick-take">Briefly assess industry alignment,justify in one sentence</p> 
</div>

<div class="content"  id="final-thoughts">
<h3>Quick Fix Tips</h3>
<ol>
  <li>Suggest the most impactful change.</li>
  <li>Recommend a way to enhance content.</li>
  <li>Advise on improving visual appeal or structure.</li>
</ol>
</div>

<div class="content" id="conclusion">
<h3>Conclusion</h3>
<p class="conclusion">Conclude with a brief encouraging statement.</p>
</div>
Be specific, balanced, and tailor advice to the apparent career level and industry. Keep it engaging but professional.
{text}

"""

default_answer = """Sorry,I am a AI based resume rater and the uploaded pdf doesn't look as a resume"""



# Intializing the flask app
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "resume" not in request.files:
        return "No file part", 400

    file = request.files["resume"]

    if file.filename == "" or not file.filename.endswith(".pdf"):
        return "Invalid file format. Please upload a PDF.", 400

    pdf_reader = PyPDF2.PdfReader(file)
    pdf_text = "".join(page.extract_text() for page in pdf_reader.pages)

    prompt = PromptTemplate(
        input_variables=["text", "default_answer"], template=input_prompt
    )
    review = get_gemini_response_first(model, prompt, default_answer, pdf_text)
    # print("Generated Review Text:\n", review)
    # parsed_output = parser.parse(review)
    # print(parsed_output)
    return render_template("index.html", parsed_output=review)


if __name__ == "__main__":
    app.run(debug=True)
