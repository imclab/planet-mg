#!/usr/bin/python
"""Fix the Chaos Life feed.

The RSS source looks roughly like this::

    <item>
      <title>...</title>
      <description>
        <![CDATA[<p><a href="http://chaoslife.findchaos.com/comic-page"
                 title="Comic Title"><img
                 src="http://chaoslife.findchaos.com/comics-rss/comic.jpg"
                 alt="Comic Title" class="comicthumbnail"
                 title="Comic Title" /></a></p> ... truncated text ...
                 [&#8230;]]]>
      </description>
      <p>
        <a href="http://chaoslife.findchaos.com/comic-page"
           title="Comic Title">
          <img src="http://chaoslife.findchaos.com/comics-rss/comic.jpg"
               alt="Comic Title" class="comicthumbnail" title="Comic Title" />
        </a>
      </p>
      <content:encoded>
        <![CDATA[... full text without image links ...]]>
      </content:encoded>
      ... other metadata ...
    </item>

Planet mangles it into the following ATOM::

    <entry xmlns=".../Atom">
      <summary type="xhtml">
        <div xmlns=".../xhtml">
          <p>
            <a href="http://chaoslife.findchaos.com/comic-page"
               title="Comic Title">
              <img src="http://chaoslife.findchaos.com/comics-rss/comic.jpg"
                   alt="Comic Title" class="comicthumbnail" title="Comic Title" />
            </a>
            ... truncated text ... [&#x2026;]
          </p>
        </div>
      </summary>
      <content type="xhtml">
        <div xmlns=".../xhtml">
          <p>... full text no images ...</p>
        </div>
      </content>
    </entry>

We want to put the comic link and inline img in the ATOM <content>.
"""
import sys
import lxml.etree

doc = lxml.etree.parse(sys.stdin)

atom = "http://www.w3.org/2005/Atom"
xhtml = 'http://www.w3.org/1999/xhtml'
nsmap = dict(xhtml=xhtml, atom=atom)

comiclinks = doc.xpath('//atom:summary/xhtml:div/xhtml:p[xhtml:a[xhtml:img]]',
                       namespaces=nsmap)
if comiclinks:
    content_div = doc.xpath('//atom:content/xhtml:div', namespaces=nsmap)[0]
    content_div[:0] = comiclinks

print(lxml.etree.tostring(doc))
