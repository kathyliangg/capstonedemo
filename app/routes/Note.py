from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Note
from app.classes.forms import NoteForm
from flask_login import login_required
import datetime as dt

@app.route('/note/new', methods=['GET', 'POST'])
@login_required
def noteNew():
    form = NoteForm()
    if form.validate_on_submit():
        newNote = Note(
            author = current_user,
            note = form.note.data
        )
        newNote.save()
        # Once the new blog is saved, this sends the user to that blog using redirect.
        # and url_for. Redirect is used to redirect a user to different route so that 
        # routes code can be run. In this case the user just created a blog so we want 
        # to send them to that blog. url_for takes as its argument the function name
        # for that route (the part after the def key word). You also need to send any
        # other values that are needed by the route you are redirecting to.
        return redirect(url_for('notes',noteID=newNote.id))


    # if form.validate_on_submit() is false then the user either has not yet filled out
    # the form or the form had an error and the user is sent to a blank form. Form errors are 
    # stored in the form object and are displayed on the form. take a look at blogform.html to 
    # see how that works.
    return render_template('noteform.html',form=form)

@app.route('/note/list')
@app.route('/notes')
# This means the user must be logged in to see this page
@login_required
def noteList():
    # This retrieves all of the 'blogs' that are stored in MongoDB and places them in a
    # mongoengine object as a list of dictionaries name 'blogs'.
    notes = Note.objects()
    # This renders (shows to the user) the blogs.html template. it also sends the blogs object 
    # to the template as a variable named blogs.  The template uses a for loop to display
    # each blog.
    return render_template('notes.html',notes=notes)

@app.route('/note/<noteID>')
# This route will only run if the user is logged in.
@login_required
def notes(noteID):
    # retrieve the blog using the blogID
    thisNote = Note.objects.get(id=noteID)
    # If there are no comments the 'comments' object will have the value 'None'. Comments are 
    # related to blogs meaning that every comment contains a reference to a blog. In this case
    # there is a field on the comment collection called 'blog' that is a reference the Blog
    # document it is related to.  You can use the blogID to get the blog and then you can use
    # the blog object (thisBlog in this case) to get all the comments.
   
    # Send the blog object and the comments object to the 'blog.html' template.
    return render_template('note.html',note=thisNote)

@app.route('/note/delete/<noteID>')
@login_required
def noteDelete(noteID): 
    deleteNote = Note.objects.get(id=noteID)
    deleteNote.delete()
    flash('This note is deleted.')
    return redirect(url_for('noteList')) 

# @app.route('/stuffie/edit/<stuffieID>', methods=['GET', 'POST'])
# @login_required
# def stuffieEdit(stuffieID):
#     editStuffie = Stuffie.objects.get(id=stuffieID)

#     if current_user != editStuffie.author:
#         flash("You can't edit a stuffie that is not your's !")
#         return redirect(url_for('stuffie',stuffieID=editStuffie.id))
    
#     form = StuffieForm()

#     if form.validate_on_submit():
#         # thisDict = {"name":form.name.data,
#         #           "type":form.type.data,
#         #           "brand":form.brand.data
#                 #   }
#         editStuffie.update(
#             name = form.name.data,
#             type = form.type.data,
#             brand = form.brand.data
#         )
     
#         # editStuffie.update({"name":form.name.data,
#         #            "type":form.type.data,
#         #            "brand":form.brand.data})
        
#         #return redirect(url_for('stuffie',StuffieID=stuffieID))
#         return redirect(url_for('stuffieList'))
#     form = StuffieForm()

#     # flash('This stuffie is'+ stuffieID)
#     # return redirect(url_for('stuffieList')) 

#     form.name.data = editStuffie.name
#     form.type.data = editStuffie.type
#     form.brand.data = editStuffie.brand

#     return render_template('stuffieform.html',form=form,stuffie=stuffie)   



# @app.route('/stuffie/delete/<stuffieID>')
# @login_required
# def stuffieDelete(stuffieID): 
#     deleteStuffie = Stuffie.objects.get(id=stuffieID)
#     deleteStuffie.delete()
#     flash('This stuffie is deleted.')
#     return redirect(url_for('stuffieList')) 