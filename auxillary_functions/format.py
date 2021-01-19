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
