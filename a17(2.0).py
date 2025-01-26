from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess

def run_llama(query):
    """Runs the Llama 3.1 LLM with the given query and returns the response."""
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.1"],
            input=query,
            text=True,
            capture_output=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error while running Llama 3.1: {e}"

class RequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle preflight requests for CORS."""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        """Handle POST requests for code analysis."""
        if self.path == "/":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode("utf-8"))

            # Extract code snippet from the request
            code_snippet = request_data.get("code", "")

            if not code_snippet:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No code snippet provided"}).encode())
                return

            # Query for Llama
            query = f"""
            You are an Automated Code Analysis and Evaluation System. Only respond to programming language-related queries.
            Analyze the following code snippet and generate a report covering these points:
            1. Readability test
            2. Complexity
            3. Naming conventions
            4. Error handling
            5. Duplication
            6. Formatting
            7. Private key detection
            Provide suggestions for improvement.

            Code snippet:
            {code_snippet}
            """
            response = run_llama(query)

            # Send response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"report": response}).encode())

def run_server():
    server = HTTPServer(("localhost", 8000), RequestHandler)
    print("Server running on http://localhost:8000")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
