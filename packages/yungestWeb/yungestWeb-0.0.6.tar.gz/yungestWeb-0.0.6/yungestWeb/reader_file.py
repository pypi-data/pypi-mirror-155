import os.path
def render_html(filename) -> str:
    if os.path.isdir("templates"):
        try:
            return open(f"./templates/{filename}", "r").read()
        except FileNotFoundError:
            pass 
    else:
        print("Must create a folder named: 'templates' and put the file in it")

