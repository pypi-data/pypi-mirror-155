``ArchiveNews 0.2 (Beta)``
=======

A module that allows you to get and analyze news from `Arquivo.pt <https://arquivo.pt/>`_

Main Features
^^^^^^^
* Get Past Covers from Newspapers
* Get Past News from Newspapers
* Get Deep Data from the News (Title, Snippet, Link, Author, Date, Locations, Organizations, People and Keywords)
* Analysis the News

Usage (Python)
^^^^^^^
How to use it on Python

``1. Install the Module``::

   pip install git+https://github.com/diogocorreia01/ArchiveNews.git

``2. Get the Covers``::

   Get_Covers(years=[2013], output_path='Samples\\CoverSample.json', newspaper_url='https://www.publico.pt')

``3. Get the News``::

       Get_News(input_file='Samples\\CoverSample.json', newspaper_url='https://www.publico.pt/', news_htmlTag='article', news_htmlClass='hentry', titles_htmlTag='h2', titles_htmlClass='entry-title', snippets_htmlTag='div',
         snippets_htmlClass='entry-summary', links_htmlTag='a', links_htmlClass='href', authors_htmlTag='span', authors_htmlClass='fn', output_path='Samples\\NewsSample')

``4. Get the News Data``::

       Get_News_Data(Samples\\NewsSample.json, Samples\\NewsDataSample)


Related projects
^^^^^^^
``Arquivo Publico`` -


