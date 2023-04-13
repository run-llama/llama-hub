# StackoverflowReader (In Beta)

Using the Stackoverflow API, this class will read the Stackoverflow Teams API and return a list of questions and answers based on posts.

It also supports caching the results to a local directory, so that you can run the load_data() method multiple times without hitting the API.

## getting a token

Visit: https://stackoverflowteams.com/users/pats/

1. Click Create a new PAT
3. Name the token, and pick the team scope
4. Select an expiration date
5. Click Create

Add this to your env, or to the instantiation of the `StackoverflowReader(pa_token, team_name, cache_dir='./stackoverflow_cache')`

```bash
export STACKOVERFLOW_PAT=your_token
export STACKOVERFLOW_TEAM_NAME=your_team
```



Other features which could be added:

 - Add articles
 - Add comments
 - Add tags
 - Add users
 - Add votes
 - Add badges
