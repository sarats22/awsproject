from flask import Flask, render_template
def main():
    return render_template('index.html')
if __name__ == "__main__":
    app.run(host= '0.0.0.0')
