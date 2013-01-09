from pyparsing import *
import urllib

removeText = replaceWith("")
scriptOpen,scriptClose = makeHTMLTags("script")
scriptBody = scriptOpen + SkipTo(scriptClose) + scriptClose
scriptBody.setParseAction(removeText)

anyTag,anyClose = makeHTMLTags(Word(alphas,alphanums+":_"))
anyTag.setParseAction(removeText)
anyClose.setParseAction(removeText)
htmlComment.setParseAction(removeText)

commonHTMLEntity.setParseAction(replaceHTMLEntity)

# get some HTML
targetURL = "http://allaboutmodels.net/ali-lagarde/"
targetPage = urllib.urlopen( targetURL )
targetHTML = targetPage.read()
targetPage.close()

# first pass, strip out tags and translate entities
firstPass = (htmlComment | scriptBody | commonHTMLEntity | 
             anyTag | anyClose ).transformString(targetHTML)

# first pass leaves many blank lines, collapse these down
repeatedNewlines = LineEnd() + OneOrMore(LineEnd())
repeatedNewlines.setParseAction(replaceWith("\n\n"))
secondPass = repeatedNewlines.transformString(firstPass)

print secondPass
