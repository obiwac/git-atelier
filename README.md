# Atelier git

The presentation and resources used during the git workshop given by Louvain-li-Nux (currently francophone only).

## Building

This presentation uses [Marp](https://marp.app/) for its slides:

```console
npm -g install @marp-team/marp-cli
```

You can serve it as such:

```console
marp -w -s .
```

## Exercise server

With no extra dependencies (except for `git` ofc), simply:

```console
python server.py
```

This creates and hosts `REPO_COUNT` repos which can be accessed at `/repo-69`, and also hosts (but doesn't build!) the presentation at `/`.
It also creates an agent per repo for the exercises.

Here are the various environment variables:

|Name|Description|
|-|-|
|`GIT_PATH`|Where the server should store all of its data.|
|`GIT_HTTP_BACKEND`|Where the `git-http-backend` CGI script is located.|
|`REPO_COUNT`|How many repos to create.|
|`SERVER_NAME`|The name of the agent which will be shown in commits made by it.|
|`SERVER_EMAIL`|The email of the agent which will be shown in commits made by it.|
|`KEEP_REPO`|If set to a truthy value, the created repos won't be destroyed and recreated when the server is run.|

### Formatting

With `tan`:

```console
tan --use-tabs --line-length 120 .
```

## Next features

- English language slides.
- CI/CD setup (spellchecker, formatting, etc).
- Show a screenshot of going into settings before going to the SSH/GPG keys tab, because some people have a hard time finding it.
- Documentation on exercises of the exercise server.

## Notes

- Do break consistency by not adding dots at the end of commands, even if they're in a sentence. It can confuse people so the consistency isn't worth it.
- Don't introduce `--allow-empty` even for the commits intended to signal to the server to move to the next exercise, it just confuses people.
