from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Stuffie
from app.classes.forms import StuffieForm
from flask_login import login_required
import datetime as dt

@app.route('/stuffie/new', methods=['GET', 'POST'])
# This means the user must be logged in to see this page
@login_required
# This is a function that is run when the user requests this route.
def stuffieNew():
    # This gets the form object from the form.py classes that can be displayed on the template.
    form = StuffieForm()

    # This is a conditional that evaluates to 'True' if the user submitted the form successfully.
    # validate_on_submit() is a method of the form object. 
    if form.validate_on_submit():

        # This stores all the values that the user entered into the new blog form. 
        # Blog() is a mongoengine method for creating a new blog. 'newBlog' is the variable 
        # that stores the object that is the result of the Blog() method.  
        newStuffie = Stuffie(
            # the left side is the name of the field from the data table
            # the right side is the data the user entered which is held in the form object.
            name = form.name.data,
            type = form.type.data,
            brand = form.brand.data,
            # This sets the modifydate to the current datetime.
        )
        # This is a method that saves the data to the mongoDB database.
        newStuffie.save()

        # Once the new blog is saved, this sends the user to that blog using redirect.
        # and url_for. Redirect is used to redirect a user to different route so that 
        # routes code can be run. In this case the user just created a blog so we want 
        # to send them to that blog. url_for takes as its argument the function name
        # for that route (the part after the def key word). You also need to send any
        # other values that are needed by the route you are redirecting to.
        return redirect(url_for('stuffie',stuffieID=newStuffie.id))

    # if form.validate_on_submit() is false then the user either has not yet filled out
    # the form or the form had an error and the user is sent to a blank form. Form errors are 
    # stored in the form object and are displayed on the form. take a look at blogform.html to 
    # see how that works.
    return render_template('stuffieform.html',form=form)

@app.route('/stuffie/list')
@app.route('/stuffies')
# This means the user must be logged in to see this page
@login_required
def stuffieList():
    # This retrieves all of the 'blogs' that are stored in MongoDB and places them in a
    # mongoengine object as a list of dictionaries name 'blogs'.
    stuffies = Stuffie.objects()
    # This renders (shows to the user) the blogs.html template. it also sends the blogs object 
    # to the template as a variable named blogs.  The template uses a for loop to display
    # each blog.
    return render_template('stuffies.html',stuffies=stuffies)

@app.route('/stuffie/<stuffieID>')
# This route will only run if the user is logged in.
@login_required
def stuffie(stuffieID):
    # retrieve the blog using the blogID
    thisStuffie = Stuffie.objects.get(id=stuffieID)
    # If there are no comments the 'comments' object will have the value 'None'. Comments are 
    # related to blogs meaning that every comment contains a reference to a blog. In this case
    # there is a field on the comment collection called 'blog' that is a reference the Blog
    # document it is related to.  You can use the blogID to get the blog and then you can use
    # the blog object (thisBlog in this case) to get all the comments.
   
    # Send the blog object and the comments object to the 'blog.html' template.
    return render_template('stuffie.html',stuffie=thisStuffie)

@app.route('/stuffie/edit/<stuffieID>', methods=['GET', 'POST'])
@login_required
def stuffieEdit(stuffieID):
    editStuffie = Stuffie.objects.get(id=stuffieID)
    if current_user != editStuffie.author:
        flash("You can't edit a stuffie that is not your's !")
        return redirect(url_for('stuffie',stuffieID=editStuffie.stuffie.id))
    Stuffie = Stuffie.objects.get(id=editStuffie.stuffie.id)
    form = StuffieForm()
    if form.validate_on_submit():
        editStuffie.update(
            name = form.name.data,
            type = form.type.data,
            brand = form.brand.data,
            modifydate = dt.datetime.utcnow
        )
        return redirect(url_for('stuffie',StuffieID=editStuffie.stuffie.id))

    form.name.data = editStuffie.name
    form.type.data = editStuffie.type
    form.brand.data = editStuffie.brand

    return render_template('stuffieform.html',form=form,stuffie=stuffie)   

@app.route('/stuffie/delete/<stuffieID>')
@login_required
def stuffieDelete(stuffieID): 
    deleteStuffie = Stuffie.objects.get(id=stuffieID)
    deleteStuffie.delete()
    flash('This stuffie is deleted.')
    return redirect(url_for('stuffie',stuffieID=deleteStuffie.stuffie.id)) 