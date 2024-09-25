from flask import Flask, jsonify, abort
from students import read 
import sqlite3
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')

app = Flask(__name__)

github_usernames = {
    1: 'NikoKiru',
    2: 'markus-rk',
    3: 'BirkLauritzen',
    4: 'ChristianBT96',
    5: 'DetGrey',
    6: 'behu-kea',
    7: 'ViktorBach',
    8: 'Natazja',
    9: 'SofieAmalie44',
    10: 'LucasFJ-2023'
}

def fetch_github_repos(username, is_self=False):
    try:
        
        url = f"https://api.github.com/users/{username}/repos"
        
       
        if is_self:
            url = "https://api.github.com/user/repos"
        
        headers = {
            "Authorization": f"token {GITHUB_ACCESS_TOKEN}"
        }
        
        
        response = requests.get(url, headers=headers)
       
        repos = [{"name": repo["name"], "url": repo["html_url"]} for repo in response.json()]
        return repos
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for {username}: {http_err}")
        return []
    except Exception as err:
        print(f"Error fetching repos for {username}: {err}")
        return []


    
    
@app.route('/members', methods=['GET'])
def get_members():
    try:
        members = read()

        for member in members:
            username = member['github_username']

            if member['id'] == 1:
                member['github_repositories'] = fetch_github_repos(username, is_self=True)
            else:
                member['github_repositories'] = fetch_github_repos(username)
        
        return jsonify(members), 200
    except Exception as e:
        abort(500, description=str(e))

@app.route('/members/<int:member_id>', methods=['GET'])
def get_member_by_id(member_id):
    try:
        members = read()
        member = next((m for m in members if m['id'] == member_id), None)
        if member is None:
            abort(404, description="Member not found")
        
        username = member['github_username']
        if member_id == 1:
            member['github_repositories'] = fetch_github_repos(username, is_self=True)
        else:
            member['github_repositories'] = fetch_github_repos(username)
        
        return jsonify(member), 200
    except Exception as e:
        abort(500, description=str(e))

@app.route('/members/update-github-usernames', methods=['PUT'])
def update_github_usernames():
    try:
        
        with sqlite3.connect('school.db') as conn:
            cur = conn.cursor()
            
          
            for member_id, github_username in github_usernames.items():
                cur.execute(
                    '''
                    UPDATE members
                    SET github_username = ?
                    WHERE id = ?
                    ''', (github_username, member_id)
                )
            
            conn.commit()  

        return jsonify({"message": "GitHub usernames updated successfully"}), 200
    except Exception as e:
        abort(500, description=str(e))

if __name__ == '__main__':
    app.run(debug=True)