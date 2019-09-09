# Given a template text file A and a content text file B, create a new file that
# replaces all of the content in the template A between two anchors with
# the contents of the contents of B. Write this file to filenameC

# NOTE: Nested replacements are not supported.
# Anchors should be alone on a line (excluding whitespace) but this is not enforced
# Any line including the anchor string will count as an anchor
# Nested anchors do not and should not work at all.

# START START END END will replace from the first start to the first end,
# NOT until the second end.

import sys

def splice(template, content, output, startAnchor, endAnchor):
    # template, content, output are all filenames / paths
    fTemplate = open(template, "r", encoding="utf-8")
    fContent  = open(content, "r", encoding="utf-8")
    fOutput   = open(output, "w", encoding="utf-8")

    replacing = False # Am I currently replacing?
    for templateLine in fTemplate:


        # This block of code is structured so oddly to highlight the fact
        # that it is basically a watered down DFA, with states and actions
        # for state transitions

        # In replace mode, print nothing from template
        # When end anchor reached in replace mode, print all content
        if replacing:
            if endAnchor in templateLine:
                # capture any whitespace before the endAnchor to make output prettier
                spaces = templateLine.find(endAnchor)

                replacing = False

                # Print each line of content, prepended by the same whitespace
                # as preceded the ending anchor
                for contentLine in fContent:
                    fOutput.write(" " * spaces)
                    fOutput.write(contentLine)

                # Print the end anchor when done
                fOutput.write(templateLine)
            else:
                pass # do nothing for template lines between anchors

        # In normal mode, print each line from template
        # When start anchor reached in normal mode, switch to replace mode
        else:
            if startAnchor in templateLine:
                replacing = True
                fOutput.write(templateLine)
            else:
                fOutput.write(templateLine)




def main():
    # Generate front.html (main LingDB site)
    template = "app/templates/front_template.html"
    content = "gen/out.html"
    output = "app/templates/front.html"

    start = "<!-- ANCHOR: AUTOGEN START -->"
    end   = "<!-- ANCHOR: AUTOGEN END -->"

    splice(template, content, output, start, end)

    # Generate survey.html (google docs autofiller site)
    template = "app/templates/survey_template.html"
    content = "gen/out.html"
    output = "app/templates/survey.html"

    splice(template, content, output, start, end)
