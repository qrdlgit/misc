import os
import openai
import requests
import json

# Set up the OpenAI API client
openai.api_key = os.environ["OPENAI_API_KEY"]

# Define the prompt for GPT-3.5
prompt = "Review the following code based on the following rubric: ..."

# Call the GPT-3.5 API
response = openai.Completion.create(
    engine="text-davinci-002",  # Replace with the GPT-3.5 engine name when available
    prompt=prompt,
    max_tokens=150,
    n=1,
    stop=None,
    temperature=0.7,
)

# Extract the review from the API response
review = response.choices[0].text.strip()

# Get the pull request number and repository information from the environment
pr_number = os.environ["GITHUB_EVENT_PATH"]
repo = os.environ["GITHUB_REPOSITORY"]
token = os.environ["GITHUB_TOKEN"]

# Post the review as a comment on the pull request
headers = {"Authorization": f"token {token}", "Content-Type": "application/json"}
url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"

data = {
    "body": f"GPT-3.5 review:\n\n{review}",
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code != 201:
    print("Error posting the review comment.")
    print(response.text)
else:
    print("Review comment posted successfully.")
