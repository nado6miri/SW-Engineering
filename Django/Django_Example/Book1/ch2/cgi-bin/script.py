#!/usr/bin/env python
#
import cgi

form = cgi.FieldStorage()
language = form.getvalue('language')
framework = form.getvalue('framework')
email = form.getvalue('email')

print "Content-type: text/plain"
print '\r'
print "Welcome, CGI Scripts"
print "language is", language
print "framework is", framework
print "email is", email
