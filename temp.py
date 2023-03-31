import json
import shutil

"Fall%20Classic"
"john@simplylift.co"
"127.0.0.1:5000/book/Fall%20Classic/Simply%20Lift"

src = "tests/data/competitions.json"
dst = "competitions.json"

shutil.copy2(src, dst)