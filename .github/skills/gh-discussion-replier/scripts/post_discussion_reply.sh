#!/usr/bin/env bash

# Post a reply to a GitHub Discussion via GraphQL
# Usage: ./post_discussion_reply.sh <discussion_number> <body_file_or_string>
#
# Examples:
#   ./post_discussion_reply.sh 66 "Thanks for the suggestion!"
#   ./post_discussion_reply.sh 66 /tmp/reply_body.md

DISC_NUM=$1
BODY_INPUT=$2

if [ -z "$DISC_NUM" ] || [ -z "$BODY_INPUT" ]; then
    echo "Usage: $0 <discussion_number> <body_text_or_file>"
    exit 2
fi

# 1. Get repo info
REPO_FULL=$(gh repo view --json owner,name -q ".owner.login + \"/\" + .name")
OWNER="${REPO_FULL%/*}"
REPO="${REPO_FULL#*/}"

# 2. Get discussion node ID
DISC_ID=$(gh api graphql -f query="
query {
  repository(owner: \"$OWNER\", name: \"$REPO\") {
    discussion(number: $DISC_NUM) { id }
  }
}" -q ".data.repository.discussion.id")

if [ -z "$DISC_ID" ] || [ "$DISC_ID" == "null" ]; then
    echo "Error: Could not find discussion #$DISC_NUM"
    exit 1
fi

# 3. Read body from file or use as string
if [ -f "$BODY_INPUT" ]; then
    BODY=$(cat "$BODY_INPUT")
else
    BODY="$BODY_INPUT"
fi

# 4. Post reply
RESULT=$(gh api graphql -f query='
mutation($body:String!, $discussionId:ID!) {
  addDiscussionComment(input:{body:$body, discussionId:$discussionId}) {
    comment { id url }
  }
}' -f body="$BODY" -f discussionId="$DISC_ID")

COMMENT_URL=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['data']['addDiscussionComment']['comment']['url'])")
echo "Posted: $COMMENT_URL"
