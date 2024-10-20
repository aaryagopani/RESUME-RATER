import re
def get_gemini_response_first(model,prompt,default_answer,text):
     response = model.generate_content(prompt.format(default_answer=default_answer,text=text))
     return response.text

def format_review(review):
    """Format the generated review text into structured HTML-ready sections."""
    
    # Define patterns to capture each section separately
    sections = {
        'rating': r"(?:\*\*Overall Rating:?\*\*|\*\*Rating:?\*\*)\s*([\d\.]+/5)",
        'positive': r"(?:\*\*1\.\s*Positive Points\*\*)(.*?)(?=\*\*2\.\s*Negative Points\*\*)",
        'negative': r"(?:\*\*2\.\s*Negative Points\*\*)(.*?)(?=\*\*Recommendations:?\*\*)",
        'recommendations': r"(?:\*\*Recommendations:?\*\*)(.*)"
    }

    # Extract sections
    extracted_sections = {
        key: re.search(pattern, review, re.DOTALL | re.IGNORECASE)
        for key, pattern in sections.items()
    }

    # Helper function to clean and format points
    def format_points(text):
        if not text:
            return []
        points = re.findall(r'[a-z]\.\s*(.*?)(?=(?:[a-z]\.|$))', text, re.DOTALL)
        return [point.strip() for point in points if point.strip()]

    # Helper function to bold text between star pairs
    def bold_star_pairs(text):
        return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)

    # Start building HTML content
    html_content = "<div class='review'>"

    # Add Overall Rating
    if extracted_sections['rating']:
        rating = extracted_sections['rating'].group(1).strip()
        html_content += f"<div class='section rating'><h3>Overall Rating</h3><p><strong>{rating}</strong></p></div>"

    # Add Positive Points
    if extracted_sections['positive']:
        positive_points = format_points(extracted_sections['positive'].group(1))
        if positive_points:
            html_content += "<div class='section positive-points'>"
            html_content += "<h3>Positive Points</h3><ul>"
            for point in positive_points:
                html_content += f"<li>{bold_star_pairs(point)}</li>"
            html_content += "</ul></div>"

    # Add Negative Points
    if extracted_sections['negative']:
        negative_points = format_points(extracted_sections['negative'].group(1))
        if negative_points:
            html_content += "<div class='section negative-points'>"
            html_content += "<h3>Negative Points</h3><ul>"
            for point in negative_points:
                html_content += f"<li>{bold_star_pairs(point)}</li>"
            html_content += "</ul></div>"

    # Add Recommendations
    if extracted_sections['recommendations']:
        recommendations = extracted_sections['recommendations'].group(1).strip().split('*')[1:]  # Split by '*' and remove empty first element
        if recommendations:
            html_content += "<div class='section recommendations'>"
            html_content += "<h3>Recommendations</h3><ul>"
            for rec in recommendations:
                html_content += f"<li>{bold_star_pairs(rec.strip())}</li>"
            html_content += "</ul></div>"

    html_content += "</div>"
    return html_content