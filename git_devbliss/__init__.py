import pkg_resources


__version__ = pkg_resources.get_distribution("git_devbliss").version

# normal branches
branches = ['feature', 'bug', 'refactor', 'research']


def help():
    print('''
Usage:
    git devbliss {branches_usage} DESCRIPTION
    git devbliss hotfix VERSION DESCRIPTION
    git devbliss finish [BASE_BRANCH]
    git devbliss release VERSION
    git devbliss status
    git devbliss delete [-f]
    git devbliss issue [TITLE]
    git devbliss review <pull-request-id>
    git devbliss merge-button <pull-request-id>
    git devbliss close-button <pull-request-id>

Options:
    {branches_options}
                  Branch from master (normal branches)
    hotfix        Branch from a tag (fix a bug in an already released version)
    finish        Open a pull request for the current branch
    release       Create a new tag, commit and push
    status        List branches, pull requests, and issues
    issue         Quickly post an issue to GitHub
    delete        Delete the current branch on github.com
    review        Review a pull request with the given id
    merge-button  Merge a pull request with the given id
    close-button  Close a pull request with the given id without merging
    -v --version  Print version number of git-devbliss
'''[1:-1].format(
        branches_usage='[' + ' | '.join(branches) + ']',
        branches_options=', '.join(branches)
    ))


"""
#!/bin/bash

set -eu

# normal branches
branches=(feature bug refactor research)

function help {
    echo 'Usage:'
    echo '    git devbliss ['`echo "${branches[@]}" | sed 's/ / \| /g'`'] DESCRIPTION'
    echo '    git devbliss hotfix VERSION DESCRIPTION'
    echo '    git devbliss finish [BASE_BRANCH]'
    echo '    git devbliss release VERSION'
    echo '    git devbliss status'
    echo '    git devbliss delete [-f]'
    echo '    git devbliss issue [TITLE]'
    echo '    git devbliss review <pull-request-id>'
    echo '    git devbliss merge-button <pull-request-id>'
    echo '    git devbliss close-button <pull-request-id>'
    echo
    echo 'Options:'
    echo '    '`echo "${branches[@]}" | sed 's/ /, /g'`
    echo '                  Branch from master (normal branches)'
    echo '    hotfix        Branch from a tag (fix a bug in an already released version)'
    echo '    finish        Open a pull request for the current branch'
    echo '    release       Create a new tag, commit and push'
    echo '    status        List branches, pull requests, and issues'
    echo '    issue         Quickly post an issue to GitHub'
    echo '    delete        Delete the current branch on github.com'
    echo '    review        Review a pull request with the given id'
    echo '    merge-button  Merge a pull request with the given id'
    echo '    close-button  Close a pull request with the given id without merging'
    echo '    -v --version  Print version number of git-devbliss'
}

function version {
    changelog="/opt/local/share/doc/git-devbliss/CHANGES.md"
    if [[ ! -e $changelog ]]; then
        changelog="/usr/share/doc/git-devbliss/CHANGES.md"
    fi
    local local_version=$(perl -ne '/^#+ +\d+\.\d+\.\d+([^\.].*)?$/ && s/^#+ +(\d+\.\d+\.\d+)/$1/ && print && exit' $changelog)
    echo $local_version
}

function is_repository_clean {
    if [ "`git status --short --untracked-files=no | wc -l | sed -e 's/ //g'`" != "0" ]; then
        return 1
    fi
    return 0
}

function is_synced_origin {
    if [ "$(git diff origin/${1} | wc -l | sed -e 's/ //g')" != "0" ]; then
        return 1
    fi
    if [ "$(git log origin/${1}..HEAD -- | wc -l | sed -e 's/ //g')" != "0" ]; then
        return 1
    fi
    return 0
}

function check_repo_toplevel {
    # check if pwd is repository root in order to run makefile hooks properly
    if [[ $(git rev-parse --show-toplevel) != $(pwd) ]]; then
        echo "You need to run this command from the toplevel of the working tree." > /dev/stderr
        exit 2
    fi
}

function makefile_hooks {
    # if you use this function always run the check_repo_toplevel beforehand
    # otherwise the makefile will not be found.
    #
    # reasonable targets are: changelog, version, test (see: README.md)
    if [ ! -f Makefile ]; then
        echo "Warning: No Makefile found. All make hooks have been skipped." >> /dev/stderr
        return
    fi
    make $1 || echo "Warning: Makefile has no target named \"$1\"." >> /dev/stderr
}

function is_branch_command {
    local e
    for e in "${branches[@]}"; do [[ "$e" == "$1" ]] && return 0; done
    return 1
}

function hotfix {

    # hotfix function needs two parameters: version and description
    if [[ $# != 2 ]]; then
        help
    fi

    if git tag | grep $1; then
        git fetch origin
        git checkout --quiet $1
        git checkout --quiet -b hotfix/$2 &> /dev/null
        git checkout --quiet hotfix/$2 &> /dev/null
        git push --set-upstream origin hotfix/$2
    else
        echo "No such tag: $1" > /dev/stderr
        echo "Available tags:" > /dev/stderr
        git tag | awk '{print "    "$1}'
        exit 2
    fi
}

function branch {

    # branch function needs two parameters:
    if [[ $# != 2 ]]; then
        help
    fi

    if [ $2 = "finish" ]; then
        echo "You are creating a branch \"$1/$2\", did you mean to type \"git devbliss finish\"?"
        echo "You can delete this branch with \"git devbliss delete\""
    fi
    git checkout --quiet master
    git pull --quiet origin master
    git checkout --quiet -b $1/$2 || git checkout --quiet $1/$2
    git push --set-upstream origin $1/$2
}

function release {

    # the first parameter is the version and must have the following format: 1.12.0
    if echo $1 | grep -vE '^[0-9]+\.[0-9]+\.[0-9]+$'; then
        echo "Invalid version number" > /dev/stderr
        exit 2
    fi

    echo $1

    check_repo_toplevel # neccessary to run makefile hooks
    git fetch --quiet origin
    local branch=`git rev-parse --abbrev-ref HEAD`
    if ! is_repository_clean; then
        echo "Error: Repository is not clean. Aborting." >> /dev/stderr
        exit 1
    fi
    if ! is_synced_origin $branch; then
        echo "Error: Local branch is not in sync with origin. Aborting." >> /dev/stderr
        echo "Do 'git pull && git push' and try agin." >> /dev/stderr
        exit 1
    fi
    export DEVBLISS_VERSION="$1"
    makefile_hooks release
    git diff
    echo "Have these changes been reviewed?"
    echo "[enter / ctrl+c to cancel]"
    read || exit 2
    if ! is_repository_clean; then
        git commit --quiet -am "Ran git devbliss release hook"
    fi
    unset DEVBLISS_VERSION
    git commit --quiet --allow-empty -m "Release: $1"
    git push origin $branch
    git tag $1
    git push --tags origin
    git push origin $branch
    if [[ "$branch" != 'master' ]]; then
        echo
        github-devbliss pull-request
    fi
}

function finish {
    local base_branch=${1-}
    check_repo_toplevel # neccessary to run makefile hooks
    local branch=`git rev-parse --abbrev-ref HEAD`
    if ! is_repository_clean; then
        echo "Error: Repository is not clean. Aborting." >> /dev/stderr
        exit 1
    fi
    if ! git branch --contains master | grep "$branch" > /dev/null; then
        if [[ $branch = hotfix/* ]]; then
            echo "Warning: Master is not merged into the current branch." > /dev/stderr
        else
            echo "Error: Won't finish. Master is not merged into the current branch." > /dev/stderr
            echo "Please do 'git merge master', make sure all conflicts are merged and try again." > /dev/stderr
            exit 1
        fi
    fi
    export DEVBLISS_BRANCH_TYPE=`echo $branch | sed -e 's#\([^/]*\)/.*#\1#g'`
    makefile_hooks finish
    if ! is_repository_clean; then
        git commit --quiet -am "Ran git devbliss finish hook"
    fi
    makefile_hooks changelog
    if ! is_repository_clean; then
        git commit --quiet -am "Ran git devbliss changelog hook"
    fi
    makefile_hooks version
    if ! is_repository_clean; then
        git commit --quiet -am "Ran git devbliss version hook"
    fi
    git push origin $branch
    echo
    github-devbliss pull-request ${base_branch-}
    echo
    github-devbliss open-pulls
}

function delete {

    # delete function can take one parameter -f
    if [[ $# -gt 1 || $1 != "-f" ]]; then
        help
    fi

    local branch=`git rev-parse --abbrev-ref HEAD`
    if [[ "$branch" == "master" ]]; then
        echo "Won't delete master branch. Aborting." > /dev/stderr
        exit 2
    fi
    if [[ $1 = "-f" ]]; then
        git push --delete origin $branch
    else
        echo -n "Really delete the remote branch? [y/N] "
        read a
        if [[ $a == "y" || $a == "Y" ]]; then
            git push --delete origin $branch
            echo 'To restore the remote branch, type'
            echo '    git push --set-upstream origin '$branch
            echo 'To delete your local branch, type'
            echo '    git checkout master && git branch -d '$branch
        else
            echo "Fatal: user interrupt" > /dev/stderr
            exit 2
        fi
    fi
}

function cleanup {

    git fetch
    echo "Deleting remote tracking branches whose tracked branches on server are gone..."
    git remote prune origin
    echo "Searching all remote branches except release that are already merged into master..."
    get_remote_merged_branches=`git branch -r --merged origin/master | grep -v master | grep -v release`
    echo "$get_remote_merged_branches" | grep '\w' && read -p "Do you want to delete those branches on the server? [y/N] " -r
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "Deleting..."
        echo "$get_remote_merged_branches" | sed 's#origin/##' | xargs -I {} git push origin :{}
        git remote prune origin
    else
        if [ "" = "$get_remote_merged_branches" ]
        then
            echo "nothing to do."
        else
            echo "ok, will not delete anything."
        fi
    fi
    echo "Deleting all local branches (except current) that are already merged into local master..."
    git branch --merged master | grep -v master | grep -v '\*' | xargs git branch -d
    echo "Checking for unmerged local branches..."
    git branch --no-merged master

}

# check whether the pwd is a git repository
git rev-parse --abbrev-ref HEAD > /dev/null || exit 1

# chech whether origin points to github.com
if ! git remote -v | grep "^origin.*github.*:.*(fetch)$" > /dev/null; then
    echo "Fatal: origin does not point to a github.com repository" > /dev/stderr
    exit 1
fi

github_functions=( "issue" "merge-button" "status" "review" "close-button" )
git_devbliss_functions=( "finish" "hotfix" "release" "delete" "cleanup")
if [ $# == 0 ]; then
    help
elif [[  "${github_functions[@]}" =~ $1 ]]; then
    github-devbliss $@
elif [[ "${git_devbliss_functions[@]}" =~ $1 ]]; then
    $@
elif [ $1 == "-v" ] || [ $1 == "--version" ]; then
    version
elif is_branch_command $1; then
    branch $1 $2
else
    help
fi
"""
