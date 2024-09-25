# docstrings

docstrings_git = {
    "LOCAL_GIT_REPO_DIR": """
            Todo: could this description be derived programmatically? DRY.
            Full path to the local repo base directory where
            the repo GIT_REPO_NAME is located, i.e.
            - [x] `~/git/repos`
            - [ ] Todo: `/home/$USER/git/repos`
            - [ ] Todo: `$HOME/git/repos`
            """,
    "MASTER_BRANCH": """
            As long as I don't know how to
            programmatically identify the main branch, this
            needs to be specified, for example `main`
            or `master`.
            """,
    "GIT_REPO_NAME": """
            Name of the repo, for example
            `vortexLibrary`.
            """,
    "BRANCH_NAME": """
            Name of the dev branch, for 
            example `PTP-123_Some-Ticket-Title`.
            """,
    "GIT_SSH": """
            The URL to the Git repo over SSH,
            i.e. `git@github.com:animallogic-rnd/dumpo.git`.
            """
}
