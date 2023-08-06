'''
            OCTOSUITE Advanced Github OSINT Framework
                Copyright (C) 2022  Richard Mwewa

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
'''

import os
import sys
import logging
import getpass
import requests
import platform
import subprocess
from pprint import pprint
from datetime import datetime
from octosuite.helper import Help
from octosuite.misc import Banner
from octosuite.colors import Color


'''
logRoller
This class is where the main notification strings/messages are held,
and are being used in two different cases (they're beig used by logging to be written to log files, and being printed out to the screen).
'''
class logRoller:
    Ctrl = 'Session terminated with {}.'
    Error = 'An error occurred: {}'
    sessionOpened = 'Opened new session on {}:{}'
    sessionClosed = 'Session closed with {} command.'
    deletedLog = 'Deleted log: {}'
    readingLog = 'Reading log: {}'
    viewingLogs = 'Viewing logs...'
    fileNotFound = 'File ({}) not found.'
    infoNotFound = 'Information ({} - {} - {}) not found.'
    repoNotFound = 'Repository ({}) not found.'
    tagNotFound = 'Tag ({}) not found.'
    userNotFound = 'User (@{}) not found.'
    orgNotFound = 'Organization (@{}) not found.'
    repoOrUserNotFound = 'Repository or user not found ({} - @{}).'


'''
pathFinder
*I couldn't think of a good name for this.*
The pathFinder is responsible for creating/checking the availability of the .logs folder
and enabling logging to automatically log network/user activity to a file.
'''
class pathFinder:
    # If .logs folder exists, we ignore (pass)
    if os.path.exists('.logs'):
        pass
    else:
        '''
        Creating the .logs directory
        If the current system is Windows based, we run mkdir command (without sudo?)
        Else we run the mkdir command (with sudo)
        As of writing, I have absolutely no idea if Windows users also use sudo to run commands as root/admin
        '''
        if sys.platform.lower().startswith(('win','darwin')):
            subprocess.run(['mkdir','.logs'])
        else:
            subprocess.run(['sudo','mkdir','.logs'],shell=False)
            
    '''
    Set to automatically monitor and log network and user activity into the .logs folder.
    Logs will be saved by date and time for each session.
    '''
    now = datetime.now()
    now_formatted = now.strftime('%Y-%m-%d %H:%M:%S%p')
    logging.basicConfig(filename=f'.logs/{now_formatted}.log', format='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S%p', level=logging.DEBUG)
    

'''
Attributes
*Even here, I couldn't think of a good name.*
The Attributes class holds the signs/symbols that show what a notification in OctoSuite might be all about.
This might not be very important or necessary in some cases, but I think it's better to know the severerity of the notifications you get in a program.
'''
class Attributes:
	prompt = f'{Color.white}[{Color.green} ? {Color.white}]{Color.reset}'
	warning = f'{Color.white}[{Color.red} ! {Color.white}]{Color.reset}'
	error = f'{Color.white}[{Color.red} x {Color.white}]{Color.reset}'
	positive = f'{Color.white}[{Color.green} + {Color.white}]{Color.reset}'
	negative = f'{Color.white}[{Color.red} - {Color.white}]{Color.reset}'
	info = f'{Color.white}[{Color.green} * {Color.white}]{Color.reset}'


def orgProfile(org_attrs, org_attr_dict, endpoint):
    organization = input(f'{Color.white}--> @{Color.green}Organization{Color.white} (username){Color.reset} ')
    response = requests.get(f'{endpoint}/orgs/{organization}')
    if response.status_code == 404:
    	print(Attributes.negative, logRoller.userNotFound.format(username))
    else:
    	print(f"\n{Color.white}{response.json()['name']}{Color.reset}")
    	for attr in org_attrs:
    		print(f'{Color.white}├─ {org_attr_dict[attr]}: {Color.green}{response.json()[attr]}{Color.reset}')
    
                        
# Fetching user information        
def userProfile(profile_attrs, profile_attr_dict, endpoint):
    username = input(f'\n{Color.white}--> @{Color.green}Username{Color.reset} ')
    response = requests.get(f'{endpoint}/users/{username}')
    if response.status_code == 404:
    	print(f'\n{Color.white}[{Color.red} - {Color.white}] User ({username}) not found.{Color.reset}')
    else:
    	print(f"\n{Color.white}{response.json()['name']}{Color.reset}")
    	for attr in profile_attrs:
    		print(f'{Color.white}├─ {profile_attr_dict[attr]}: {Color.green}{response.json()[attr]}{Color.reset}')

        	        	
# Fetching repository information   	
def repoProfile(repo_attrs, repo_attr_dict, endpoint):
    repo_name = input(f'\n{Color.white}--> %{Color.green}Repo{Color.reset} ')
    username = input(f'{Color.white}--> @{Color.green}Owner{Color.white} (username){Color.reset} ')
    response = requests.get(f'{endpoint}/repos/{username}/{repo_name}')
    if response.status_code == 404:
    	print(f'\n{Color.white}[{Color.red} - {Color.white}] Repository ({repo_name}) or user ({username}) not found.{Color.reset}')
    else:
    	response = response.json()
    	print(f"\n{Color.white}{response.json()['full_name']}{Color.reset}")
    	for attr in repo_attrs:
    	    print(f"{Color.white}├─ {repo_attr_dict[attr]}: {Color.green}{response.json()[attr]}{Color.reset}")
        
    
# Get path contents        
def pathContents(path_attrs, path_attr_dict, endpoint):
    repo_name = input(f'\n{Color.white}--> %{Color.green}Repo{Color.reset} ')
    username = input(f'{Color.white}--> @{Color.green}Owner{Color.white} (username){Color.reset} ')
    path_name = input(f'{Color.white}--> ~{Color.green}/path/name{Color.reset} ')
    response = requests.get(f'{endpoint}/repos/{username}/{repo_name}/contents/{path_name}')
    if response.status_code == 404:
        print(f'\n{Color.white}[{Color.red} - {Color.white}] Information not found.{Color.reset}')
    else:
    	response = response.json()
    	for item in response:
    	    print(f"\n{Color.white}{item['name']}{Color.reset}")
    	    for attr in path_attrs:
    	    	print(f'{Color.white}├─ {path_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}')
    	    	
    	    	
# repo contributors
def repoContributors(user_attrs, user_attr_dict, endpoint):
    repo_name = input(f'{Color.white}--> %{Color.green}Repo{Color.reset} ')
    username = input(f'{Color.white}--> @{Color.green}Owner{Color.white} (username){Color.reset} ')
    response = requests.get(f'{endpoint}/repos/{username}/{repo_name}/contributors')
    if response.status_code == 404:
        print(Attributes.negative, logRoller.repoOrUserNotFound.format(repo_name, username))
    else:
        for item in response.json():
            print(f"\n{Color.white}{item['login']}{Color.reset}")
            for attr in user_attrs:
            	print(f'{Color.white}├─ {user_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}')
            	
            	
# repo downloads
def repoLanguages(endpoint):
    repo_name = input(f'{Color.white}--> %{Color.green}Repo{Color.reset} ')
    username = input(f'{Color.white}--> @{Color.green}Owner{Color.white} (username){Color.reset} ')
    response = requests.get(f'{endpoint}/repos/{username}/{repo_name}/languages')
    if response.status_code == 404:
        print(Attributes.negative, logRoller.repoOrUserNotFound.format(repo_name, username))
    elif response.json() == {}:
        print(f'{Attributes.negative} Repository ({repo_name}) language(s) unavailabile.{Color.reset}')
    else:
        print(f'\n{Color.white}{username}/{repo_name}{Color.reset}')
        for language in response.json():
            print(f'{Color.white}├─ {Color.green}{language}{Color.reset}')
            
            
# repo stargazers
def repoStargazers(user_attrs, user_attr_dict, endpoint):
    repo_name = input(f'{Color.white}--> %{Color.green}Repo{Color.reset} ')
    username = input(f'{Color.white}--> @{Color.green}Owner{Color.white} (username){Color.reset} ')
    response = requests.get(f'{endpoint}/repos/{username}/{repo_name}/stargazers')
    if response.status_code == 404:
        print(Attributes.negative, logRoller.repoOrUserNotFound.format(repo_name, username))
    elif response.json() == {}:
        print(f'{Attributes.negative} Repository ({repo_name}) does not have any stargazers.{Color.reset}')
    else:
        for item in response.json():
            print(f"\n{Color.white}{item['login']}{Color.reset}")
            for attr in  user_attrs:
                print(f'{Color.white}├─ {user_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}')
                
                
# repo forks
def repoForks(repo_attrs, repo_attr_dict, endpoint):
    repo_name = input(f'{Color.white}--> %{Color.green}Repo{Color.reset} ')
    username = input(f'{Color.white}--> @{Color.green}Owner{Color.white} (username){Color.reset} ')
    response = requests.get(f'{endpoint}/repos/{username}/{repo_name}/forks')
    if response.status_code == 404:
        print(Attributes.negative, logRoller.repoOrUserNotFound.format(repo_name, username))
    elif response.json() == {}:
        print(f'{Attributes.negative} Repository ({repo_name}) does not have forks.{Color.reset}')
    else:
        for item in response.json():
            print(f"\n{Color.white}{item['full_name']}{Color.reset}")
            for attr in  repo_attrs:
                print(f'{Color.white}├─ {repo_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}')
                
                
# Repo issues
def repoIssues(repo_issues_attrs, repo_issues_attr_dict, endpoint):
    repo_name = input(f'{Color.white}--> %{Color.green}Repo{Color.reset} ')
    username = input(f'{Color.white}--> @{Color.green}Owner{Color.white} (username){Color.reset} ')
    response = requests.get(f'{endpoint}/repos/{username}/{repo_name}/issues')
    if response.status_code == 404:
        print(Attributes.negative, logRoller.repoOrUserNotFound.format(repo_name, username))
    elif response.json() == []:
        print(f'{Attributes.negative} Repository ({repo_name}) does not have open issues.{Color.reset}')
    else:
    	for item in response.json():
    	    print(f"\n{Color.white}{item['title']}{Color.reset}")
    	    for attr in  repo_issues_attrs:
    	        print(f'{Color.white}├─ {repo_issues_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}')
    	    print(item['body'])
 
 
 # Repo releases
def repoReleases(repo_releases_attrs, repo_releases_attr_dict, endpoint):
    repo_name = input(f'{Color.white}--> %{Color.green}Repo{Color.reset} ')
    username = input(f'{Color.white}--> @{Color.green}Owner{Color.white} (username){Color.reset} ')
    response = requests.get(f'{endpoint}/repos/{username}/{repo_name}/releases')
    if response.status_code == 404:
    	 print(Attributes.negative, logRoller.repoOrUserNotFound.format(repo_name, username))
    elif response.json() == []:
        print(f"\n{Attributes.negative} Repository ({repo_name}) does not have releases.{Color.reset}")
    else:
        for item in response.json():
        	print(f"\n{Color.white}{item['name']}{Color.reset}")
        	for attr in repo_releases_attrs:
        	    print(f'{Color.white}├─ {repo_releases_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}')
        	print(item['body'])


# Fetching organization repositories        
def orgRepos(repo_attrs, repo_attr_dict, endpoint):
    organization = input(f'{Color.white}--> @{Color.green}Organization{Color.white} (username){Color.reset} ')
    response = requests.get(f'{endpoint}/orgs/{organization}/repos?per_page=100')
    if response.status_code == 404:
        print(Attributes.negative, logRoller.orgNotFound.format(organization))
    else:
        for repo in response.json():
        	print(f"\n{Color.white}{repo['full_name']}{Color.reset}")
        	for attr in repo_attrs:
        		print(f"{Color.white}├─ {repo_attr_dict[attr]}: {Color.green}{repo[attr]}{Color.reset}")
        		
        		
# organization events        
def orgEvents(endpoint):
    organization = input(f"{Color.white}--> @{Color.green}Organization{Color.white} (username){Color.reset} ")
    response = requests.get(f'{endpoint}/orgs/{organization}/events')
    if response.status_code == 404:
        print(Attributes.negative, logRoller.orgNotFound.format(organization))
    else:
        for item in response.json():
        	print(f"\n{Color.white}{item['id']}{Color.reset}")
        	print(f"{Color.white}├─ Type: {Color.green}{item['type']}{Color.reset}\n{Color.white}├─ Created at: {Color.green}{item['created_at']}{Color.green}")
        	pprint(item['payload'])
        	print(f"{Color.reset}\n")
        	
        	
# organization member        	
def orgMember(endpoint):
    organization = input(f"{Color.white}--> @{Color.green}Organization{Color.white} (username){Color.reset} ")
    username = input(f'{Color.white}--> @{Color.green}Username{Color.reset} ')
    response = requests.get(f'{endpoint}/orgs/{organization}/public_members/{username}')
    if response.status_code == 204:
        print(f"{Attributes.positive} User is a public member of the organization{Color.reset}")
    else:
    	print(f"{Attributes.negative} {response.json()['message']}{Color.reset}")
 
   
# Fetching user repositories        
def userRepos(repo_attrs, repo_attr_dict, endpoint):
    username = input(f'{Color.white}--> @{Color.green}Username{Color.reset} ')
    response = requests.get(f'{endpoint}/users/{username}/repos?per_page=100')
    if response.status_code == 404:
    	print(Attributes.negative, logRoller.userNotFound.format(username))
    else:
    	for repo in response.json():
    		print(f"\n{Color.white}{repo['full_name']}{Color.reset}")
    		for attr in repo_attrs:
    			print(f"{Color.white}├─ {repo_attr_dict[attr]}: {Color.green}{repo[attr]}{Color.reset}")	        	


# Fetching user's gists
def userGists(gists_attrs, gists_attr_dict, endpoint):
    username = input(f'{Color.white}--> @{Color.green}Username{Color.reset} ')
    response = requests.get(f'{endpoint}/users/{username}/gists')
    if response.json() == []:
    	print(f'{Attributes.negative} User does not have any active gists.{Color.reset}')
    elif response.status_code == 404:
    	print(Attributes.negative, logRoller.userNotFound.format(username))
    else:
        for item in response.json():
        	print(f"\n{Color.white}{item['id']}{Color.reset}")
        	for attr in gists_attrs:
        		print(f"{Color.white}├─ {gists_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}")
        		
        		
# Fetching a list of organizations that a user owns or belongs to        	
def userOrgs(user_orgs_attrs, user_orgs_attr_dict, endpoint):
    username = input(f'{Color.white}--> @{Color.green}Username{Color.reset} ')
    response = requests.get(f'{endpoint}/users/{username}/orgs')
    if response.json() == []:
        print(f'{Attributes.negative} User does not belong to or own any organizations.{Color.reset}')
    elif response.status_code == 404:
       print(Attributes.negative, logRoller.userNotFound.format(username))
    else:
    	for item in response.json():
    	    print(f'\n{Color.white}{item["login"]}{Color.reset}')
    	    for attr in user_orgs_attrs:
    	        print(f'{Color.white}├─ {user_orgs_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}')
    	        
    	        
# Fetching a users events 
def userEvents(endpoint):
    username = input(f'{Color.white}--> @{Color.green}Username{Color.reset} ')
    response = requests.get(f'{endpoint}/users/{username}/events/public')
    if response.status_code == 404:
        print(Attributes.negative, logRoller.userNotFound.format(username))
    else:
        for item in response.json():
        	print(f"\n{Color.white}{item['id']}{Color.reset}")
        	print(f"{Color.white}├─ Type: {Color.green}{item['type']}{Color.reset}\n{Color.white}├─ Created at: {Color.green}{item['created_at']}{Color.green}")
        	pprint(item['payload'])
        	print(reset)
        	
        	
# Fetching a target user's subscriptions 
def userSubscriptions(repo_attrs, repo_attr_dict, endpoint):
    username = input(f'{Color.white}--> @{Color.green}Username{Color.reset} ')
    response = requests.get(f'{endpoint}/users/{username}/subscriptions')
    if response.json() == []:
    	print(f"{Attributes.negative} User does not have any subscriptions.{Color.reset}")
    elif response.status_code == 404:
        print(Attributes.negative, logRoller.userNotFound.format(username))
    else:
    	for item in response.json():
    		print(f"\n{Color.white}{item['full_name']}{Color.reset}")
    		for attr in repo_attrs:
    			print(f"{Color.white}├─ {repo_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}")
    			
    			
# Fetching user's followera'    	    
def userFollowers(user_attrs, user_attr_dict, endpoint):
    username = input(f'{Color.white}--> @{Color.green}Username{Color.reset} ')
    response = requests.get(f'{endpoint}/users/{username}/followers?per_page=100')
    if response.json() == []:
    	print(f'{Attributes.negative} User does not have followers.{Color.reset}')
    elif response.status_code == 404:
    	print(Attributes.negative, logRoller.userNotFound.format(username))
    else:
        for item in response.json():
        	print(f"\n{Color.white}@{item['login']}{Color.reset}")
        	for attr in user_attrs:
        		print(f"{Color.white}├─ {user_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}")
        		
        		
# Checking whether or not user[A] follows user[B]            
def userFollowing(endpoint):
    user_a = input(f'{Color.white}--> @{Color.green}user{Color.white}[A] (username){Color.reset} ')
    user_b = input(f'{Color.white}--> @{Color.green}user{Color.white}[B] (username){Color.reset} ')
    response = requests.get(f'{endpoint}/users/{user_a}/following/{user_b}')
    if response.status_code == 204:
    	print(f'{Attributes.positive} @{user_a} follows @{user_b}{Color.reset}')
    else:
    	print(f'{Attributes.negative} @{user_a} does not follow @{user_b}{Color.reset}')
    	
    	
# User search    	    
def userSearch(user_attrs, user_attr_dict, endpoint):
    query = input(f'{Color.white}--> @{Color.green}Query{Color.white} (eg. john){Color.reset} ')
    response = requests.get(f'{endpoint}/search/users?q={query}&per_page=100').json()
    for item in response['items']:
    	print(f"\n{Color.white}@{item['login']}{Color.reset}")
    	for attr in user_attrs:
    		print(f"{Color.white}├─ {user_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}")
    		
    		
# Repository search
def repoSearch(repo_attrs, repo_attr_dict, endpoint):
    query = input(f'{Color.white}--> %{Color.green}Query{Color.white} (eg. git){Color.reset} ')
    response = requests.get(f'{endpoint}/search/repositories?q={query}&per_page=100').json()
    for item in response['items']:
        print(f"\n{Color.white}{item['full_name']}{Color.reset}")
        for attr in repo_attrs:
            print(f"{Color.white}├─ {repo_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}")
            
            
# Topics search
def topicSearch(topic_attrs, topic_attr_dict, endpoint):
    query = input(f'{Color.white}--> #{Color.green}Query{Color.white} (eg. osint){Color.reset} ')
    response = requests.get(f'{endpoint}/search/topics?q={query}&per_page=100').json()
    for item in response['items']:
        print(f"\n{Color.white}{item['name']}{Color.reset}")
        for attr in topic_attrs:
            print(f"{Color.white}├─ {topic_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}")
            
            
# Issue search
def issueSearch(issue_attrs, issue_attr_dict, endpoint):
    query = input(f'{Color.white}--> !{Color.green}Query{Color.white} (eg. error){Color.reset} ')
    response = requests.get(f'{endpoint}/search/issues?q={query}&per_page=100').json()
    for item in response['items']:
        print(f"\n\n{Color.white}{item['title']}{Color.reset}")
        for attr in issue_attrs:
            print(f"{Color.white}├─ {issue_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}")
        print(item['body'])
        
        
# Commits search
def commitsSearch(endpoint):
    query = input(f'{Color.white}--> :{Color.green}Query{Color.white} (eg. filename:index.php){Color.reset} ')
    response = requests.get(f'{endpoint}/search/commits?q={query}&per_page=100').json()
    number=0
    for item in response['items']:
    	number+=1
    	print(f'\n{Color.white}-> {number}.{Color.reset}')
    	pprint(item['commit'])
    	
    	
# View octosuite log files    	
def viewLogs():
    logging.info(logRoller.viewingLogs)
    logs = os.listdir('.logs')
    print(f'''{Color.white}
Log                               Size{Color.reset}
---                               ---------''')
    for log in logs:
        print(f"{log}\t ",os.path.getsize(".logs/"+log),"bytes")
        
        
# Delete a specified log file    
def deleteLog():
    log_file = input(f"{Color.white}--> Log file (eg. 2022-04-27 10:09:36AM.log){Color.reset} ")
    if sys.platform.lower().startswith(('win','darwin')):
        subprocess.run(['del',f'{os.getcwd()}\.logs\{log_file}'])
    else:
        subprocess.run(['sudo','rm',f'.logs/{log_file}'],shell=False)
    
    logging.info(logRoller.deletedLog.format(log_file))
    print(Attributes.positive, logRoller.deletedLog)
    
    
# Read a specified log file    
def readLog():
    log_file = input(f"{Color.white}--> Log file (eg. 2022-04-27 10:09:36AM.log){Color.reset} ")
    with open(f'.logs/{log_file}', 'r') as log:
        logging.info(logRoller.readingLog.format(log_file))
        print("\n"+log.read())
        
        
# Show version information
def versionInfo():
	'''
    Yes... the changelog is actually hard coded
	It's actually frustrating having to change this everytime I publish a new release lol
    '''
	print(f'''
Tag: {Banner.versionTag}
Released at: 2022-06-15 12:30AM
{'-'*31}

What's changed?
{'-'*15}
[✓] Fixed a bug in issue #2
''')


# Author info
def author(author_dict):
    print(f'{Color.white}Richard Mwewa (Ritchie){Color.reset}')
    for key, value in author_dict.items():
    	print(f'{Color.white}├─ {key}: {Color.green}{value}{Color.reset}')
    	
    	
def about():
    print('''
     OCTOSUITE © 2022 Richard Mwewa
        
An advanced and lightning fast framework for gathering open-source intelligence on GitHub users and organizations.

Read the wiki: https://github.com/rly0nheart/octosuite/wiki
GitHub REST API documentation: https://docs.github.com/rest
        ''')
        
        
# Close session 	
def exitSession():
    logging.info(logRoller.sessionClosed.format('exit'))
    print(Attributes.info, logRoller.sessionClosed.format(f'{Color.green}exit{Color.reset}'));exit()
    

# Clear screen
def clearScreen():
    if sys.platform.lower().startswith(('win','darwin')):
        subprocess.run(['cls'])
    else:
        subprocess.run(['clear'],shell=False)


def Start():
    pathFinder()
    
    # API endpoint
    endpoint = 'https://api.github.com'
    # Path attribute
    path_attrs =['size','type','path','sha','html_url']
    # Path attribute dictionary
    path_attr_dict = {'size': 'Size (bytes)',
                      'type': 'Type',
                      'path': 'Path',
                      'sha': 'SHA',
                      'html_url': 'URL'}
                                             
                                             
    # Organization attributes
    org_attrs = ['avatar_url','login','id','node_id','email','description','blog','location','followers','following','twitter_username','public_gists','public_repos','type','is_verified','has_organization_projects','has_repository_projects','created_at','updated_at']
    # Organization attribute dictionary
    org_attr_dict = {'avatar_url': 'Profile Photo',
                     'login': 'Username',
                     'id': 'ID#',
                     'node_id': 'Node ID',
                     'email': 'Email',
                     'description': 'About',
                     'location': 'Location',
                     'blog': 'Blog',
                     'followers': 'Followers',
                     'following': 'Following',
                     'twitter_username': 'Twitter Handle',
                     'public_gists': 'Gists (public)',
                     'public_repos': 'Repositories (public)',
                     'type': 'Account type',
                     'is_verified': 'Is verified?',
                     'has_organization_projects': 'Has organization projects?',
                     'has_repository_projects': 'Has repository projects?',
                     'created_at': 'Created at',
                     'updated_at': 'Updated at'}
                                           
                                           
    # Repository attributes
    repo_attrs = ['id','description','forks','stargazers_count','watchers','license','default_branch','visibility','language','open_issues','topics','homepage','clone_url','ssh_url','fork','allow_forking','private','archived','has_downloads','has_issues','has_pages','has_projects','has_wiki','pushed_at','created_at','updated_at']
    # Repository attribute dictionary
    repo_attr_dict = {'id': 'ID#',
                      'description': 'About',
                      'forks': 'Forks',
                      'stargazers_count': 'Stars',
                      'watchers': 'Watchers',
                      'license': 'License',
                      'default_branch': 'Branch',
                      'visibility': 'Visibility',
                      'language': 'Language(s)',
                      'open_issues': 'Open issues',
                      'topics': 'Topics',
                      'homepage': 'Homepage',
                      'clone_url': 'Clone URL',
                      'ssh_url': 'SSH URL',
                      'fork': 'Is fork?',
                      'allow_forking': 'Is forkable?',
                      'private': 'Is private?',
                      'archived': 'Is archived?',
                      'is_template': 'Is template?',
                      'has_wiki': 'Has wiki?',
                      'has_pages': 'Has pages?',
                      'has_projects': 'Has projects?',
                      'has_issues': 'Has issues?',
                      'has_downloads': 'Has downloads?',
                      'pushed_at': 'Pushed at',
                      'created_at': 'Created at',
                      'updated_at': 'Updated at'}
                               
                               
    # Repo releases attributes
    repo_releases_attrs = ['node_id','tag_name','target_commitish','assets','draft','prerelease','created_at','published_at']
    # Repo releases attribute dictionary
    repo_releases_attr_dict = {'node_id': 'Node ID',
                               'tag_name': 'Tag',
                               'target_commitish': 'Branch',
                               'assets': 'Assets',
                               'draft': 'Is draft?',
                               'prerelease': 'Is prerelease?',
                               'created_at': 'Created at',
                               'published_at': 'Published at'}
                                              
                                              
    # Profile attributes
    profile_attrs = ['avatar_url','login','id','node_id','bio','blog','location','followers','following','twitter_username','public_gists','public_repos','company','hireable','site_admin','created_at','updated_at']
    # Profile attribute dictionary
    profile_attr_dict = {'avatar_url': 'Profile Photo',
                         'login': 'Username',
                         'id': 'ID#',
                         'node_id': 'Node ID',
                         'bio': 'Bio',
                         'blog': 'Blog',
                         'location': 'Location',
                         'followers': 'Followers',
                         'following': 'Following',
                         'twitter_username': 'Twitter Handle',
                         'public_gists': 'Gists (public)',
                         'public_repos': 'Repositories (public)',
                         'company': 'Organization',
                         'hireable': 'Is hireable?',
                         'site_admin': 'Is site admin?',
                         'created_at': 'Joined at',
                         'updated_at': 'Updated at'}
                                             
                                             
    # User attributes
    user_attrs = ['avatar_url','id','node_id','gravatar_id','site_admin','type','html_url']
    # User attribute dictionary
    user_attr_dict = {'avatar_url': 'Profile Photo',
                      'id': 'ID#',
                      'node_id': 'Node ID',
                      'gravatar_id': 'Gravatar ID',
                      'site_admin': 'Is site admin?',
                      'type': 'Account type',
                      'html_url': 'URL'}
                                             
                                         
    # Topic atrributes
    topic_attrs = ['score','curated','featured','display_name','created_by','created_at','updated_at']
    # Topic attribute dictionary
    topic_attr_dict = {'score': 'Score',
                       'curated': 'Curated',
                       'featured': 'Featured',
                       'display_name': 'Display Name',
                       'created_by': 'Created by',
                       'created_at': 'Created at',
                       'updated_at': 'Updated at'}
                                               
        
    # Gists attributes
    gists_attrs = ['node_id','description','comments','files','git_push_url','public','truncated','updated_at']
    # Gists attribute dictionary
    gists_attr_dict = {'node_id': 'Node ID',
                       'description': 'About',
                       'comments': 'Comments',
                       'files': 'Files',
                       'git_push_url': 'Git Push URL',
                       'public': 'Is public?',
                       'truncated': 'Is truncated?',
                       'updated_at': 'Updated at'}
                                              
                                              
    # Issue attributes
    issue_attrs = ['id','node_id','score','state','number','comments','milestone','assignee','assignees','labels','locked','draft','closed_at']
    # Issue attribute dict
    issue_attr_dict = {'id': 'ID#',
                       'node_id': 'Node ID',
                       'score': 'Score',
                       'state': 'State',
                       'closed_at': 'Closed at',
                       'number': 'Number',
                       'comments': 'Comments',
                       'milestone': 'Milestone',
                       'assignee': 'Assignee',
                       'assignees': 'Assignees',
                       'labels': 'Labels',
                       'draft': 'Is draft?',
                       'locked': 'Is locked?',
                       'created_at': 'Created at'}
                       
                           
    # Repo issues attributes
    repo_issues_attrs = ['id','node_id','state', 'reactions','number','comments','milestone','assignee','active_lock_reason', 'author_association','assignees','labels','locked','closed_at','created_at','updated_at']
    # Issue attribute dict
    repo_issues_attr_dict = {'id': 'ID#',
                             'node_id': 'Node ID',
                             'number': 'Number',
                             'state': 'State',
                             'reactions': 'Reactions',
                             'comments': 'Comments',
                             'milestone': 'Milestone',
                             'assignee': 'Assignee',
                             'assignees': 'Assignees',
                             'author_association': 'Author association',
                             'labels': 'Labels',
                             'locked': 'Is locked?',
                             'active_lock_reason': 'Lock reason',
                             'closed_at': 'Closed at',
                             'created_at': 'Created at',
                             'updated_at': 'Updated at'}
                                               
                                               
    # User organizations attributes
    user_orgs_attrs = ['avatar_url','id','node_id','url','description']
    user_orgs_attr_dict = {'avatar_url': 'Profile Photo',
                           'id': 'ID#',
                           'node_id': 'Node ID',
                           'url': 'URL',
                           'description': 'About'}
                                               
                                               
    # Author dictionary
    author_dict = {'Alias': 'rly0nheart',
                   'Country': 'Zambia, Africa',
                   'About.me': 'https://about.me/rly0nheart',
                   'BuyMeACoffee': 'https://buymeacoffee.com/189381184'}
                       
    
    logging.info(logRoller.sessionOpened.format(platform.node(), getpass.getuser()))
    print(Banner.nameLogo)                
    while True:
        try:
            command_input = input(f'''{Color.white}┌──({Color.red}{getpass.getuser()}{Color.white}@{Color.red}octosuite{Color.white})-[{Color.green}~{os.getcwd()}{Color.white}]\n└╼[{Color.green}:~{Color.white}]{Color.reset} ''').lower()
            print('\n')
            
            if command_input == 'org:events':
                orgEvents(endpoint)
            elif command_input == 'org:profile':
                orgProfile(org_attrs, org_attr_dict, endpoint)
            elif command_input == 'org:repos':
                orgRepos(repo_attrs, repo_attr_dict, endpoint)
            elif command_input == 'org:member':
                orgMember(endpoint)
            elif command_input == 'repo:pathcontents':
                pathContents(path_attrs, path_attr_dict, endpoint)
            elif command_input == 'repo:profile':
                repoProfile(repo_attrs, repo_attr_dict, endpoint)
            elif command_input == 'repo:contributors':
                repoContributors(user_attrs, user_attr_dict, endpoint)
            elif command_input == 'repo:languages':
                repoLanguages(endpoint)
            elif command_input == 'repo:stargazers':
                repoStargazers(user_attrs, user_attr_dict, endpoint)
            elif command_input == 'repo:forks':
                repoForks(repo_attrs, repo_attr_dict, endpoint)
            elif command_input == 'repo:issues':
                repoIssues(repo_issues_attrs, repo_issues_attr_dict, endpoint)
            elif command_input == 'repo:releases':
                repoReleases(repo_releases_attrs, repo_releases_attr_dict, endpoint)
            elif command_input == 'user:repos':
                userRepos(repo_attrs, repo_attr_dict, endpoint)
            elif command_input == 'user:gists':
                userGists(gists_attrs, gists_attr_dict, endpoint)
            elif command_input == 'user:orgs':
                userOrgs(org_attrs, org_attr_dict, endpoint)
            elif command_input == 'user:profile':
                userProfile(profile_attrs, profile_attr_dict, endpoint)
            elif command_input == 'user:events':
                userEvents(endpoint)
            elif command_input == 'user:followers':
                userFollowers(user_attrs, user_attr_dict, endpoint)
            elif command_input == 'user:following':
                userFollowing(endpoint)
            elif command_input == 'user:subscriptions':
                userSubscriptions(repo_attrs, repo_attr_dict, endpoint)
            elif command_input == 'search:users':
                userSearch(user_attrs, user_attr_dict, endpoint)
            elif command_input == 'search:repos':
                repoSearch(repo_attrs, repo_attr_dict, endpoint)
            elif command_input == 'search:topics':
                topicSearch(topic_attrs, topic_attr_dict, endpoint)
            elif command_input == 'search:issues':
                issueSearch(issue_attrs, issue_attr_dict, endpoint)
            elif command_input == 'search:commits':
                commitsSearch(endpoint)
            elif command_input == 'logs:view':
                viewLogs()
            elif command_input == 'logs:read':
                readLog()
            elif command_input == 'logs:delete':
                deleteLog()
            elif command_input == 'help':
                Help.helpCommand()
            elif command_input == 'help:search':
                Help.searchCommand()
            elif command_input == 'help:user':
                Help.userCommand()
            elif command_input == 'help:repo':
                Help.repoCommand()
            elif command_input == 'help:logs':
                Help.logsCommand()
            elif command_input == 'help:org':
                Help.orgCommand()
            elif command_input == 'author':
                author(author_dict)
            elif command_input == 'about':
                about()
            elif command_input == 'clear':
                clearScreen()
            elif command_input == 'version':
                versionInfo()
            elif command_input == 'exit':
                exitSession()
            else:
                pass
            print('\n')
            
        except KeyboardInterrupt:
            logging.info(logRoller.Ctrl.format('Ctrl+C'))
            print(Attributes.warning, logRoller.Ctrl.format(f'{Color.red}Ctrl{Color.reset}+{Color.red}C{Color.reset}'));break
            
        except Exception as e:
            logging.error(logRoller.Error.format(e))
            print(Attributes.error, logRoller.Error.format(f'{Color.red}{e}{Color.reset}'));exit()