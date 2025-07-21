from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import sendgrid
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev')

@app.route("/", methods=["GET", "POST"])
def index():
    # Default selections for the new multi-step process
    selections = {
        "cover_type": "paperback",
        "binding_type": "copta", 
        "cover_shape": "flat",
        "pages": "100",
        "size": "A5"
    }
    return render_template("index.html", selections=selections)

@app.route("/submit", methods=["POST"])
def submit():
    # Collect notebook selections
    notebook = {
        "cover_type": request.form.get("cover_type"),
        "binding_type": request.form.get("binding_type"),
        "cover_shape": request.form.get("cover_shape"),
        "pages": request.form.get("pages"),
        "size": request.form.get("size")
    }
    # Collect user details
    user = {
        "full_name": request.form.get("full_name"),
        "email": request.form.get("email"),
        "address1": request.form.get("address1"),
        "address2": request.form.get("address2"),
        "country": request.form.get("country"),
        "city": request.form.get("city"),
        "locality": request.form.get("locality"),
        "phone": request.form.get("phone")
    }
    # Prepare email content
    subject = "New Notebook Order"
    vendor_email = "link2000ve@gmail.com"
    user_email = user["email"]
    from_email = os.environ.get("ORDER_SENDER_EMAIL", "noreply@notebookstore.com")
    html_content = f"""
    <h2>New Notebook Order</h2>
    <h3>Notebook Details</h3>
    <ul>
        <li><b>Cover Type:</b> {notebook['cover_type']}</li>
        <li><b>Binding Type:</b> {notebook['binding_type']}</li>
        <li><b>Cover Shape:</b> {notebook['cover_shape']}</li>
        <li><b>Pages:</b> {notebook['pages']}</li>
        <li><b>Size:</b> {notebook['size']}</li>
    </ul>
    <h3>User Details</h3>
    <ul>
        <li><b>Full Name:</b> {user['full_name']}</li>
        <li><b>Email:</b> {user['email']}</li>
        <li><b>Address 1:</b> {user['address1']}</li>
        <li><b>Address 2:</b> {user['address2']}</li>
        <li><b>Country:</b> {user['country']}</li>
        <li><b>City:</b> {user['city']}</li>
        <li><b>Locality:</b> {user['locality']}</li>
        <li><b>Phone:</b> {user['phone']}</li>
    </ul>
    """
    # Send email using SendGrid
    try:
        sg = sendgrid.SendGridAPIClient(api_key=os.environ["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"])
        message = Mail(
            from_email=from_email,
            to_emails=[vendor_email, user_email],
            subject=subject,
            html_content=html_content
        )
        sg.send(message)
        # Return JSON for JS pop-up
        return jsonify({"success": True, "message": "Your order has been submitted successfully, please check your inbox."})
    except Exception as e:
        return jsonify({"success": False, "message": f"There was an error sending your order: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
