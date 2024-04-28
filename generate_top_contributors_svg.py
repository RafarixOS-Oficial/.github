import requests
import os

REPO = os.getenv('GITHUB_REPOSITORY')
TOKEN = os.getenv('GITHUB_TOKEN')
API_URL = f"https://api.github.com/repos/{REPO}/contributors"

def fetch_contributors():
    headers = {'Authorization': f'token {TOKEN}'}
    response = requests.get(API_URL, headers=headers)
    if response.status_code != 200:
        print("Error fetching contributors")
        return []
    contributors = response.json()
    return contributors[:3]

def generate_svg(contributor, rank):
    commits = contributor['contributions']
    user = contributor['login']
    return f"""
<svg width="300" height="100" xmlns="http://www.w3.org/2000/svg">
  <style>
    .title {{ font: bold 24px sans-serif; }}
    .user {{ font: italic 20px sans-serif; fill: red; }}
  </style>
  <rect x="10" y="10" width="280" height="80" fill="grey" />
  <text x="150" y="35" class="title" text-anchor="middle" fill="white">TOP {rank} ({commits} commits)</text>
  <text x="150" y="70" class="user" text-anchor="middle">{user}</text>
</svg>
"""

def main():
    contributors = fetch_contributors()
    for i, contributor in enumerate(contributors):
        svg_content = generate_svg(contributor, i+1)
        with open(f'top_{i+1}.svg', 'w') as file:
            file.write(svg_content.strip())

if __name__ == "__main__":
    main()
