import http.server
import subprocess
import os
import select
import shutil
import socketserver

GIT_PATH = "/tmp/atelier-git"
GIT_HTTP_BACKEND_PATH = "/usr/local/libexec/git-core/git-http-backend"
REPO_COUNT = 5

class GitHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
	rbufsize = 0 # it is super important to make the server unbuffered, otherwise it will hang

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

		env["CONTENT_TYPE"] = self.headers.get_content_type() if self.headers.get_content_type() else self.headers["content-type"]
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

		if pid == 0: # child
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

if __name__ == '__main__':
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
		subprocess.run(["git", "config", "user.name", "Tux"], cwd=working_path)
		subprocess.run(["git", "config", "user.email", "info@louvainlinux.org"], cwd=working_path)

		# add a file and commit it

		with open(os.path.join(working_path, "README.md"), "w") as f:
			f.write(f"# Repo {i}\n\nCeci est un fichier dans un dépôt git !\n")

		subprocess.run(["git", "add", "README.md"], cwd=working_path)
		subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=working_path)
		subprocess.run(["git", "push"], cwd=working_path)

	# serve the server

	with socketserver.TCPServer(("", 8000), GitHTTPRequestHandler) as httpd:
		print("Server started")
		httpd.serve_forever()
