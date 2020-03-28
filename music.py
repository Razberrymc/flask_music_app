from flask import Flask, render_template
import csv
def convert_to_dict(filename):
    """
    Convert a CSV file to a list of Python dictionaries
    """
    # open a CSV file - note - must have column headings in top row
    datafile = open(filename, newline='')

    # create DictReader object
    my_reader = csv.DictReader(datafile)

    # create a regular Python list containing dicts
    list_of_dicts = list(my_reader)

    # close original csv file
    datafile.close()

    # return the list
    return list_of_dicts

def make_ordinal(num):
    """
    Create an ordinal (1st, 2nd, etc.) from a number.
    """
    base = num % 10
    if base in [0,4,5,6,7,8,9] or num in [11,12,13]:
        ext = "th"
    elif base == 1:
        ext = "st"
    elif base == 2:
        ext = "nd"
    else:
        ext = "rd"
    return str(num) + ext

app = Flask(__name__)
application = app

# create a list of dicts from a CSV
music_list = convert_to_dict("music.csv")

# create a list of tuples in which the first item is the number
# (Presidency) and the second item is the name (President)
pairs_list = []
for s in music_list:
    pairs_list.append( (s['id'], s['name']) )

# first route

@app.route('/')
def index():
    return render_template('index.html', pairs=pairs_list, the_title="Music Index")

# second route

@app.route('/song/<num>')
def detail(num):
    try:
        mus_dict = music_list[int(num) - 1]
    except:
        return f"<h1>Invalid value for Song: {num}</h1>"
    # a little bonus function, imported on line 2 above
    ord = make_ordinal( int(num) )
    return render_template('music.html', mus=mus_dict, ord=ord, the_title=mus_dict['name'])


# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
