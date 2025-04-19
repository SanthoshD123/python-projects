import requests
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import argparse
import os
from collections import Counter
import json
from dateutil import parser as date_parser

class GitHubProfileAnalyzer:
    def __init__(self, username, token=None):
        """
        Initialize the GitHub Profile Analyzer with a username and optional token.
        
        Args:
            username (str): GitHub username to analyze
            token (str, optional): GitHub personal access token for API authentication
        """
        self.username = username
        self.headers = {}
        if token:
            self.headers = {'Authorization': f'token {token}'}
        self.base_url = 'https://api.github.com'
        self.profile_data = None
        self.repos_data = None
        self.languages_data = None
        self.contributions_data = None
        
    def fetch_profile(self):
        """Fetch basic profile information."""
        url = f"{self.base_url}/users/{self.username}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            self.profile_data = response.json()
            return self.profile_data
        else:
            print(f"Error fetching profile: {response.status_code}")
            return None
    
    def fetch_repositories(self):
        """Fetch all public repositories."""
        url = f"{self.base_url}/users/{self.username}/repos?per_page=100"
        all_repos = []
        
        while url:
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                print(f"Error fetching repositories: {response.status_code}")
                break
                
            repos = response.json()
            all_repos.extend(repos)
            
            # Check if there are more pages
            if 'next' in response.links:
                url = response.links['next']['url']
            else:
                url = None
                
        self.repos_data = all_repos
        return self.repos_data
    
    def analyze_languages(self):
        """Analyze programming languages used across repositories."""
        if self.repos_data is None:
            self.fetch_repositories()
            
        languages = {}
        for repo in self.repos_data:
            if repo['language']:
                languages[repo['language']] = languages.get(repo['language'], 0) + 1
                
        self.languages_data = languages
        return languages
    
    def fetch_contribution_activity(self):
        """Fetch contribution activity for the past year."""
        # This is a simplified version - GitHub API doesn't directly provide contribution data
        # We'll use commits to user's repos as a proxy
        if self.repos_data is None:
            self.fetch_repositories()
            
        contributions = []
        # Limit to top 5 repos by star count to avoid hitting rate limits
        top_repos = sorted(self.repos_data, key=lambda x: x['stargazers_count'], reverse=True)[:5]
        
        for repo in top_repos:
            url = f"{self.base_url}/repos/{self.username}/{repo['name']}/commits?author={self.username}&per_page=100"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                commits = response.json()
                for commit in commits:
                    if 'commit' in commit and 'author' in commit['commit'] and commit['commit']['author']['date']:
                        contributions.append({
                            'date': commit['commit']['author']['date'],
                            'repo': repo['name'],
                            'type': 'commit'
                        })
        
        self.contributions_data = contributions
        return contributions
    
    def get_profile_summary(self):
        """Generate a summary of the user's profile."""
        if self.profile_data is None:
            self.fetch_profile()
            
        if not self.profile_data:
            return "Unable to fetch profile data."
            
        created_at = datetime.strptime(self.profile_data['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        account_age = (datetime.now() - created_at).days
        
        summary = {
            'username': self.profile_data['login'],
            'name': self.profile_data['name'] or 'Not provided',
            'bio': self.profile_data['bio'] or 'Not provided',
            'location': self.profile_data['location'] or 'Not provided',
            'public_repos': self.profile_data['public_repos'],
            'followers': self.profile_data['followers'],
            'following': self.profile_data['following'],
            'join_date': created_at.strftime('%Y-%m-%d'),
            'account_age_days': account_age
        }
        
        return summary
    
    def get_repository_stats(self):
        """Generate statistics about the user's repositories."""
        if self.repos_data is None:
            self.fetch_repositories()
            
        if not self.repos_data:
            return "Unable to fetch repository data."
            
        total_stars = sum(repo['stargazers_count'] for repo in self.repos_data)
        total_forks = sum(repo['forks_count'] for repo in self.repos_data)
        
        # Sort repos by stars and forks
        top_repos_by_stars = sorted(self.repos_data, key=lambda x: x['stargazers_count'], reverse=True)[:5]
        top_repos_by_forks = sorted(self.repos_data, key=lambda x: x['forks_count'], reverse=True)[:5]
        
        stats = {
            'total_repos': len(self.repos_data),
            'total_stars': total_stars,
            'total_forks': total_forks,
            'avg_stars_per_repo': total_stars / len(self.repos_data) if self.repos_data else 0,
            'top_repos_by_stars': [{
                'name': repo['name'],
                'stars': repo['stargazers_count'],
                'description': repo['description'] or 'No description'
            } for repo in top_repos_by_stars],
            'top_repos_by_forks': [{
                'name': repo['name'],
                'forks': repo['forks_count'],
                'description': repo['description'] or 'No description'
            } for repo in top_repos_by_forks]
        }
        
        return stats
    
    def visualize_languages(self, output_file=None):
        """Generate a pie chart of programming languages used."""
        if self.languages_data is None:
            self.analyze_languages()
            
        if not self.languages_data:
            return "No language data available."
            
        # Get top 8 languages and group the rest as 'Other'
        sorted_languages = sorted(self.languages_data.items(), key=lambda x: x[1], reverse=True)
        labels = []
        sizes = []
        
        if len(sorted_languages) > 8:
            for lang, count in sorted_languages[:7]:
                labels.append(lang)
                sizes.append(count)
            other_count = sum(count for _, count in sorted_languages[7:])
            labels.append('Other')
            sizes.append(other_count)
        else:
            labels = [lang for lang, _ in sorted_languages]
            sizes = [count for _, count in sorted_languages]
        
        # Create pie chart
        plt.figure(figsize=(10, 7))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title(f'Programming Languages Used by {self.username}')
        
        if output_file:
            plt.savefig(output_file)
            return f"Language visualization saved to {output_file}"
        else:
            plt.show()
            return "Language visualization displayed"
    
    def visualize_activity(self, output_file=None):
        """Generate a bar chart of contribution activity by month."""
        if self.contributions_data is None:
            self.fetch_contribution_activity()
            
        if not self.contributions_data:
            return "No contribution data available."
            
        # Parse dates and group by month
        for contrib in self.contributions_data:
            contrib['parsed_date'] = date_parser.parse(contrib['date'])
            
        monthly_counts = Counter()
        for contrib in self.contributions_data:
            month_year = contrib['parsed_date'].strftime('%Y-%m')
            monthly_counts[month_year] += 1
            
        # Sort by date
        sorted_months = sorted(monthly_counts.items())
        months = [m[0] for m in sorted_months]
        counts = [m[1] for m in sorted_months]
        
        # Create bar chart
        plt.figure(figsize=(12, 6))
        plt.bar(months, counts)
        plt.xticks(rotation=45)
        plt.xlabel('Month')
        plt.ylabel('Contributions')
        plt.title(f'Monthly Contributions by {self.username}')
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file)
            return f"Activity visualization saved to {output_file}"
        else:
            plt.show()
            return "Activity visualization displayed"
    
    def generate_report(self, output_file=None):
        """Generate a comprehensive report on the GitHub profile."""
        profile_summary = self.get_profile_summary()
        repo_stats = self.get_repository_stats()
        languages = self.analyze_languages()
        
        # Sort languages by usage count
        sorted_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)
        
        report = {
            'profile_summary': profile_summary,
            'repository_stats': repo_stats,
            'top_languages': dict(sorted_languages[:10]),
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            return f"Report saved to {output_file}"
        else:
            return report

def main():
    parser = argparse.ArgumentParser(description='Analyze GitHub profiles')
    parser.add_argument('username', help='GitHub username to analyze')
    parser.add_argument('--token', help='GitHub personal access token')
    parser.add_argument('--output', help='Output folder for visualizations and reports')
    args = parser.parse_args()
    
    analyzer = GitHubProfileAnalyzer(args.username, args.token)
    
    # Create output directory if specified
    if args.output:
        os.makedirs(args.output, exist_ok=True)
        lang_vis_path = os.path.join(args.output, f"{args.username}_languages.png")
        activity_vis_path = os.path.join(args.output, f"{args.username}_activity.png")
        report_path = os.path.join(args.output, f"{args.username}_report.json")
    else:
        lang_vis_path = None
        activity_vis_path = None
        report_path = None
    
    # Run analysis
    print(f"Analyzing GitHub profile for {args.username}...")
    
    profile = analyzer.fetch_profile()
    if not profile:
        print("Failed to fetch profile data. Check the username or your API rate limits.")
        return
    
    print("\nProfile Summary:")
    summary = analyzer.get_profile_summary()
    print(f"Name: {summary['name']}")
    print(f"Bio: {summary['bio']}")
    print(f"Location: {summary['location']}")
    print(f"Account created: {summary['join_date']} ({summary['account_age_days']} days ago)")
    print(f"Followers: {summary['followers']}")
    print(f"Following: {summary['following']}")
    print(f"Public repositories: {summary['public_repos']}")
    
    print("\nRepository Statistics:")
    repos = analyzer.get_repository_stats()
    print(f"Total repositories: {repos['total_repos']}")
    print(f"Total stars received: {repos['total_stars']}")
    print(f"Total forks received: {repos['total_forks']}")
    print(f"Average stars per repository: {repos['avg_stars_per_repo']:.1f}")
    
    print("\nTop Repositories by Stars:")
    for i, repo in enumerate(repos['top_repos_by_stars'], 1):
        print(f"{i}. {repo['name']} - {repo['stars']} stars")
        print(f"   {repo['description']}")
    
    print("\nLanguage Analysis:")
    analyzer.analyze_languages()
    vis_result = analyzer.visualize_languages(lang_vis_path)
    print(vis_result)
    
    print("\nContribution Activity:")
    activity_result = analyzer.visualize_activity(activity_vis_path)
    print(activity_result)
    
    print("\nGenerating comprehensive report...")
    report_result = analyzer.generate_report(report_path)
    if isinstance(report_result, str):
        print(report_result)
    else:
        print("Report generated successfully.")
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()
