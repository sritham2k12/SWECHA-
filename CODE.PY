from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import matplotlib.pyplot as plt
import io
import base64

# Replace with your actual API key
API_KEY = "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"

def analyze_code(code_snippet):
    """Analyze code snippet and return a simulated report."""
    # Simulated analysis report
    report = {
        "readability": 75,
        "complexity": 60,
        "naming_conventions": 85,
        "error_handling": 50,
        "duplication": 90,
        "formatting": 80,
        "private_key_detection": 95,
    }
    return report

def generate_graph(report):
    """Generate a graph representation of the analysis report."""
    categories = list(report.keys())
    values = list(report.values())

    # Create the bar graph
    plt.figure(figsize=(10, 5))
    plt.bar(categories, values, color='skyblue')
    plt.title("Code Analysis Report")
    plt.ylabel("Score (%)")
    plt.xticks(rotation=45)

    # Save the graph to a base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    graph_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()

    return graph_base64

def generate_pie_chart(report):
    """Generate a pie chart representation of the analysis report."""
    labels = list(report.keys())
    sizes = list(report.values())

    # Create the pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20c.colors)
    plt.title("Code Analysis Breakdown")

    # Save the pie chart to a base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    pie_chart_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()

    return pie_chart_base64

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
            # Handle incoming data
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            try:
                request_data = json.loads(post_data.decode("utf-8"))
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid JSON format"}).encode())
                return

            # Extract code snippet
            code_snippet = request_data.get("code", "")

            if not code_snippet:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No code snippet provided"}).encode())
                return

            # Analyze the code and generate graphs
            report = analyze_code(code_snippet)
            graph_base64 = generate_graph(report)
            pie_chart_base64 = generate_pie_chart(report)

            # Prepare the response
            response = {
                "report": report,
                "graph": graph_base64,
                "pie_chart": pie_chart_base64
            }

            # Send the response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

def run_server():
    server = HTTPServer(("localhost", 8000), RequestHandler)
    print("Server running on http://localhost:8000")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
