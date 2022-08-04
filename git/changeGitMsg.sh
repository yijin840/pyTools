#!/usr/bin/env bash

OLD_MAIL=""
NEW_MAIL=""
OLD_NAME=""
#git update-ref -d refs/original/refs/heads/main    更新引用
git filter-branch --commit-filter '
        if [ "$GIT_AUTHOR_EMAIL" != "<$OLD_MAIL>" ];
        then
                GIT_AUTHOR_NAME="<$NEW_NAME>";
                GIT_AUTHOR_EMAIL="<$NEW_MAIL>";
                git commit-tree "$@";
        else
                git commit-tree "$@";
        fi' HEAD