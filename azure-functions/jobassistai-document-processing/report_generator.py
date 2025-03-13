# report_generator.py
import logging
from clients import openai_client

def generate_report(raw_text, report_type):
    """Generate an HTML report from raw text using OpenAI."""
    if report_type == "government":
        prompt = f"""
        From the text below, generate an HTML report using this template. Fill fields based on relevance, using 'Unknown' for missing details. Only include text in 'Compliance Notes' if it specifically relates to compliance or regulatory observations; otherwise, leave it 'Unknown'. Use <b> tags for field names and <br> for line breaks. Do not wrap the output in code blocks (e.g., ```html).
        Template:
        <b>Job Support Compliance Report (to Government Agencies)</b><br>
        <b>Date:</b> <br>
        <b>Client Name:</b> <br>
        <b>Supervisor/Coach Name:</b> <br>
        <b>Disability:</b> <br>
        <b>Location:</b> <br>
        <b>Purpose:</b> <br>
        <b>Activity:</b> <br>
        <b>Support Provided:</b> <br>
        <b>Challenges Faced:</b> <br>
        <b>Follow-Up Actions Required:</b> <br>
        <b>Next Scheduled Check-In:</b> <br>
        <b>Compliance Notes:</b> <br>
        <b>State-Specific Regulations Applied:</b> <br>

        Text: 
        {raw_text}
        """
    elif report_type == "employer":
        prompt = f"""
        From the text below, generate an HTML report using this template. Fill fields based on relevance, using 'Unknown' for missing details. Only include text in 'Additional Notes' if it provides relevant extra context beyond other fields; otherwise, leave it 'Unknown'. Use <b> tags for field names and <br> for line breaks. Do not wrap the output in code blocks (e.g., ```html).
        Template:
        <b>Employee Progress Report (to Employer)</b><br>
        <b>Date:</b> <br>
        <b>Employee Name:</b> <br>
        <b>Supervisor/Coach Name:</b> <br>
        <b>Disability:</b> <br>
        <b>Activity Performed:</b> <br>
        <b>Performance Summary:</b> <br>
        <b>Job Readiness Skills Observed:</b> <br>
        <b>Areas for Improvement:</b> <br>
        <b>Employee Satisfaction Feedback:</b> <br>
        <b>Additional Notes:</b> <br>

        Text: 
        {raw_text}
        """
    else:
        raise ValueError(f"Unknown report type: {report_type}")

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a precise report generator outputting HTML for job coach notes for a supported employment program."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"OpenAI failed for {report_type} report: {str(e)}")
        return f"<b>Error</b><br>Failed to generate {report_type} report."