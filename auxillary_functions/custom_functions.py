import sys,os

def update_progress(progress):
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    return sys.stdout.write(text)


def system_check(core_files):
    '''
    The programm relies on custom python modules to assure that functionality
    of the programm can be maintened. In order to do this,
    a check is performed to make sure that the necessary files are in their respective folders
    '''

    core_files_counter = 0
    missing_file = []

    # Performing a file check by counting the mandatory files
    for file in core_files:
         if os.path.exists(file): core_files_counter += 1
         else: missing_file.append(file)

    # If all of the availabe files are avaible, then the program can start.
    if core_files_counter == len(core_files):
        return True,missing_file
    else:
        return False,missing_file


def book_style():
    '''
    CSS styling sheet necessary for formating the epub file
    '''

    css = '''@namespace h "http://www.w3.org/1999/xhtml";
    body {
      display: block;
      margin: 5pt;
      page-break-before: always;
      text-align: justify;
    }
    h1, h2, h3 {
      font-weight: bold;
      margin-bottom: 1em;
      margin-left: 0;
      margin-right: 0;
      margin-top: 1em;
    }
    p {
      margin-bottom: 1em;
      margin-left: 0;
      margin-right: 0;
      margin-top: 1em;
    }
    a {
      color: inherit;
      text-decoration: inherit;
      cursor: default;
    }
    a[href] {
      color: blue;
      text-decoration: none;
      cursor: pointer;
    }
    a[href]:hover {
      color: red;
    }
    .center {
      text-align: center;
    }
    .cover {
      height: 100%;
    }'''
    return css
