import http.server
import subprocess
import os
import time
import re
import select
import shutil
import socketserver
import multiprocessing

GIT_PATH = os.environ.get("GIT_PATH", "/tmp/atelier-git")
GIT_HTTP_BACKEND_PATH = os.environ.get("GIT_HTTP_BACKEND_PATH", "/usr/lib/git-core/git-http-backend")
REPO_COUNT = int(os.environ.get('REPO_COUNT', 10))
POOL_COUNT = max(REPO_COUNT, multiprocessing.cpu_count())
SERVER_NAME = os.environ.get("SERVER_NAME", "Tux")
SERVER_EMAIL = os.environ.get("SERVER_EMAIL", "info@louvainlinux.org")


class GitHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
	rbufsize = 0  # it is super important to make the server unbuffered, otherwise it will hang

	def do_GET(self):
		self.run_cgi()

	def do_POST(self):
		self.run_cgi()

	def do_HEAD(self):
		self.run_cgi()

	def run_cgi(self):
		bits = self.path.split("/")
		repo = bits[1]

		if not repo.endswith(".git"):
			repo = repo + ".git"

		path = os.path.join(GIT_PATH, repo)
		translated = "/".join([path] + bits[2:])

		if "?" in translated:
			translated, query = translated.split("?")

		else:
			query = ""

		# XXX a lot of this is adapted from the deprecated CGIHTTPRequestHandler class

		env = {
			**os.environ,
			"SERVER_SOFTWARE": self.version_string(),
			"GATEWAY_INTERFACE": "CGI/1.1",
			"SERVER_PROTOCOL": self.protocol_version,
			"REQUEST_METHOD": self.command,
			"REMOTE_ADDR": self.client_address[0],
			"PATH_TRANSLATED": translated,
			"QUERY_STRING": query,
			"GIT_HTTP_EXPORT_ALL": "",
		}

		env["CONTENT_TYPE"] = (
			self.headers.get_content_type() if self.headers.get_content_type() else self.headers["content-type"]
		)
		length = self.headers.get("content-length")

		if length is not None:
			env["CONTENT_LENGTH"] = length

		accept = self.headers.get_all("accept", ())
		env["HTTP_ACCEPT"] = ",".join(accept)

		ua = self.headers.get("user-agent")

		if ua is not None:
			env["HTTP_USER_AGENT"] = ua

		co = filter(None, self.headers.get_all("cookie", []))
		env["HTTP_COOKIE"] = ", ".join(co)

		self.send_response(200, "Script output follows")
		self.flush_headers()

		# fork

		self.wfile.flush()
		pid = os.fork()

		if pid == 0:  # child
			try:
				os.dup2(self.rfile.fileno(), 0)
				os.dup2(self.wfile.fileno(), 1)
				os.execve(GIT_HTTP_BACKEND_PATH, [GIT_HTTP_BACKEND_PATH], env)

			except:
				self.server.handle_error(self.request, self.client_address)
				os._exit(127)

		# parent

		pid, status = os.waitpid(pid, 0)

		while select.select([self.rfile], [], [], 0)[0]:
			if not self.rfile.read(1):
				break

		code = os.waitstatus_to_exitcode(status)

		if code:
			print(f"CGI script exited with status {code}")


class Repo:
	def __init__(self, id: int, path: str, working_path: str):
		self.id = id
		self.path = path
		self.working_path = working_path
		self.last_commit_hash = ""

	def event(self):
		# check if there's a new commit which isn't from us

		out = subprocess.run(["git", "log", "--pretty=%ae:%H:%f"], cwd=self.path, capture_output=True, text=True)
		(*commits,) = map(lambda x: x.split(":"), out.stdout.strip().splitlines())

		if not commits:
			return

		email, last_commit_hash, body = commits[0]

		if email == SERVER_EMAIL:
			return

		if last_commit_hash == self.last_commit_hash:
			return

		print(self.last_commit_hash, last_commit_hash)
		self.last_commit_hash = last_commit_hash

		# handle the new commit

		body = body.lower()
		body = re.sub(r"-+", "-", body)

		def is_exercice(body: str, num: int):
			return f"exercice-{num}" in body or f"exercise-{num}" in body

		subprocess.run(["git", "pull"], cwd=self.working_path)

		if is_exercice(body, 2):
			filename = "simplythebest"
			count = 1

			while os.path.exists(os.path.join(self.working_path, filename)):
				count += 1
				filename = f"simplythebest-{count}"

			with open(os.path.join(self.working_path, filename), "w") as f:
				f.write("Simply the best\nBetter than all the rest\nBetter than anyone\nAnyone I've ever met\n")

			subprocess.run(["git", "add", filename], cwd=self.working_path)
			subprocess.run(["git", "commit", "-m", f"exercice 2: Simply the best ({count})"], cwd=self.working_path)
			subprocess.run(["git", "push"], cwd=self.working_path)

		if is_exercice(body, 3):
			path = os.path.join(self.working_path, "README.md")

			with open(path) as f:
				lines = f.read().splitlines()
				lines[0] = "# This title is SIMPLY THE BEST\n"

			with open(path, "w") as f:
				f.write("\n".join(lines))

			subprocess.run(["git", "add", "README.md"], cwd=self.working_path)
			subprocess.run(["git", "commit", "-m", "exercice 3: Update title of README"], cwd=self.working_path)
			subprocess.run(["git", "push"], cwd=self.working_path)

	def __repr__(self):
		return f"Repo({self.id})"


def repo_worker(repo):
	# TODO could this be instead called only when the repo endpoint is called?

	while True:
		repo.event()
		time.sleep(1)


if __name__ == "__main__":
	# create new git repos

	subprocess.run(["git", "config", "--global", "init.defaultBranch", "main"])
	shutil.rmtree(GIT_PATH, ignore_errors=True)
	os.mkdir(GIT_PATH)

	for i in range(REPO_COUNT):
		path = os.path.join(GIT_PATH, f"repo-{i}.git")
		print(f"Creating git repo {i} at {path}")

		os.mkdir(path)
		subprocess.run(["git", "init", "--bare"], cwd=path)

		# initial configuration

		subprocess.run(["git", "config", "http.receivepack", "true"], cwd=path)

		# clone the repo we just created into a working directory

		working_path = path + "-work"
		subprocess.run(["git", "clone", path, working_path])

		# configure working repository

		subprocess.run(["git", "config", "commit.gpgsign", "false"], cwd=working_path)
		subprocess.run(["git", "config", "user.name", SERVER_NAME], cwd=working_path)
		subprocess.run(["git", "config", "user.email", SERVER_EMAIL], cwd=working_path)

		# add a file and commit it

		with open(os.path.join(working_path, "README.md"), "w") as f:
			f.write(f"# Repo {i}\n\nCeci est un fichier dans un dépôt git !\n")

		subprocess.run(["git", "add", "README.md"], cwd=working_path)
		subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=working_path)
		subprocess.run(["git", "push"], cwd=working_path)

		# create repo worker process

		repo = Repo(i, path, working_path)

		p = multiprocessing.Process(target=repo_worker, args=(repo,))
		p.start()

	# serve the server

	with socketserver.TCPServer(("", 8000), GitHTTPRequestHandler) as httpd:
		print("Server started")
		httpd.serve_forever()
