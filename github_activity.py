import requests
import sys
from datetime import datetime 

def github_fetch(username):

    url = f"https://api.github.com/users/{username}/events"

    try:
        response = request.get(url)

        if response.status_code == 404:
            print(f"Error: User '{username}' not found")
            return None
        elif response.status_code != 200:
            print(f"Error: Unable to fetch data (Status code: {response.status.code})")
            return None
        
        return response.json()
    
    except requests.exceptions.RequestException as exc:
        print(f"Error: Network error ocurred - {exc}")
        return None
    


def format_activity(events):

    if not events:
        print("No recent activitiy found.")
        return
    
    print(f"\nDisplaying {len(events)} recent activities:\n")

    event_formatter = {
        'PushEvent': lambda e: f"Pushed {len(e['payload'].get('commits', []))} commit(s) to {e['repo']['name']}",
        'CreateEvent': lambda e: f"Created {e['payload'].get('ref_type', 'repository')} in {e['repo']['name']}",
        'DeleteEvent': lambda e: f"Deleted {e['payload'].get('ref_type', 'branch')} in {e['repo']['name']}",
        'IssuesEvent': lambda e: f"{e['payload']['action'].capitalize()} an issue in {e['repo']['name']}",
        'PullRequestEvent': lambda e: f"{e['payload']['action'].capitalize()} a pull request in {e['repo']['name']}",
        'WatchEvent': lambda e: f"Starred {e['repo']['name']}",
        'ForkEvent': lambda e: f"Forked {e['repo']['name']}",
    }

    for event in events: 
        event_type = event['type']
        created_at = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        date_str = created_at.strftime('%Y-%m-%d %H:%M')

        formatter = event_formatter.get(
            event_type, 
            lambda e: f"{e['type'].replace('Event', '')} in {e['repo']['name']}"
        )

        activity_msg = formatter(event)
        print(f"- {activity_msg} [{date_str}]")

def main():
    if len(sys.argv) < 2:
        print("Usage: python github_activity.py <github_username>")
        sys.exit(1)
    
    username = sys.argv[1]
    print(f"Fetching activity for GitHub user: {username}...")
    
    events = github_fetch(username)
    
    if events is not None:
        format_activity(events)


if __name__ == "__main__":
    main()