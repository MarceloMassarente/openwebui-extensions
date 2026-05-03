#!/usr/bin/env bash

# Discussion Star Checker
# Usage: ./check_discussion_star.sh <discussion_number>

DISC_NUM=$1
if [ -z "$DISC_NUM" ]; then exit 2; fi

# 1. Get Repo info
REPO_FULL=$(gh repo view --json owner,name -q ".owner.login + \"/\" + .name")
OWNER="${REPO_FULL%/*}"
REPO="${REPO_FULL#*/}"

# 2. Get discussion author via GraphQL
USER_LOGIN=$(gh api graphql -f query="
query {
  repository(owner: \"$OWNER\", name: \"$REPO\") {
    discussion(number: $DISC_NUM) {
      author { login }
    }
  }
}" -q ".data.repository.discussion.author.login")

if [ -z "$USER_LOGIN" ] || [ "$USER_LOGIN" == "null" ]; then
    echo "Error: Could not find discussion #$DISC_NUM"
    exit 2
fi

# 3. Use GraphQL to check star status
IS_STARRED=$(gh api graphql -f query='
query($owner:String!, $repo:String!, $user:String!) {
  repository(owner:$owner, name:$repo) {
    stargazers(query:$user, first:1) {
      nodes {
        login
      }
    }
  }
}' -f owner="$OWNER" -f repo="$REPO" -f user="$USER_LOGIN" -q ".data.repository.stargazers.nodes[0].login")

if [ "$IS_STARRED" == "$USER_LOGIN" ]; then
    echo "Confirmed: @$USER_LOGIN HAS starred $REPO_FULL. ⭐"
    exit 0
else
    echo "Confirmed: @$USER_LOGIN has NOT starred $REPO_FULL."
    exit 1
fi
