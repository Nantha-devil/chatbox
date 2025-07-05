from flask import Flask, render_template,request
app = Flask(__name__)
conversation=[]
def nk(user):
    user=user.lower()
    if "hii" in user:
        return "can i help you"
    else:
        return"i don't understand"

@app.route('/', methods=["GET","POST"])
def sk():
    global conversation
    if request.method == "POST":
        user_msg=request.form["user_input"]
        bot=nk(user_msg)
        conversation.append(("you",user_msg))
        conversation.append(("bot",bot))
    return render_template("ht.html",conversation=conversation)

if __name__=="__main__":
    app.run(debug=True)

